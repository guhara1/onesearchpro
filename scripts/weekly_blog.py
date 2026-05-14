#!/usr/bin/env python3
"""
Weekly blog auto-publish script.

Reads CONTENT_CALENDAR.md to find the next pending topic,
calls Anthropic Claude API to generate a structured blog article,
inserts the article into partials/build_pages.py at the AUTO-INSERT marker,
updates sitemap.xml and CONTENT_CALENDAR.md, then runs build_pages.py.

Designed to run from GitHub Actions, but can be run locally too.
Requires: ANTHROPIC_API_KEY environment variable.
"""

import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Installing anthropic SDK...")
    subprocess.run([sys.executable, "-m", "pip", "install", "anthropic"], check=True)
    import anthropic


ROOT = Path(__file__).parent.parent
CALENDAR = ROOT / "CONTENT_CALENDAR.md"
BUILD_PAGES = ROOT / "partials" / "build_pages.py"
SITEMAP = ROOT / "sitemap.xml"

CATEGORY_MAP = {
    "구글 SEO": "google-seo",
    "기술 SEO": "technical-seo",
    "콘텐츠 SEO": "content-seo",
    "지역 SEO": "local-seo",
    "백링크·디지털 PR": "backlink-pr",
    "백링크 · 디지털 PR": "backlink-pr",
    "SNS 마케팅": "sns",
    "검색 노출 문제 해결": "visibility",
}


def find_next_topic():
    """Find the first unchecked topic in CONTENT_CALENDAR.md weekly plan."""
    content = CALENDAR.read_text(encoding="utf-8")
    # Match lines like "- [ ] **W2 [기술 SEO]** Topic title"
    pattern = re.compile(
        r"- \[ \] \*\*W(\d+) \[([^\]]+)\]\*\* ([^\n→]+?)(?:\s*→.*)?$",
        re.MULTILINE,
    )
    for m in pattern.finditer(content):
        week, category, title = m.groups()
        category = category.strip()
        return {
            "week": week,
            "category": category,
            "category_slug": CATEGORY_MAP.get(category, "general"),
            "title": title.strip(),
            "raw_line": m.group(0),
        }
    return None


def generate_article(topic):
    """Call Claude API to generate structured article data as JSON."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set")

    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = (
        "당신은 한국 SEO·디지털 마케팅 에이전시 OneSearchPro의 시니어 콘텐츠 작가입니다. "
        "구글 정책을 엄격히 준수하고 E-E-A-T 신호를 강화하는 블로그 글을 작성합니다. "
        "AI 양산 패턴을 피하고 자연스러운 한국어로 작성합니다."
    )

    user_prompt = f"""다음 주제로 OneSearchPro 블로그 글을 작성해주세요.

카테고리: {topic['category']}
주제: {topic['title']}

핵심 작성 규칙 (E-E-A-T 준수):
- 한국 시장 맥락 (네이버, 카카오, 한국 광고 정책 등) 자연스럽게 활용
- 보장·확실·100%·반드시 같은 단정 표현 금지
- **검증 불가능한 구체 수치 절대 사용 금지** (예: "92%가 일치", "전환율 0.3%→4.1%", "이탈률 78%")
- **익명 사례·가공 사례 절대 사용 금지** (예: "한 화장품 브랜드는...", "한 SaaS 스타트업은...")
  → 대신 "자주 보이는 패턴", "실무 관찰상", "현장에서는" 같은 일반화된 표현 사용
- **출처가 명확한 사실만 인용 가능** (예: 구글 공식 알고리즘 이름, 네이버 공식 탭 이름)
  연도·통계는 본인이 확인한 것이 아니라면 인용하지 말 것
- 다양한 문장 길이로 자연스럽게 (AI 양산 패턴 회피)
- 실패 사례·한계·예외 케이스 명시
- 본문 5~7개 H2 섹션, 섹션당 200~400자
- 각 섹션 HTML 사용 (<p>, <ul>, <ol>, <code>, <table>, <strong>)
- 표(<table>)에는 인라인 style 사용하지 말 것 (CSS에서 자동 스타일링됨)

응답 JSON 필드 주의:
- intro: 순수 텍스트만 사용. <p> 태그를 절대 포함하지 말 것 (헬퍼가 자동 감쌈)
- sections 각 값: HTML 사용, <p>로 단락 구분
- title_meta는 "...| OneSearchPro 인사이트" 같은 브랜드 꼬리표 자동 추가됨, 본문 제목만

응답은 **JSON 한 객체만** (다른 설명 없이, 코드블록도 없이):

{{
  "slug": "url-slug-with-hyphens (40자 이내 권장)",
  "title_meta": "<title> 태그 (50-65자, 키워드+브랜드)",
  "desc": "메타 디스크립션 (120-160자, CTA 포함)",
  "keywords": "키워드1, 키워드2, 키워드3, 키워드4, 키워드5",
  "h1": "본문 H1 (제목)",
  "lead": "히어로 리드 문장 (1-2 문장)",
  "intro": "본문 시작 인트로 한 문단 (순수 텍스트, <p> 태그 없음)",
  "sections": [
    ["섹션 H2", "<p>HTML 본문</p>"],
    ["섹션 H2", "<p>HTML 본문</p>"]
  ],
  "key_takeaways": ["요점1", "요점2", "요점3", "요점4"],
  "reading_time": 7
}}

JSON 외 다른 텍스트는 출력하지 마세요."""

    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=8000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    text = msg.content[0].text.strip()
    # Remove code fences if any
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def py_str(value):
    """Escape value for use inside a triple-quoted Python string."""
    if value is None:
        return ""
    return str(value).replace('"""', '\\"\\"\\"')


def py_inline(value):
    """Escape value for use as a single-line double-quoted Python string."""
    if value is None:
        return ""
    s = str(value)
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    s = s.replace("\n", " ")
    return s


def build_entry(article, category_slug, today_iso):
    """Return Python source code for a new PAGES dict entry."""
    slug = article["slug"]
    url_path = f"/insights/{category_slug}/{slug}/"
    full_url = f"https://onesearchpro.org{url_path}"

    sections_repr = ",\n                ".join(
        f'("{py_inline(s[0])}", """{py_str(s[1])}""")' for s in article["sections"]
    )
    takeaways_repr = ",\n                ".join(
        f'"{py_inline(t)}"' for t in article["key_takeaways"]
    )

    category_label_map = {
        "google-seo": "구글 SEO",
        "technical-seo": "기술 SEO",
        "content-seo": "콘텐츠 SEO",
        "local-seo": "지역 SEO",
        "backlink-pr": "백링크 · 디지털 PR",
        "sns": "SNS 마케팅",
        "visibility": "검색 노출 문제 해결",
    }
    category_label = category_label_map.get(category_slug, "")
    eyebrow = category_label.upper() + " · ARTICLE" if category_label else "INSIGHTS · ARTICLE"

    return f'''    "{url_path}": {{
        "title": "{py_inline(article['title_meta'])}",
        "desc": "{py_inline(article['desc'])}",
        "keywords": "{py_inline(article['keywords'])}",
        "h1": "{py_inline(article['h1'])}",
        "eyebrow": "{py_inline(eyebrow)}",
        "lead": "{py_inline(article['lead'])}",
        "body": blog_post(
            date="{today_iso}",
            reading_time={int(article.get('reading_time', 7))},
            intro="""{py_str(article['intro'])}""",
            sections=[
                {sections_repr}
            ],
            key_takeaways=[
                {takeaways_repr}
            ],
            related=[
                ("{py_inline(category_label)} 인사이트 더 보기", "/insights/{category_slug}/", "{py_inline(category_label)}"),
                ("SEO 컨설팅 서비스", "/services/seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="{full_url}",
            title="{py_inline(article['h1'])}",
            desc="{py_inline(article['desc'])}",
            date_published="{today_iso}"
        ),
        "active": "insights",
    }},
'''


def insert_entry_into_build_pages(entry_code):
    """Insert the new article entry before the AUTO-INSERT marker."""
    content = BUILD_PAGES.read_text(encoding="utf-8")
    marker = "    # ===== AUTO-INSERT MARKER (weekly_blog.py inserts new articles above) ====="
    if marker not in content:
        raise RuntimeError("AUTO-INSERT marker not found in build_pages.py")
    new_content = content.replace(marker, entry_code + marker, 1)
    BUILD_PAGES.write_text(new_content, encoding="utf-8")


def append_to_sitemap(article, category_slug):
    slug = article["slug"]
    url = f"https://onesearchpro.org/insights/{category_slug}/{slug}/"
    content = SITEMAP.read_text(encoding="utf-8")
    new_url = f"  <url><loc>{url}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n"
    content = content.replace("</urlset>", new_url + "</urlset>")
    SITEMAP.write_text(content, encoding="utf-8")


def mark_calendar_done(topic, article, category_slug):
    """Mark the topic as [x] in CONTENT_CALENDAR.md and append URL."""
    content = CALENDAR.read_text(encoding="utf-8")
    slug = article["slug"]
    url_path = f"/insights/{category_slug}/{slug}/"
    today = date.today().isoformat()
    new_line = (
        topic["raw_line"]
        .replace("- [ ]", "- [x]", 1)
        + f" → `{url_path}` ({today} 자동 발행)"
    )
    content = content.replace(topic["raw_line"], new_line, 1)
    CALENDAR.write_text(content, encoding="utf-8")


def run_build():
    subprocess.run(
        [sys.executable, "partials/build_pages.py"],
        cwd=ROOT,
        check=True,
    )


def main():
    print("== Weekly Blog Auto-Publish ==")
    topic = find_next_topic()
    if not topic:
        print("No pending topics in CONTENT_CALENDAR.md. Nothing to publish.")
        return 0

    print(f"Next topic: W{topic['week']} [{topic['category']}] {topic['title']}")

    print("Generating article via Claude API...")
    article = generate_article(topic)
    print(f"  slug: {article['slug']}")
    print(f"  title: {article['title_meta'][:60]}...")

    category_slug = topic["category_slug"]
    today_iso = date.today().isoformat()
    entry_code = build_entry(article, category_slug, today_iso)

    print("Inserting entry into build_pages.py...")
    insert_entry_into_build_pages(entry_code)

    print("Updating sitemap.xml...")
    append_to_sitemap(article, category_slug)

    print("Updating CONTENT_CALENDAR.md...")
    mark_calendar_done(topic, article, category_slug)

    print("Running build_pages.py...")
    run_build()

    print(f"\nDone. New article: /insights/{category_slug}/{article['slug']}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Generate remaining service & company pages from a shared template."""
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
SITE = "https://onesearchpro.org"

HEADER = '''<header class="site-header">
    <div class="container nav-wrap">
      <a href="/" class="brand" aria-label="OneSearchPro 홈"><img src="/assets/images/logo.png" alt="OneSearchPro - 검색의 기준을 바꾸다" class="brand-logo" width="180" height="60" /></a>
      <nav class="nav" id="nav">
        <div class="has-dropdown">
          <a href="/services/seo/" class="nav-trigger{ACTIVE_SVC}">서비스 <span class="caret">▾</span></a>
          <div class="dropdown">
            <a href="/services/seo/" class="dd-main"><b>🔍 SEO 컨설팅</b><span>대표 서비스</span></a>
            <a href="/services/technical-seo/">기술 SEO 진단</a>
            <a href="/services/content-seo/">콘텐츠 SEO</a>
            <a href="/services/local-seo/">지역 SEO</a>
            <a href="/services/digital-pr/">디지털 PR · 백링크 진단</a>
            <a href="/services/social-media/">SNS 마케팅</a>
            <a href="/services/web-design/">SEO 웹사이트 제작</a>
          </div>
        </div>
        <div class="has-dropdown">
          <a href="/case-studies/" class="nav-trigger{ACTIVE_CASES}">성공사례 <span class="caret">▾</span></a>
          <div class="dropdown">
            <a href="/case-studies/" class="dd-main"><b>📁 전체 성공사례</b><span>업종별 작업 기록</span></a>
            <a href="/case-studies/seo/">SEO 개선 사례</a>
            <a href="/case-studies/local-seo/">지역 SEO 사례</a>
            <a href="/case-studies/content/">콘텐츠 개선 사례</a>
            <a href="/case-studies/web-design/">웹사이트 제작 사례</a>
            <a href="/case-studies/visibility/">검색 노출 문제 해결 사례</a>
          </div>
        </div>
        <div class="has-dropdown">
          <a href="/insights/" class="nav-trigger{ACTIVE_INSIGHTS}">SEO 인사이트 <span class="caret">▾</span></a>
          <div class="dropdown">
            <a href="/insights/" class="dd-main"><b>📰 전체 글</b><span>SEO 전문 콘텐츠</span></a>
            <a href="/insights/google-seo/">구글 SEO</a>
            <a href="/insights/technical-seo/">기술 SEO</a>
            <a href="/insights/content-seo/">콘텐츠 SEO</a>
            <a href="/insights/local-seo/">지역 SEO</a>
            <a href="/insights/backlink-pr/">백링크 · 디지털 PR</a>
            <a href="/insights/sns/">SNS 마케팅</a>
            <a href="/insights/visibility/">검색 노출 문제 해결</a>
          </div>
        </div>
        <div class="has-dropdown">
          <a href="/about/" class="nav-trigger{ACTIVE_ABOUT}">회사소개 <span class="caret">▾</span></a>
          <div class="dropdown">
            <a href="/about/" class="dd-main"><b>🏢 원서치프로 소개</b><span>About OneSearchPro</span></a>
            <a href="/about/principles/">작업 원칙</a>
            <a href="/about/process/">진행 프로세스</a>
            <a href="/about/faq/">자주 묻는 질문</a>
            <a href="/contact/">문의하기</a>
          </div>
        </div>
        <a href="https://t.me/googleseolab" class="btn btn-ghost" target="_blank" rel="noopener noreferrer">내 사이트 진단받기</a>
      </nav>
      <button class="nav-toggle" id="navToggle" aria-label="메뉴 열기"><span></span><span></span><span></span></button>
    </div>
  </header>'''

FOOTER = '''<footer class="site-footer">
    <div class="container foot-grid">
      <div><a href="/" class="brand"><span class="brand-mark">1</span><span class="brand-name">OneSearch<strong>Pro</strong></span></a><p class="muted">검색에서 시작되는 비즈니스 성장.<br/>SEO · 디지털 마케팅 전문 에이전시.</p></div>
      <div><h5>SEO 서비스</h5><ul><li><a href="/services/seo/">SEO 컨설팅</a></li><li><a href="/services/technical-seo/">기술 SEO 진단</a></li><li><a href="/services/content-seo/">콘텐츠 SEO</a></li><li><a href="/services/local-seo/">지역 SEO</a></li><li><a href="/services/digital-pr/">디지털 PR · 백링크 진단</a></li><li><a href="/services/social-media/">SNS 마케팅</a></li><li><a href="/services/web-design/">SEO 웹사이트 제작</a></li></ul></div>
      <div><h5>회사</h5><ul><li><a href="/case-studies/">성공사례</a></li><li><a href="/insights/">SEO 인사이트</a></li><li><a href="/about/">회사 소개</a></li><li><a href="/contact/">내 사이트 진단받기</a></li></ul></div>
      <div><h5>연락처</h5><ul><li>contact@onesearchpro.com</li><li>Seoul, Korea</li><li>KakaoTalk: @onesearchpro</li></ul></div>
    </div>
    <div class="container foot-bottom"><span>© <span id="year"></span> OneSearchPro. All rights reserved.</span><span>Made with ☕ in Seoul</span></div>
  </footer>'''


def page(*, path, title, desc, keywords, h1, eyebrow, lead, body, json_ld="", active="svc"):
    canonical = f"{SITE}{path}"
    active_svc = " active" if active == "svc" else ""
    active_cases = " active" if active == "cases" else ""
    active_insights = " active" if active == "insights" else ""
    active_about = " active" if active == "about" else ""
    header = (HEADER
        .replace("{ACTIVE_SVC}", active_svc)
        .replace("{ACTIVE_CASES}", active_cases)
        .replace("{ACTIVE_INSIGHTS}", active_insights)
        .replace("{ACTIVE_ABOUT}", active_about))

    is_article = path.startswith("/insights/") and path.strip("/").count("/") >= 2
    body_class = " is-article" if is_article else ""

    if is_article:
        hero_html = f'<section class="article-hero"><div class="container article-hero-inner"><span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lead">{lead}</p></div></section>'
    else:
        hero_html = f'''<section class="page-hero">
      <div class="container page-hero-grid">
        <div>
          <span class="eyebrow">{eyebrow}</span>
          <h1>{h1}</h1>
          <p class="lead">{lead}</p>
          <div class="cta-row">
            <a href="https://t.me/googleseolab" target="_blank" rel="noopener noreferrer" class="btn btn-primary">내 사이트 진단받기</a>
            <a href="/case-studies/" class="btn btn-outline">성공사례 보기 →</a>
          </div>
        </div>
        <div class="page-hero-stats">
          <div><b>1,200+</b><span>구축 백링크</span></div>
          <div><b>180+</b><span>프로젝트</span></div>
          <div><b>97%</b><span>고객 재계약</span></div>
          <div><b>DR 50+</b><span>평균 도메인</span></div>
        </div>
      </div>
    </section>'''

    breadcrumb_html = ""
    if path.startswith("/services/"):
        slug_title = h1
        breadcrumb_html = f'''<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <a href="/services/seo/">서비스</a> <span>›</span> <span>{slug_title}</span></div></nav>'''
    elif path == "/about/":
        breadcrumb_html = '<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <span>회사소개</span></div></nav>'
    elif path.startswith("/about/") and path != "/about/":
        breadcrumb_html = f'<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <a href="/about/">회사소개</a> <span>›</span> <span>{h1}</span></div></nav>'
    elif path == "/contact/":
        breadcrumb_html = '<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <span>내 사이트 진단받기</span></div></nav>'
    elif path == "/case-studies/":
        breadcrumb_html = '<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <span>성공사례</span></div></nav>'
    elif path.startswith("/case-studies/") and path != "/case-studies/":
        breadcrumb_html = f'<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <a href="/case-studies/">성공사례</a> <span>›</span> <span>{h1}</span></div></nav>'
    elif path == "/insights/":
        breadcrumb_html = '<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <span>SEO 인사이트</span></div></nav>'
    elif path.startswith("/insights/") and path != "/insights/":
        breadcrumb_html = f'<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <a href="/insights/">SEO 인사이트</a> <span>›</span> <span>{h1}</span></div></nav>'

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://onesearchpro.org/assets/images/logo.png" />
  <meta property="og:site_name" content="OneSearchPro" />
  <meta property="og:locale" content="ko_KR" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="https://onesearchpro.org/assets/images/logo.png" />
  <link rel="icon" type="image/svg+xml" href="/assets/images/favicon.svg" />
  <link rel="alternate icon" type="image/png" href="/assets/images/logo.png" />
  <link rel="apple-touch-icon" href="/assets/images/logo.png" />
  <meta name="theme-color" content="#7c5cff" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
  {json_ld}
</head>
<body class="{body_class}">
  <div class="reading-progress" id="readingProgress"></div>
  {header}
  {breadcrumb_html}
  <main>
    {hero_html}
    {body}
    <section class="section section-cta">
      <div class="container cta-grid">
        <div><h2>무료 진단 후 정확한 견적을 받아보세요</h2><p>24시간 내 분석 리포트와 맞춤 제안서를 보내드립니다.</p></div>
        <div class="cta-actions"><a href="https://t.me/googleseolab" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-lg">무료 진단 신청 →</a><a href="/case-studies/" class="btn btn-outline btn-lg btn-light">성공사례 보기</a></div>
      </div>
    </section>
  </main>
  {FOOTER}
  <script src="/script.js"></script>
</body>
</html>
'''


def section(eyebrow, h2, p, cards):
    items = ""
    for c in cards:
        ul = ""
        if c.get("li"):
            ul = "<ul>" + "".join(f"<li>{i}</li>" for i in c["li"]) + "</ul>"
        items += f'<div class="svc"><div class="svc-icon">{c["icon"]}</div><h3>{c["h"]}</h3><p>{c["p"]}</p>{ul}</div>'
    return f'''<section class="section">
      <div class="container">
        <div class="section-head"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2><p>{p}</p></div>
        <div class="grid services">{items}</div>
      </div>
    </section>'''


def steps_section(eyebrow, h2, steps):
    items = "".join(f'<li><span class="step-num">{i+1:02d}</span><h4>{s[0]}</h4><p>{s[1]}</p></li>' for i, s in enumerate(steps))
    return f'<section class="section section-soft"><div class="container"><div class="section-head"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2></div><ol class="steps">{items}</ol></div></section>'


def case_card(*, badge, icon, h3, problem, diagnosis, improvements, results, caveats):
    imp_list = "".join(f"<li>{x}</li>" for x in improvements)
    res_list = "".join(f"<li>{x}</li>" for x in results)
    return (
        f'<article class="svc case-card">'
        f'<span class="badge">{badge}</span>'
        f'<div class="svc-icon">{icon}</div>'
        f'<h3>{h3}</h3>'
        f'<h4>작업 전 문제</h4><p>{problem}</p>'
        f'<h4>진단 결과</h4><p>{diagnosis}</p>'
        f'<h4>개선한 항목</h4><ul>{imp_list}</ul>'
        f'<h4>적용 후 변화</h4><ul>{res_list}</ul>'
        f'<h4>주의할 점</h4><p>{caveats}</p>'
        f'</article>'
    )


def cases_section(anchor, eyebrow, h2, intro, cards):
    inner = "".join(cards)
    return (
        f'<section class="section" id="{anchor}"><a id="{anchor}-anchor"></a>'
        f'<div class="container">'
        f'<div class="section-head left"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2><p>{intro}</p></div>'
        f'<div class="grid services case-grid">{inner}</div>'
        f'</div></section>'
    )


def insight_card(title, summary, label="준비 중"):
    return (
        f'<div class="svc insight-card">'
        f'<span class="badge">{label}</span>'
        f'<h3>{title}</h3>'
        f'<p>{summary}</p>'
        f'</div>'
    )


def insight_article_card(title, summary, url, reading_time, label="NEW"):
    return (
        f'<a href="{url}" class="svc insight-article-card">'
        f'<span class="badge">{label}</span>'
        f'<h3>{title}</h3>'
        f'<p>{summary}</p>'
        f'<span class="article-meta-mini">⏱ {reading_time}분 읽기</span>'
        f'<span class="svc-link">읽어보기 →</span>'
        f'</a>'
    )


def insights_section(anchor, eyebrow, h2, intro, cards):
    inner = "".join(cards)
    return (
        f'<section class="section" id="{anchor}"><a id="{anchor}-anchor"></a>'
        f'<div class="container">'
        f'<div class="section-head left"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2><p>{intro}</p></div>'
        f'<div class="grid services">{inner}</div>'
        f'</div></section>'
    )


def blog_post(*, date, reading_time, author="OneSearchPro SEO팀", intro, sections, key_takeaways=None, related=None):
    """블로그 글 본문 HTML을 생성합니다.
    sections: list of (h2, html_content) tuples
    key_takeaways: 글 끝부분에 들어가는 요약 리스트 (optional)
    related: list of (title, url, badge) tuples - 내부 링크용
    """
    meta = (
        f'<div class="article-meta">'
        f'<span>📅 {date}</span>'
        f'<span>⏱ 읽는 시간 약 {reading_time}분</span>'
        f'<span>✍ {author}</span>'
        f'</div>'
    )

    section_html = ""
    for h2_title, content in sections:
        section_html += f'<h2>{h2_title}</h2>\n{content}\n'

    takeaways_html = ""
    if key_takeaways:
        items = "".join(f"<li>{x}</li>" for x in key_takeaways)
        takeaways_html = (
            f'<aside class="article-takeaway">'
            f'<h3>🎯 핵심 정리</h3>'
            f'<ul>{items}</ul>'
            f'</aside>'
        )

    related_html = ""
    if related:
        cards = ""
        for title, url, badge in related:
            cards += (
                f'<a href="{url}" class="svc related-card">'
                f'<span class="badge">{badge}</span>'
                f'<h3>{title}</h3>'
                f'<span class="svc-link">자세히 보기 →</span>'
                f'</a>'
            )
        related_html = (
            f'<section class="section section-soft">'
            f'<div class="container">'
            f'<div class="section-head left">'
            f'<span class="eyebrow">READ NEXT</span>'
            f'<h2>이어서 읽으면 좋은 글</h2>'
            f'<p>같은 주제 또는 연관 분야를 더 자세히 다루는 글입니다. 한 주제를 깊이 이해하는 데 도움이 됩니다.</p>'
            f'</div>'
            f'<div class="grid services">{cards}</div>'
            f'</div></section>'
        )

    cta_html = (
        f'<section class="section">'
        f'<div class="container">'
        f'<div class="article-cta">'
        f'<h3>내 사이트의 SEO 상태가 궁금하다면</h3>'
        f'<p>위 가이드의 항목들을 실제 우리 사이트에 적용하면 어떤 결과가 나올지 궁금하시면, 무료 SEO 진단을 받아보세요. 텔레그램으로 사이트 URL을 보내주시면 24시간 내 분석 리포트를 회신드립니다.</p>'
        f'<a href="https://t.me/googleseolab" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-lg">무료 SEO 진단 받기 →</a>'
        f'</div>'
        f'</div></section>'
    )

    return (
        f'<section class="section article-section">'
        f'<article class="article-body container">'
        f'{meta}'
        f'<p class="article-intro">{intro}</p>'
        f'{section_html}'
        f'{takeaways_html}'
        f'</article>'
        f'</section>'
        f'{cta_html}'
        f'{related_html}'
    )


def blog_jsonld(*, url, title, desc, date_published, date_modified=None):
    date_modified = date_modified or date_published
    return (
        f'<script type="application/ld+json">'
        f'{{"@context":"https://schema.org","@type":"BlogPosting",'
        f'"headline":"{title}",'
        f'"description":"{desc}",'
        f'"url":"{url}",'
        f'"datePublished":"{date_published}",'
        f'"dateModified":"{date_modified}",'
        f'"author":{{"@type":"Organization","name":"OneSearchPro","url":"https://onesearchpro.org/"}},'
        f'"publisher":{{"@type":"Organization","name":"OneSearchPro","logo":{{"@type":"ImageObject","url":"https://onesearchpro.org/assets/images/logo.png"}}}},'
        f'"image":"https://onesearchpro.org/assets/images/logo.png",'
        f'"mainEntityOfPage":{{"@type":"WebPage","@id":"{url}"}},'
        f'"inLanguage":"ko-KR"}}'
        f'</script>'
    )


PAGES = {
    "/services/seo/": {
        "title": "SEO 컨설팅 | 검색 노출 원인 진단·통합 개선 - OneSearchPro",
        "desc": "OneSearchPro의 SEO 컨설팅은 검색 노출이 안 되는 원인을 사이트 구조·콘텐츠·기술 요소까지 통합 진단하고 단계적으로 개선하는 대표 서비스입니다.",
        "keywords": "SEO 컨설팅, SEO 진단, 검색엔진최적화, 구글 SEO, 네이버 SEO, 사이트 진단",
        "h1": "SEO 컨설팅",
        "eyebrow": "SEO CONSULTING",
        "lead": "검색 노출이 안 되는 진짜 이유를 찾는 것에서 시작합니다. 사이트 구조·콘텐츠·기술 요소를 통합 진단하고, 우선순위에 따라 단계적으로 개선하는 OneSearchPro의 대표 서비스입니다.",
        "body": (
            section("AREAS", "통합 SEO 4대 영역",
                    "검색 노출에 필요한 모든 요소를 한 번에 관리합니다.",
                    [
                        {"icon":"🔑","h":"키워드 리서치","p":"상업 의도가 높은 키워드를 발굴하고 난이도·검색량·CPC를 분석합니다.","li":["경쟁사 갭 분석","롱테일 키워드 매핑"]},
                        {"icon":"📄","h":"온페이지 SEO","p":"타이틀, 메타, 헤딩, 내부 링크, 콘텐츠 구조를 검색 의도에 맞춰 최적화.","li":["스키마 마크업","E-E-A-T 강화"]},
                        {"icon":"⚙️","h":"테크니컬 SEO","p":"Core Web Vitals, 크롤링, 색인, 사이트맵, robots.txt까지 기술 SEO 점검.","li":["속도·접근성 개선","구조화 데이터"]},
                        {"icon":"✍️","h":"콘텐츠 전략","p":"검색 의도에 맞는 콘텐츠 기획·작성·운영으로 토픽 권위(Topical Authority) 구축.","li":["콘텐츠 클러스터","월 4~8편 발행"]},
                    ]) +
            steps_section("PROCESS", "SEO 진행 프로세스", [
                ("기술 감사", "사이트 전체를 100+ 항목으로 진단해 우선순위 도출."),
                ("키워드·콘텐츠 플랜", "타겟 키워드와 콘텐츠 캘린더 수립."),
                ("실행 & 빌딩", "온페이지 적용 + 백링크 빌딩 동시 진행."),
                ("리포트 & 개선", "월간 순위·트래픽·전환 리포트, 분기별 전략 조정."),
            ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","serviceType":"SEO","provider":{"@type":"Organization","name":"OneSearchPro"}}</script>',
    },

    "/services/local-seo/": {
        "title": "지역 SEO Local SEO | 구글맵·네이버 플레이스 상위 노출 - OneSearchPro",
        "desc": "OneSearchPro의 지역 SEO는 구글 비즈니스 프로필(GBP), 네이버 플레이스, 지역 디렉토리, 리뷰 관리까지 통합 운영하여 우리 동네 검색 1위를 만듭니다.",
        "keywords": "지역SEO, Local SEO, 구글 비즈니스 프로필, 네이버 플레이스, 지도 SEO, 동네 마케팅",
        "h1": "지역 SEO (Local SEO)",
        "eyebrow": "LOCAL SEO",
        "lead": "오프라인 매장과 지역 기반 서비스를 위한 필수 마케팅. 구글맵·네이버 지도에서 '내 주변 [업종]' 검색 시 가장 먼저 노출되도록 만듭니다.",
        "body": (
            section("CHANNELS", "지역 SEO 핵심 채널",
                    "한국 주요 지역 검색 채널을 통합 운영합니다.",
                    [
                        {"icon":"📍","h":"구글 비즈니스 프로필","p":"GBP 최적화, 카테고리·서비스·사진·게시물 운영, 리뷰 응대.","li":["카테고리·속성 최적화","주간 게시물 운영"]},
                        {"icon":"🗺️","h":"네이버 플레이스","p":"플레이스 정보 최적화, 영수증 리뷰 유도, 톡톡 응대, 스마트플레이스 광고 연계.","li":["블로그·플레이스 연동","리뷰 이벤트 설계"]},
                        {"icon":"📚","h":"지역 디렉토리","p":"국내 주요 비즈니스 디렉토리 등록과 NAP 정보 일관성 관리.","li":["NAP 일관성","로컬 인용(citation)"]},
                        {"icon":"⭐","h":"리뷰 관리","p":"긍정 리뷰 유도 시스템, 부정 리뷰 대응 매뉴얼, 평점 관리.","li":["리뷰 응대 SLA","위기 대응 가이드"]},
                    ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","serviceType":"Local SEO","provider":{"@type":"Organization","name":"OneSearchPro"}}</script>',
    },

    "/services/social-media/": {
        "title": "SNS 마케팅 | 인스타·유튜브·틱톡·네이버 외부 유입 - OneSearchPro",
        "desc": "OneSearchPro의 SNS 마케팅은 인스타그램, 유튜브, 틱톡, 네이버 채널 등 외부 유입과 브랜드 신뢰를 보조하는 채널 운영 서비스입니다.",
        "keywords": "SNS 마케팅, 소셜미디어마케팅, 인스타그램마케팅, 유튜브마케팅, 틱톡마케팅, 네이버 채널",
        "h1": "SNS 마케팅",
        "eyebrow": "SOCIAL MEDIA MARKETING",
        "lead": "브랜드 스토리에 맞는 채널을 찾고, 콘텐츠와 광고를 함께 운영합니다. 팔로워가 아닌 매출로 직결되는 SNS 마케팅을 추구합니다.",
        "body": (
            section("CHANNELS", "운영 채널",
                    "각 채널의 알고리즘과 사용자 특성에 맞게 별도 전략을 수립합니다.",
                    [
                        {"icon":"📷","h":"인스타그램","p":"릴스 중심 콘텐츠, 인플루언서 협업, 쇼핑 태그 활용.","li":["릴스 주 3~5건","스토리·하이라이트 관리"]},
                        {"icon":"👍","h":"페이스북","p":"커뮤니티·이벤트·메타 광고 매니저 기반 정밀 타겟팅.","li":["룩어라이크 타겟팅","리타겟팅 퍼널"]},
                        {"icon":"🎵","h":"틱톡","p":"트렌드 기반 숏폼 콘텐츠, 해시태그 챌린지, TikTok Ads.","li":["UGC 캠페인","Spark Ads 운영"]},
                        {"icon":"▶️","h":"유튜브","p":"숏츠·롱폼 동시 운영, SEO 친화적 메타데이터, 유튜브 광고.","li":["검색·추천 최적화","TrueView 광고"]},
                    ]) +
            section("WORKFLOW", "운영 방식",
                    "기획-제작-광고-분석의 풀사이클을 책임집니다.",
                    [
                        {"icon":"🧠","h":"콘텐츠 기획","p":"월간 콘텐츠 캘린더와 카피 기획."},
                        {"icon":"🎬","h":"제작","p":"숏폼 영상·이미지·카드뉴스 제작 (자체 스튜디오)."},
                        {"icon":"💰","h":"광고 운영","p":"메타·틱톡·구글 광고 통합 운영과 A/B 테스트."},
                        {"icon":"📈","h":"리포트","p":"주간 KPI, 광고 효율(ROAS) 리포트."},
                    ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","serviceType":"Social Media Marketing","provider":{"@type":"Organization","name":"OneSearchPro"}}</script>',
    },

    "/services/corporate-marketing/": {
        "title": "기업 마케팅 | B2B·B2C 통합 퍼포먼스 마케팅 - OneSearchPro",
        "desc": "OneSearchPro의 기업 마케팅은 브랜드 전략, 퍼포먼스 광고, CRM, 콘텐츠 마케팅을 통합한 풀스택 B2B/B2C 마케팅 컨설팅 서비스입니다.",
        "keywords": "기업마케팅, B2B마케팅, B2C마케팅, 퍼포먼스마케팅, 브랜드컨설팅, CRM마케팅",
        "h1": "기업 마케팅",
        "eyebrow": "CORPORATE MARKETING",
        "lead": "단발성 캠페인이 아닌, 분기별 KPI를 기반으로 한 지속 가능한 성장 엔진을 설계합니다. 브랜드부터 퍼포먼스, CRM까지 한 팀이 책임집니다.",
        "body": (
            section("PILLARS", "4대 영역",
                    "기업의 성장 단계에 맞게 우선순위를 조정합니다.",
                    [
                        {"icon":"💎","h":"브랜드 전략","p":"포지셔닝, 비주얼 아이덴티티, 메시지 프레임워크.","li":["브랜드 오디트","톤앤매너 가이드"]},
                        {"icon":"🎯","h":"퍼포먼스 광고","p":"구글·메타·네이버·카카오 통합 운영, 풀퍼널 광고 설계.","li":["퍼널별 광고 분리","UTM·전환 트래킹"]},
                        {"icon":"📨","h":"CRM·이메일 마케팅","p":"고객 세그먼트별 자동화 시나리오, 재구매 유도.","li":["LTV 모델링","리텐션 시퀀스"]},
                        {"icon":"📝","h":"콘텐츠 마케팅","p":"산업 리포트, 케이스 스터디, 블로그 운영.","li":["월 4~8편 발행","리드 마그넷 제작"]},
                    ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","serviceType":"Corporate Marketing","provider":{"@type":"Organization","name":"OneSearchPro"}}</script>',
    },

    "/services/web-design/": {
        "title": "SEO 웹사이트 제작 | 검색엔진 친화 구조로 만드는 사이트 - OneSearchPro",
        "desc": "OneSearchPro의 SEO 웹사이트 제작은 처음부터 검색엔진이 이해하기 쉬운 구조·메타·스키마·속도로 설계하는 사이트 제작 서비스입니다. SEO 기초 공사가 끝난 상태로 납품됩니다.",
        "keywords": "SEO 웹사이트 제작, 홈페이지제작, 랜딩페이지제작, 워드프레스, SEO 최적화 웹사이트, 반응형 웹사이트",
        "h1": "SEO 웹사이트 제작",
        "eyebrow": "SEO-READY WEB DESIGN",
        "lead": "처음부터 검색엔진이 이해하기 쉬운 구조로 설계합니다. SEO·속도·접근성에 최적화된 반응형 사이트로, 운영 단계에서 SEO를 위해 다시 손볼 필요가 없도록 만듭니다.",
        "body": (
            section("TYPES", "제작 유형",
                    "프로젝트 성격에 맞는 기술 스택을 선택합니다.",
                    [
                        {"icon":"🏢","h":"기업 홈페이지","p":"브랜드 소개부터 다국어, 채용까지 — 표준 기업 사이트.","li":["다국어 (KR/EN)","CMS 운영 페이지"]},
                        {"icon":"🚀","h":"랜딩페이지","p":"단일 상품·캠페인용 고전환 랜딩페이지를 3~7일 내 제작.","li":["A/B 테스트 가능","폼·픽셀 연동"]},
                        {"icon":"🛒","h":"쇼핑몰","p":"Shopify, WooCommerce, Cafe24 기반 커머스 구축.","li":["결제·배송 연동","리뷰·재고 자동화"]},
                        {"icon":"📰","h":"콘텐츠/블로그","p":"SEO 친화 구조의 워드프레스·헤드리스 CMS 구축.","li":["스키마 마크업","Core Web Vitals 90+"]},
                    ]) +
            section("INCLUDED", "제작 시 기본 포함 사항", "모든 사이트에 SEO 기초 공사가 포함됩니다.",
                    [
                        {"icon":"⚡","h":"속도 최적화","p":"Core Web Vitals 90점+ 보장."},
                        {"icon":"📱","h":"반응형 디자인","p":"모든 디바이스 완벽 대응."},
                        {"icon":"🔍","h":"SEO 셋업","p":"메타·OG·sitemap·robots·스키마 마크업."},
                        {"icon":"📊","h":"분석 연동","p":"GA4, GTM, 서치콘솔, 픽셀 연동."},
                    ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","serviceType":"Web Design & Development","provider":{"@type":"Organization","name":"OneSearchPro"}}</script>',
    },

    "/about/": {
        "title": "회사 소개 | 원서치프로 - SEO·디지털 마케팅 에이전시",
        "desc": "OneSearchPro는 서울에 거점을 둔 SEO·디지털 마케팅 전문 에이전시입니다. 화이트햇 방식과 투명한 데이터로 180+ 프로젝트를 성공시킨 작업 원칙과 프로세스를 소개합니다.",
        "keywords": "OneSearchPro, 원서치프로, SEO 에이전시, 마케팅 에이전시, 작업 원칙, 진행 프로세스, 서울",
        "h1": "원서치프로 소개",
        "eyebrow": "ABOUT ONESEARCHPRO",
        "lead": "OneSearchPro(원서치프로)는 검색에서 시작되는 비즈니스 성장을 만듭니다. 서울에 거점을 두고 SEO·디지털 마케팅을 제공하며, 단기 트릭이 아닌 정공법으로 검색 자산을 누적시키는 것을 원칙으로 합니다.",
        "body": (
            '<section class="section" id="intro"><div class="container"><div class="section-head"><span class="eyebrow">WHO WE ARE</span><h2>원서치프로는 어떤 에이전시인가요</h2><p>대량 백링크 판매가 아닌, 사이트의 검색 자산을 구조적으로 만드는 SEO 전문 에이전시입니다. 모든 작업은 구글 가이드라인을 준수하는 화이트햇 방식으로만 진행하며, 페널티 사례 0건의 안전성을 유지하고 있습니다.</p></div><div class="grid services"><div class="svc"><div class="svc-icon">🇰🇷</div><h3>서울 기반</h3><p>국내 기업의 구글·네이버 동시 대응을 메인 영역으로 합니다.</p></div><div class="svc"><div class="svc-icon">📈</div><h3>180+ 프로젝트</h3><p>리테일·F&amp;B·뷰티·핀테크·교육 등 산업별 케이스를 축적했습니다.</p></div><div class="svc"><div class="svc-icon">🛡️</div><h3>페널티 0건</h3><p>1,200+ 백링크 빌딩 동안 구글 페널티 사례가 발생하지 않았습니다.</p></div><div class="svc"><div class="svc-icon">🤝</div><h3>97% 재계약률</h3><p>한번 시작한 고객의 97%가 6개월 이상 함께 일하고 있습니다.</p></div></div></div></section>' +

            '<a id="principles"></a>' +
            section("PRINCIPLES", "작업 원칙",
                    "에이전시의 가치는 결국 '신뢰'에서 나온다고 믿습니다.",
                    [
                        {"icon":"✅","h":"화이트햇 원칙","p":"구글 웹마스터 가이드라인을 우선합니다. 단기 트릭, 자동화 도구, 대량 발주 방식은 사용하지 않습니다.","li":["수동 검수 100%","리스크 사전 고지"]},
                        {"icon":"🤝","h":"투명한 공유","p":"모든 백링크 URL, 작업 내역, 키워드 순위 변화, 비용 구조를 고객과 공유합니다.","li":["월간 리포트 발송","대시보드 접근권 제공"]},
                        {"icon":"📊","h":"데이터 기반 의사결정","p":"가설 → 실험 → 측정 → 개선 사이클을 반복합니다. 추정이 아닌 숫자로 보고합니다.","li":["서치콘솔·GA4 연동","A/B 테스트 운영"]},
                        {"icon":"🎯","h":"업종 특화 전략","p":"리테일·F&B·뷰티·핀테크·교육·여행 등 산업별 검색 의도와 경쟁 구도를 분리해 접근합니다.","li":["업종별 케이스북","경쟁사 갭 분석"]},
                        {"icon":"🧭","h":"과장 없는 커뮤니케이션","p":"\"무조건 1위\", \"보장\" 같은 표현은 쓰지 않습니다. 예상 타임라인과 리스크를 사전에 명시합니다.","li":["진단 후 견적 제시","현실적 타임라인"]},
                        {"icon":"♻️","h":"검색 자산 누적","p":"광고를 끄면 사라지는 트래픽이 아니라, 작업을 멈춰도 남는 콘텐츠·링크·평판을 누적시킵니다.","li":["콘텐츠 IP 고객 귀속","링크 자산 분기 점검"]},
                    ]) +

            '<a id="process"></a>' +
            steps_section("PROCESS", "진행 프로세스 (6단계)", [
                ("사이트 진단", "100+ 항목 기술 감사, 현재 키워드 순위, 백링크 프로파일, 경쟁사 갭 분석. 무료 1차 진단 리포트 제공."),
                ("키워드·경쟁 분석", "상업 의도 높은 타겟 키워드 선정, 경쟁사 콘텐츠·링크 패턴 분해, 12개월 키워드 로드맵 수립."),
                ("콘텐츠·구조 설계", "토픽 클러스터 설계, 내부 링크와 헤딩 구조, 스키마 마크업을 검색 의도에 맞춰 재배치."),
                ("기술 SEO 개선", "Core Web Vitals, 색인, sitemap, robots, 중복 URL, canonical 등 코드 레벨 개선 실행."),
                ("외부 신뢰 강화", "디지털 PR, 화이트햇 백링크, 브랜드 언급(citation) 누적으로 도메인·토픽 권위 확보."),
                ("측정·지속 개선", "월간 순위·트래픽·전환 리포트, 분기 전략 리뷰, 6개월 단위 콘텐츠 리프레시."),
            ]) +

            '<section class="section" id="faq-anchor"><a id="faq"></a><div class="container faq-wrap"><div class="section-head left"><span class="eyebrow">FAQ</span><h2>자주 묻는 질문</h2></div><div class="faq">'
            '<details open><summary>SEO 효과는 언제부터 나타나나요?</summary><p>키워드 난이도와 사이트 상태에 따라 다르지만, 일반적으로 온페이지 개선은 4~8주, 외부 신호 누적 효과는 8~16주, 안정적인 상위 노출은 3~6개월 이후입니다. 무료 진단 단계에서 예상 타임라인을 함께 제시합니다.</p></details>'
            '<details><summary>"무조건 구글 1위 보장"이 가능한가요?</summary><p>가능하지 않습니다. 검색 결과는 구글 알고리즘이 결정하며, 어떤 에이전시도 순위를 보장할 수 없습니다. OneSearchPro는 보장 대신 진단 결과와 예상 시나리오, 작업 범위를 사전에 명시합니다.</p></details>'
            '<details><summary>월 비용은 얼마부터 시작하나요?</summary><p>서비스 종류와 사이트 규모에 따라 다릅니다. SEO 컨설팅은 월 단위 리테이너, 기술 SEO 진단은 일회성 진단도 가능합니다. 정확한 견적은 무료 진단 후 사이트 상태에 맞춰 맞춤 제안드립니다.</p></details>'
            '<details><summary>계약 기간은 어떻게 되나요?</summary><p>기본 3개월 단위 계약을 권장하지만, 1~2개월 시범 운영도 가능합니다. SEO는 누적 효과가 핵심이므로 6개월 이상 진행 시 가장 좋은 ROI가 나옵니다.</p></details>'
            '<details><summary>이전 대행사가 사용한 백링크가 위험할 수 있나요?</summary><p>가능합니다. 디지털 PR·백링크 진단 서비스로 기존 백링크를 전수 점검해 스팸·페널티 위험 링크를 식별하고, 필요 시 disavow 작업까지 진행합니다.</p></details>'
            '<details><summary>네이버 SEO도 함께 해주시나요?</summary><p>네. 구글과 네이버는 알고리즘이 다르므로 분리된 전략이 필요합니다. 통합 SEO 컨설팅에는 두 검색엔진 동시 대응이 포함됩니다.</p></details>'
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"AboutPage","name":"­원서치프로 소개","url":"https://onesearchpro.org/about/","mainEntity":{"@type":"Organization","name":"OneSearchPro","alternateName":"원서치프로","url":"https://onesearchpro.org/","description":"SEO·디지털 마케팅 전문 에이전시"}}</script>',
        "active": "about",
    },

    "/services/technical-seo/": {
        "title": "기술 SEO 진단 | 색인·속도·구조화 데이터 점검 - OneSearchPro",
        "desc": "OneSearchPro의 기술 SEO 진단은 색인 문제, robots.txt, sitemap, canonical, Core Web Vitals, 모바일 사용성, 중복 URL, 구조화 데이터까지 100+ 항목을 점검하는 테크니컬 SEO 서비스입니다.",
        "keywords": "기술 SEO, 테크니컬 SEO, 색인 문제, robots.txt, sitemap, canonical, Core Web Vitals, 구조화 데이터, 중복 URL",
        "h1": "기술 SEO 진단",
        "eyebrow": "TECHNICAL SEO AUDIT",
        "lead": "콘텐츠는 충분한데 검색 노출이 안 된다면 대부분 기술적 문제입니다. 색인·속도·구조화 데이터까지 100+ 항목을 점검하고 실제 코드 레벨에서 개선합니다.",
        "body": (
            section("CHECKPOINTS", "기술 SEO 점검 항목",
                    "검색엔진이 사이트를 제대로 읽고 이해할 수 있도록 8개 영역을 점검합니다.",
                    [
                        {"icon":"🔍","h":"색인·크롤링 점검","p":"구글·네이버 색인 여부, 크롤링 차단, noindex 오설정, 페이지 발견성 문제를 진단합니다.","li":["서치콘솔 커버리지 분석","크롤링 예산 점검"]},
                        {"icon":"📄","h":"robots.txt · sitemap","p":"robots.txt 규칙 검증과 XML 사이트맵 구조·우선순위·갱신 주기 최적화.","li":["다중 sitemap 분리","이미지·뉴스 sitemap"]},
                        {"icon":"🔗","h":"canonical · 중복 URL","p":"파라미터·페이지네이션·hreflang으로 인한 중복 콘텐츠와 canonical 누락 해결.","li":["URL 정규화","중복 페이지 통합"]},
                        {"icon":"⚡","h":"Core Web Vitals","p":"LCP, INP, CLS 점수를 실측하고 이미지·CSS·JS·서버 응답을 개선합니다.","li":["이미지 LCP 최적화","JS 번들 분할"]},
                        {"icon":"📱","h":"모바일 사용성","p":"모바일 우선 색인 기준으로 뷰포트, 탭 영역, 가독성을 점검합니다.","li":["모바일 친화성 테스트","터치 타겟 크기"]},
                        {"icon":"🏷️","h":"구조화 데이터","p":"Organization, FAQ, Article, Product 등 검색 결과에 풍부한 결과를 만들어내는 스키마 마크업.","li":["JSON-LD 적용","Rich Results 테스트"]},
                        {"icon":"🌐","h":"HTTPS · 보안","p":"SSL, 혼합 콘텐츠, HSTS, 보안 헤더가 검색 신뢰도에 영향을 줍니다.","li":["혼합 콘텐츠 해결","보안 헤더 설정"]},
                        {"icon":"🧭","h":"내부 링크 구조","p":"앵커텍스트, 깊이, 고립 페이지(orphan)를 점검해 크롤링 효율을 높입니다.","li":["내부 링크 흐름 분석","고립 페이지 연결"]},
                    ]) +
            steps_section("PROCESS", "진단 진행 프로세스", [
                ("초기 스캔", "Screaming Frog, Ahrefs, 서치콘솔로 100+ 항목 자동 스캔."),
                ("수동 검수", "자동 도구가 놓치는 캐싱, 렌더링, JS SEO 이슈를 수동 검수."),
                ("리포트", "심각도별 이슈 분류와 우선순위, 개선 가이드 문서 제공."),
                ("개선 실행", "선택적으로 개발팀 협업 또는 OneSearchPro가 직접 코드 수정."),
            ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","serviceType":"Technical SEO Audit","provider":{"@type":"Organization","name":"OneSearchPro"}}</script>',
    },

    "/services/content-seo/": {
        "title": "콘텐츠 SEO | 키워드·H태그·E-E-A-T 콘텐츠 전략 - OneSearchPro",
        "desc": "OneSearchPro의 콘텐츠 SEO는 키워드 설계, H태그 구조, 검색 의도 분석, E-E-A-T 기반 콘텐츠 개선, 블로그 콘텐츠 전략을 통합 제공하는 SEO 서비스입니다.",
        "keywords": "콘텐츠 SEO, 키워드 설계, H태그 구조, 검색 의도, E-E-A-T, 블로그 SEO, 콘텐츠 전략",
        "h1": "콘텐츠 SEO",
        "eyebrow": "CONTENT SEO",
        "lead": "검색엔진이 신뢰하는 콘텐츠에는 구조가 있습니다. 키워드 설계부터 H태그 계층, 검색 의도 매칭, E-E-A-T 신호까지 — 토픽 권위를 만드는 콘텐츠 전략을 설계합니다.",
        "body": (
            section("PILLARS", "콘텐츠 SEO 5대 축",
                    "단순 글쓰기가 아닌, 검색 자산을 만드는 콘텐츠 전략.",
                    [
                        {"icon":"🔑","h":"키워드 설계","p":"상업 의도·정보 의도·내비게이션 의도를 구분해 단계별 키워드 맵을 만듭니다.","li":["검색량·난이도 분석","롱테일 키워드 발굴"]},
                        {"icon":"🧠","h":"검색 의도 분석","p":"같은 키워드여도 검색 의도가 다릅니다. SERP를 분석해 진짜 원하는 답을 찾아냅니다.","li":["SERP 유형 분류","People Also Ask 분석"]},
                        {"icon":"📐","h":"H태그·페이지 구조","p":"H1~H4의 계층, 내부 링크, 스키마 마크업으로 검색엔진이 콘텐츠를 이해하기 쉽게 만듭니다.","li":["콘텐츠 클러스터 설계","내부 링크 흐름"]},
                        {"icon":"🏆","h":"E-E-A-T 신호 강화","p":"경험(Experience), 전문성, 권위, 신뢰의 4축을 콘텐츠 안에 자연스럽게 녹입니다.","li":["저자 정보 마크업","케이스·실적 인용"]},
                        {"icon":"📅","h":"블로그 콘텐츠 운영","p":"월 4~8편 발행 캘린더, 토픽 클러스터, 콘텐츠 갱신(refresh) 사이클까지 운영합니다.","li":["콘텐츠 캘린더","리프레시 주기 관리"]},
                    ]) +
            steps_section("PROCESS", "콘텐츠 SEO 진행 프로세스", [
                ("토픽 리서치", "비즈니스 핵심 토픽을 정의하고 SERP를 분석해 콘텐츠 갭을 찾습니다."),
                ("클러스터 설계", "필러 콘텐츠 1개 + 클러스터 콘텐츠 6~10개로 토픽 권위 구조 설계."),
                ("작성·발행", "전문 작가가 SEO 가이드라인에 따라 작성, 내부 링크와 스키마까지 적용."),
                ("측정·갱신", "월간 순위·트래픽 측정 후 6개월 주기로 콘텐츠 리프레시."),
            ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","serviceType":"Content SEO","provider":{"@type":"Organization","name":"OneSearchPro"}}</script>',
    },

    "/services/digital-pr/": {
        "title": "디지털 PR · 백링크 진단 | 링크 리스크 점검과 평판 관리 - OneSearchPro",
        "desc": "OneSearchPro의 디지털 PR·백링크 진단은 위험한 링크 식별, 브랜드 언급 추적, 외부 평판 분석, 디지털 PR을 통한 자연스러운 신뢰 신호 확보 서비스입니다.",
        "keywords": "디지털 PR, 백링크 진단, 링크 리스크, 백링크 분석, 브랜드 언급, 외부 평판, 백링크 감사",
        "h1": "디지털 PR · 백링크 진단",
        "eyebrow": "DIGITAL PR & LINK AUDIT",
        "lead": "백링크는 양이 아니라 신뢰가 핵심입니다. 위험한 링크를 걸러내고, 브랜드 언급과 외부 평판을 통해 검색엔진이 자연스럽게 신뢰할 수 있는 신호를 만듭니다.",
        "body": (
            section("FOCUS AREAS", "4대 진단 영역",
                    "대량 백링크 판매가 아닌, 안전성과 신뢰도 중심의 접근.",
                    [
                        {"icon":"🚨","h":"링크 리스크 진단","p":"기존 백링크를 전수 점검해 스팸·페널티 위험 링크를 식별하고 disavow 대상을 분류합니다.","li":["Ahrefs/SEMrush 분석","Toxic Score 평가"]},
                        {"icon":"📣","h":"브랜드 언급 추적","p":"링크 없는 브랜드 언급(unlinked mentions)을 발견해 링크화하고, 신규 언급 기회를 발굴합니다.","li":["언급 모니터링","링크 전환 캠페인"]},
                        {"icon":"🏛️","h":"외부 평판 분석","p":"리뷰·뉴스·커뮤니티에서의 브랜드 신호를 분석해 검색 결과 페이지의 평판을 개선합니다.","li":["SERP 평판 분석","리뷰 신호 관리"]},
                        {"icon":"📰","h":"디지털 PR 캠페인","p":"보도자료, 데이터 리서치, 전문가 인터뷰 등 자연스럽게 신뢰 링크가 따라오는 PR 콘텐츠를 기획합니다.","li":["HARO·전문가 코멘트","오리지널 데이터 리서치"]},
                    ]) +
            steps_section("PROCESS", "진단 진행 프로세스", [
                ("백링크 전수 스캔", "현재 사이트로 향하는 모든 외부 링크 수집과 품질 평가."),
                ("리스크 분류", "안전 / 주의 / 위험 3단계로 분류하고 disavow 후보 정리."),
                ("기회 발굴", "링크 없는 브랜드 언급, 경쟁사 백링크 갭, PR 기회 리스트업."),
                ("실행·모니터링", "선택 캠페인 실행과 분기별 백링크 프로파일 추적."),
            ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","serviceType":"Digital PR and Backlink Audit","provider":{"@type":"Organization","name":"OneSearchPro"}}</script>',
    },

    "/case-studies/": {
        "title": "성공사례 | SEO·검색 노출 개선 작업 기록 - OneSearchPro",
        "desc": "OneSearchPro의 실제 작업 사례 모음. SEO 개선, 지역 SEO, 콘텐츠 개선, 웹사이트 제작, 검색 노출 문제 해결 사례를 작업 전 문제·진단·개선·변화·주의점 5단계로 정리했습니다.",
        "keywords": "SEO 성공사례, 마케팅 사례, 검색 노출 사례, 지역 SEO 사례, 콘텐츠 SEO 사례, 백링크 사례",
        "h1": "성공사례",
        "eyebrow": "CASE STUDIES",
        "lead": "실제 작업 사례를 \"작업 전 문제 / 진단 결과 / 개선한 항목 / 적용 후 변화 / 주의할 점\" 5단계로 공개합니다. 과장된 수치나 \"무조건 1위\" 표현은 쓰지 않으며, 검색엔진 알고리즘 변경에 따른 한계도 함께 명시합니다.",
        "body": (
            cases_section("seo", "SEO IMPROVEMENT", "SEO 개선 사례",
                "사이트 구조·콘텐츠·기술 요소를 통합 개선해 검색 노출이 회복된 사례입니다.",
                [
                    case_card(
                        badge="SAAS · B2B",
                        icon="💼",
                        h3="B2B SaaS — 핵심 키워드 진입 회복",
                        problem="자체 블로그가 있지만 핵심 상업 키워드 검색에서 거의 노출되지 않았고, 경쟁사 대비 도메인 권위가 낮은 상태였습니다.",
                        diagnosis="키워드 매핑이 검색 의도와 어긋나 있었고, 페이지 간 토픽이 분산되어 토픽 권위가 형성되지 않았습니다. 내부 링크도 사실상 없었습니다.",
                        improvements=["필러 페이지 1개 + 클러스터 8개로 토픽 구조 재설계", "타이틀·H1·메타 재작성과 검색 의도 매칭", "내부 링크 흐름 재구성과 앵커텍스트 통일"],
                        results=["타겟 키워드 중 다수가 1~2페이지로 이동", "오가닉 세션 약 2~3배 수준으로 증가", "전체 작업 기간 약 6개월"],
                        caveats="신규 페이지의 경우 색인까지 시간이 걸리며, 동일한 결과가 모든 산업에서 보장되지는 않습니다. 검색 트렌드 변화 시 재조정이 필요합니다."
                    ),
                    case_card(
                        badge="EDU",
                        icon="🎓",
                        h3="온라인 교육 — 카테고리 페이지 재구성",
                        problem="강의 카테고리 페이지가 빈약해서 카테고리 단위 키워드에서 경쟁사보다 뒤로 밀려 있었습니다.",
                        diagnosis="카테고리 페이지에 본문이 거의 없고 H1·H2 구조가 정렬되지 않은 상태였습니다. 또한 panel 검색 의도(\"○○ 강의 비교\")에 맞는 콘텐츠가 없었습니다.",
                        improvements=["카테고리 페이지에 비교·선택 가이드 본문 추가", "스키마 마크업(BreadcrumbList, ItemList) 적용", "내부 링크에서 카테고리로 권위 집중"],
                        results=["카테고리 키워드 평균 노출 순위 개선", "카테고리 페이지 직접 방문 증가", "작업 기간 약 4개월"],
                        caveats="구글의 카테고리·리스트 페이지 평가는 자주 바뀌므로 분기 단위 점검이 필요합니다."
                    ),
                ]
            ) +

            cases_section("local-seo", "LOCAL SEO", "지역 SEO 사례",
                "지역명 + 서비스 키워드, 지도 노출, 지역 기반 검색 유입을 개선한 사례입니다.",
                [
                    case_card(
                        badge="MASSAGE",
                        icon="💆",
                        h3="지역 마사지 전문점 — 6개월간 단계적 개선",
                        problem="네이버 플레이스에 등록은 되어 있었으나, \"지역명 + 마사지\" 검색에서 거의 노출되지 않았고 구글 비즈니스 프로필도 비어 있는 상태였습니다.",
                        diagnosis="NAP(상호·주소·전화) 정보가 채널마다 달랐고, 카테고리 설정·서비스 항목·사진이 부족했습니다. 자체 사이트의 지역 키워드 사용도 거의 없었습니다.",
                        improvements=["NAP 정보 통일과 GBP·플레이스 카테고리 재설정", "지역 랜딩페이지 신설(지역명 + 서비스 페이지 구조)", "지역 디렉토리 인용(citation) 등록과 일관성 확보", "리뷰 응대 매뉴얼과 사진·게시물 주간 운영"],
                        results=["일부 핵심 지역 키워드에서 구글 1페이지 진입", "네이버 플레이스 노출과 예약 문의 증가", "작업 기간 약 6개월"],
                        caveats="지역 검색은 경쟁 매장의 활동성에 따라 순위가 자주 바뀝니다. 작업 종료 후에도 리뷰·게시물 운영이 멈추면 다시 밀려날 수 있습니다."
                    ),
                    case_card(
                        badge="DENTAL",
                        icon="🦷",
                        h3="다지점 치과 — 지점별 지역 랜딩 정비",
                        problem="여러 지점이 있지만 사이트는 본점 정보만 있고, 지점별 검색에서 노출이 되지 않았습니다.",
                        diagnosis="모든 지점이 같은 페이지를 공유해 지역 시그널이 분산되어 있었고, 각 지점의 GBP가 미정비 상태였습니다.",
                        improvements=["지점별 랜딩페이지 분리(지역명·진료 항목 별)", "지점별 GBP 분리 운영과 카테고리·서비스 정비", "지역 리뷰 응대 SLA 수립"],
                        results=["일부 지점에서 \"지역명 + 진료과목\" 검색 노출 회복", "지점 단위 신규 방문 문의 증가", "작업 기간 약 5개월"],
                        caveats="치과·의료 분야는 광고 관련 법규와 의료광고심의 대상 표현을 반드시 사전 검토해야 합니다."
                    ),
                ]
            ) +

            cases_section("content", "CONTENT", "콘텐츠 개선 사례",
                "키워드 설계·H태그·검색 의도·E-E-A-T 신호를 보완해 콘텐츠 자산이 작동하기 시작한 사례입니다.",
                [
                    case_card(
                        badge="MEDIA",
                        icon="📰",
                        h3="라이프스타일 미디어 — 오래된 글 리프레시",
                        problem="과거 글이 많지만 대부분 색인은 되어 있어도 트래픽이 거의 없었습니다.",
                        diagnosis="검색 의도가 변한 키워드를 따라가지 못했고, 본문 길이·이미지·내부 링크가 빈약했습니다. 일부 글은 중복 토픽으로 카니발리제이션 상태였습니다.",
                        improvements=["트래픽 잠재력이 높은 글 50개 선별 후 리프레시", "중복 토픽 통합과 301 리다이렉트 정리", "본문 구조(H2·H3) 재정렬과 내부 링크 재배치"],
                        results=["리프레시 대상 글의 평균 순위 상승", "오가닉 유입 회복 추세 확인", "작업 기간 약 4개월"],
                        caveats="콘텐츠 리프레시 효과는 곧바로 나타나지 않습니다. 색인 재크롤·재평가에 수 주 이상 걸릴 수 있습니다."
                    ),
                    case_card(
                        badge="ECOMMERCE",
                        icon="🛍️",
                        h3="D2C 커머스 — 제품 페이지 SEO 재작성",
                        problem="제품 페이지가 이미지 중심으로만 만들어져 검색엔진이 제품을 이해하지 못했습니다.",
                        diagnosis="제품명·H1·메타·본문이 동일 문구의 반복이었고, 리뷰·FAQ·사양 정보가 구조화되어 있지 않았습니다.",
                        improvements=["제품별 본문(특징·재질·사용법·FAQ) 추가", "Product·FAQ·Review 스키마 적용", "이미지 alt·파일명·이미지맵 sitemap 정비"],
                        results=["롱테일 제품 키워드 노출 증가", "검색 결과의 리치 스니펫(별점·가격) 노출 시작", "작업 기간 약 3개월"],
                        caveats="제품 정보가 자주 바뀌면 sitemap·구조화 데이터를 함께 갱신해야 합니다."
                    ),
                ]
            ) +

            cases_section("web-design", "WEB DESIGN", "웹사이트 제작 사례",
                "처음부터 검색엔진이 이해하기 쉬운 구조로 만든 사이트 제작 사례입니다.",
                [
                    case_card(
                        badge="STARTUP",
                        icon="🚀",
                        h3="스타트업 신규 웹사이트 — SEO 기초 공사 포함 제작",
                        problem="기존 사이트가 외주로 만들어진 디자인 중심 페이지여서 메타·sitemap·스키마가 없는 상태였습니다.",
                        diagnosis="페이지 구조·URL·내부 링크가 검색엔진 친화적이지 않았고, Core Web Vitals 점수가 낮았습니다.",
                        improvements=["정보 구조 재설계(서비스·사례·인사이트 허브 구분)", "Core Web Vitals 90+ 기준으로 코드 최적화", "메타·OG·sitemap·robots·구조화 데이터 셋업", "GA4·서치콘솔·픽셀 연동까지 납품"],
                        results=["런칭 직후부터 색인 정상화", "초기 키워드 노출이 일반 신규 사이트보다 빠르게 형성됨", "제작·셋업 기간 약 6주"],
                        caveats="신규 사이트는 도메인 권위가 낮아 경쟁 키워드 진입까지 추가 시간이 필요합니다. 제작 후 콘텐츠·외부 신호 작업이 이어져야 합니다."
                    ),
                    case_card(
                        badge="B2B",
                        icon="🏗️",
                        h3="B2B 기업 사이트 — 리뉴얼과 URL 마이그레이션",
                        problem="기존 사이트의 URL 구조 변경이 필요했지만 트래픽 손실이 우려되는 상황이었습니다.",
                        diagnosis="기존 페이지 다수가 핵심 키워드에서 노출되고 있어, 잘못된 리다이렉트 시 트래픽 손실 가능성이 컸습니다.",
                        improvements=["기존 URL·키워드·트래픽 매핑 시트 작성", "1:1 301 리다이렉트 매핑과 사전 검증", "출시 직후 서치콘솔로 색인 재요청과 모니터링"],
                        results=["리뉴얼 이후 핵심 키워드 순위 대부분 유지", "오가닉 트래픽 손실 최소화", "프로젝트 기간 약 2개월"],
                        caveats="대규모 마이그레이션은 사전 계획이 부족하면 회복까지 수개월 걸릴 수 있습니다."
                    ),
                ]
            ) +

            cases_section("visibility", "VISIBILITY FIX", "검색 노출 문제 해결 사례",
                "색인·페널티·중복 콘텐츠 등 검색 노출 자체가 막혀 있던 사이트를 정상화한 사례입니다.",
                [
                    case_card(
                        badge="INDEXING",
                        icon="🔍",
                        h3="신규 도메인 — 색인 자체가 안 되던 사이트",
                        problem="런칭 후 몇 달이 지나도 구글 색인에 거의 잡히지 않았습니다.",
                        diagnosis="robots.txt에서 일부 디렉토리가 차단되어 있었고, canonical과 메타 robots noindex가 잘못 설정된 페이지가 다수였습니다.",
                        improvements=["robots.txt 재작성과 차단 규칙 해제", "canonical·noindex 설정 점검과 수정", "sitemap 재생성과 서치콘솔 색인 요청"],
                        results=["주요 페이지 대부분 색인 정상화", "키워드 노출 시작", "작업 기간 약 4주"],
                        caveats="색인 정상화 자체와 상위 노출은 별개입니다. 색인 이후에도 콘텐츠·외부 신호 작업이 필요합니다."
                    ),
                    case_card(
                        badge="DUPLICATE",
                        icon="🧩",
                        h3="대형 쇼핑몰 — 중복 URL 문제 정리",
                        problem="제품 페이지가 옵션·필터·정렬에 따라 수만 개의 중복 URL로 색인되어 크롤링 예산이 낭비되고 있었습니다.",
                        diagnosis="canonical 미설정·중복 메타·중복 콘텐츠가 누적되어 핵심 페이지가 평가받지 못하는 상태였습니다.",
                        improvements=["옵션·필터 파라미터에 대한 canonical 설정", "파라미터별 noindex·meta robots 규칙 정비", "sitemap에서 핵심 페이지만 포함"],
                        results=["크롤링 통계상 핵심 페이지 방문 증가", "중복 색인 페이지 점진적 감소", "작업 기간 약 3개월"],
                        caveats="대규모 색인 정리는 단기 트래픽 변동이 발생할 수 있으며, 분기 단위 추적이 필요합니다."
                    ),
                ]
            )
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"성공사례","url":"https://onesearchpro.org/case-studies/","description":"OneSearchPro의 SEO 작업 사례 모음"}</script>',
        "active": "cases",
    },

    "/insights/": {
        "title": "SEO 인사이트 | 구글·네이버 SEO 전문 콘텐츠 - OneSearchPro",
        "desc": "OneSearchPro의 SEO 인사이트는 구글 SEO, 기술 SEO, 콘텐츠 SEO, 지역 SEO, 백링크·디지털 PR, SNS 마케팅, 검색 노출 문제 해결을 다루는 전문 콘텐츠 허브입니다.",
        "keywords": "SEO 인사이트, 구글 SEO 가이드, 기술 SEO, 콘텐츠 SEO, 지역 SEO, 백링크 가이드, 검색 노출",
        "h1": "SEO 인사이트",
        "eyebrow": "SEO INSIGHTS",
        "lead": "구글·네이버 검색에서 살아남기 위한 실무 가이드 모음. 카테고리별로 다루는 주제와 곧 공개될 글을 미리 확인할 수 있습니다. 콘텐츠는 정기적으로 업데이트되며, 단발성 트렌드보다는 \"오랫동안 유효한 SEO 원칙\"에 가중치를 두고 작성합니다.",
        "body": (
            insights_section("google-seo", "GOOGLE SEO", "구글 SEO",
                "구글 검색 결과 페이지의 작동 원리, 알고리즘 업데이트, E-E-A-T 가이드라인을 다룹니다.",
                [
                    insight_article_card(
                        "구글 코어 업데이트 직후 2주, 절대 손대지 말아야 할 5가지",
                        "트래픽이 흔들릴 때 가장 위험한 건 패닉 작업입니다. 첫 2주에 손대지 말아야 할 5가지와 대신 무엇을 해야 하는지.",
                        "/insights/google-seo/post-core-update-mistakes/",
                        7
                    ),
                    insight_article_card(
                        "Helpful Content System 셀프 점검 — 한국 사이트가 자주 떨어지는 7가지 질문",
                        "HCS는 사이트 전체 평가입니다. 한국 사이트가 셀프 평가에서 자주 떨어지는 패턴과 통과 기준.",
                        "/insights/google-seo/helpful-content-self-check/",
                        8
                    ),
                    insight_card("검색 의도 4가지 유형과 콘텐츠 매칭 전략", "정보형·내비게이션형·상업형·트랜잭션형 의도에 맞는 페이지 유형과 헤딩 구조 가이드."),
                    insight_card("SERP 기능별 노출 전략 — 스니펫·People Also Ask·이미지", "다양한 SERP 기능에 노출되기 위한 콘텐츠 구조와 마크업 가이드.")
                ]
            ) +

            insights_section("technical-seo", "TECHNICAL SEO", "기술 SEO",
                "색인·속도·구조화 데이터·중복 URL 등 기술 요소에 대한 실무 가이드입니다.",
                [
                    insight_article_card(
                        "서치콘솔 \"발견됨 - 현재 색인되지 않음\" 7가지 원인과 진단 순서",
                        "서치콘솔에서 가장 헷갈리는 메시지의 의미와 빈도순 진단법. 7가지 원인을 가장 흔한 것부터 점검.",
                        "/insights/technical-seo/discovered-not-indexed/",
                        9
                    ),
                    insight_article_card(
                        "워드프레스 사이트 LCP 4초 → 1.5초로 줄인 실제 작업 순서",
                        "워드프레스 LCP 90%는 4가지 패턴에서 결정됩니다. 효과 큰 순서로 정리한 작업 매뉴얼.",
                        "/insights/technical-seo/wordpress-lcp-fix/",
                        8
                    ),
                    insight_card("canonical 태그, 언제 어떻게 써야 하나", "파라미터·페이지네이션·다국어·복제 콘텐츠 상황별 canonical 설정 가이드."),
                    insight_card("sitemap.xml 설계 — 큰 사이트는 어떻게 분리해야 하나", "다중 sitemap, 이미지/뉴스/비디오 sitemap, sitemap 인덱스 활용 가이드.")
                ]
            ) +

            insights_section("content-seo", "CONTENT SEO", "콘텐츠 SEO",
                "키워드 설계·H태그·검색 의도·콘텐츠 클러스터링·리프레시 전략을 다룹니다.",
                [
                    insight_article_card(
                        "병원·치과 블로그 첫 100자 — 환자 검색어로 시작해야 하는 이유와 예시",
                        "첫 100자에서 검색 의도 매칭과 메타 디스크립션이 결정됩니다. 의료광고심의 충돌도 피하는 작성법.",
                        "/insights/content-seo/medical-blog-first-100/",
                        7
                    ),
                    insight_article_card(
                        "쇼핑몰 제품 페이지 본문이 비어있을 때 추가하는 6단락 구조",
                        "이미지 위주 제품 페이지가 색인 안 되는 이유와, 본문 6단락으로 롱테일 노출을 늘리는 패턴.",
                        "/insights/content-seo/product-page-content-structure/",
                        8
                    ),
                    insight_card("토픽 클러스터로 토픽 권위(Topical Authority)를 만드는 방법", "필러 콘텐츠 1개 + 클러스터 6~12개의 구조 설계와 내부 링크 흐름 가이드."),
                    insight_card("오래된 글 리프레시 — 새 글보다 효과가 큰 이유", "트래픽 잠재력이 높은 글을 선별하는 기준과 리프레시 작업 순서, 측정 방법.")
                ]
            ) +

            insights_section("local-seo", "LOCAL SEO", "지역 SEO",
                "구글 비즈니스 프로필·네이버 플레이스·지역 랜딩페이지·NAP 일관성 가이드입니다.",
                [
                    insight_article_card(
                        "신규 매장 네이버 플레이스 — 영수증 리뷰 적을 때 첫 3개월 운영 패턴",
                        "리뷰 없는 신규 매장이 빠지는 함정과, 정보·블로그·리뷰 우선순위로 짠 월별 운영 매뉴얼.",
                        "/insights/local-seo/new-store-naver-place/",
                        7
                    ),
                    insight_article_card(
                        "다지점 매장 구글 비즈니스 프로필 — 본사·지점 정보 분리 원칙과 흔한 실수",
                        "본사 정보를 모든 지점에 복붙하면 안 되는 이유. 위치·카테고리·사진·리뷰 응대 4가지 분리 원칙.",
                        "/insights/local-seo/multi-location-gbp/",
                        7
                    ),
                    insight_card("\"지역명 + 서비스\" 키워드용 지역 랜딩페이지 설계법", "다지점 비즈니스에서 지역 키워드를 잡기 위한 페이지 구조와 콘텐츠 작성 가이드."),
                    insight_card("NAP 일관성과 로컬 인용(citation)이 왜 중요한가", "디렉토리·SNS·자체 사이트의 상호·주소·전화 정보 통일 가이드.")
                ]
            ) +

            insights_section("backlink-pr", "BACKLINK & DIGITAL PR", "백링크 · 디지털 PR",
                "안전한 외부 신호 확보, 백링크 리스크 진단, 디지털 PR 전략을 다룹니다.",
                [
                    insight_article_card(
                        "이전 대행사가 남긴 위험한 백링크 — 어디서부터 Disavow 결정해야 하나",
                        "도구 점수의 한계와 즉시·보류·유지 3단계 분류, 단계적 Disavow 제출 전략.",
                        "/insights/backlink-pr/disavow-decision/",
                        9
                    ),
                    insight_article_card(
                        "한국 언론사 보도자료 배포 — 백링크 따라오는 매체와 안 오는 매체 구분법",
                        "본문 링크가 살아남는 매체와 텍스트만 남는 매체의 차이, 브랜드 언급의 가치.",
                        "/insights/backlink-pr/korean-press-release/",
                        7
                    ),
                    insight_card("게스트 포스트와 디지털 PR의 차이", "스팸과 합법적 PR을 가르는 기준, 자연스러운 신뢰 링크 확보 전략."),
                    insight_card("브랜드 언급(unlinked mention)을 링크로 전환하는 방법", "언급 모니터링 도구 활용과 정중한 컨택 템플릿, 전환율 높이는 팁.")
                ]
            ) +

            insights_section("sns", "SNS MARKETING", "SNS 마케팅",
                "인스타그램·유튜브·틱톡·네이버 채널 운영과 SEO 보조 역할에 대한 가이드입니다.",
                [
                    insight_article_card(
                        "유튜브 쇼츠 설명란 — 본 영상 페이지로 트래픽 유도하는 텍스트 구조",
                        "쇼츠 설명란의 첫 줄·본문·해시태그 구조와 외부 사이트 클릭률을 높이는 패턴.",
                        "/insights/sns/youtube-shorts-description/",
                        6
                    ),
                    insight_article_card(
                        "인스타그램 프로필 링크 — 링크인바이오 vs 자체 랜딩, 어느 게 SEO에 도움될까",
                        "두 선택지의 SEO·UX·측정 관점 비교. 비즈니스 단계별 권장 방향.",
                        "/insights/sns/instagram-link-in-bio/",
                        6
                    ),
                    insight_card("SNS는 SEO에 직접 영향을 주는가 — 통념과 사실", "소셜 신호와 검색 순위의 실제 관계, 간접적으로 작용하는 경로 정리."),
                    insight_card("인스타그램 검색 탭과 구글 인덱싱 — 활용 포인트", "프로필·릴스·해시태그를 어떻게 검색 자산으로 만들 수 있는지에 대한 실무 가이드.")
                ]
            ) +

            insights_section("visibility", "VISIBILITY", "검색 노출 문제 해결",
                "색인·페널티·중복·트래픽 급락 등 \"검색 노출이 안 될 때\" 진단 가이드입니다.",
                [
                    insight_article_card(
                        "사이트 리뉴얼 후 트래픽 절반 — 301 리다이렉트 시 자주 빠뜨리는 12가지",
                        "리뉴얼 후 트래픽 손실의 90%는 301 매핑 누락에서. 자주 빠뜨리는 12가지와 모니터링 매뉴얼.",
                        "/insights/visibility/301-migration-mistakes/",
                        8
                    ),
                    insight_article_card(
                        "서치콘솔 \"크롤링됨 - 현재 색인되지 않음\" — 다른 상태와의 차이와 대응법",
                        "구글이 가져갔는데 색인 안 시키는 상태. 5가지 원인과 단계적 개선 방법.",
                        "/insights/visibility/crawled-not-indexed/",
                        8
                    ),
                    insight_card("트래픽이 갑자기 떨어졌을 때 4주 진단 매뉴얼", "코어 업데이트·알고리즘 변경·사이트 문제·계절성을 구분하는 진단 순서."),
                    insight_card("\"수동 조치(manual action)\" 메시지를 받았을 때 대응 가이드", "서치콘솔에서 메시지를 받은 경우 단계별 점검 항목과 재심사 요청 절차.")
                ]
            )
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Blog","name":"SEO 인사이트","url":"https://onesearchpro.org/insights/","description":"구글·네이버 SEO·디지털 마케팅 전문 콘텐츠 허브"}</script>',
        "active": "insights",
    },

    # ========== Case Studies subpages ==========
    "/case-studies/seo/": {
        "title": "SEO 개선 성공사례 | 사이트 구조·콘텐츠·기술 통합 개선 - OneSearchPro",
        "desc": "OneSearchPro의 SEO 개선 사례 모음. 키워드 매핑, 토픽 클러스터, 내부 링크, 스키마 적용까지 통합 작업으로 검색 노출이 회복된 B2B·교육·미디어 프로젝트를 작업 전·진단·개선·변화·주의점 5단계로 기록했습니다.",
        "keywords": "SEO 개선 사례, SEO 성공사례, 검색 노출 회복, 키워드 매핑, 토픽 클러스터, B2B SEO 사례",
        "h1": "SEO 개선 사례",
        "eyebrow": "SEO IMPROVEMENT CASES",
        "lead": "사이트 구조·콘텐츠·기술 요소를 통합 개선해 검색 노출이 회복된 실제 작업 사례입니다. 모든 사례는 \"작업 전 문제 / 진단 결과 / 개선한 항목 / 적용 후 변화 / 주의할 점\" 5단계로 정리했으며, 과장된 수치나 \"무조건 1위\" 표현은 사용하지 않습니다.",
        "body": (
            '<section class="section"><div class="container"><div class="grid services case-grid">' +
            case_card(
                badge="SAAS · B2B",
                icon="💼",
                h3="B2B SaaS — 핵심 키워드 진입 회복",
                problem="자체 블로그가 있지만 핵심 상업 키워드 검색에서 거의 노출되지 않았고, 경쟁사 대비 도메인 권위가 낮은 상태였습니다.",
                diagnosis="키워드 매핑이 검색 의도와 어긋나 있었고, 페이지 간 토픽이 분산되어 토픽 권위가 형성되지 않았습니다. 내부 링크도 사실상 없었습니다.",
                improvements=["필러 페이지 1개 + 클러스터 8개로 토픽 구조 재설계", "타이틀·H1·메타 재작성과 검색 의도 매칭", "내부 링크 흐름 재구성과 앵커텍스트 통일"],
                results=["타겟 키워드 중 다수가 1~2페이지로 이동", "오가닉 세션 약 2~3배 수준으로 증가", "전체 작업 기간 약 6개월"],
                caveats="신규 페이지의 색인까지 시간이 걸리며, 동일한 결과가 모든 산업에서 보장되지는 않습니다. 검색 트렌드 변화 시 재조정이 필요합니다."
            ) +
            case_card(
                badge="EDU",
                icon="🎓",
                h3="온라인 교육 — 카테고리 페이지 재구성",
                problem="강의 카테고리 페이지가 빈약해서 카테고리 단위 키워드에서 경쟁사보다 뒤로 밀려 있었습니다.",
                diagnosis="카테고리 페이지에 본문이 거의 없고 H1·H2 구조가 정렬되지 않은 상태였습니다. 또한 비교형 검색 의도(\"○○ 강의 비교\")에 맞는 콘텐츠가 없었습니다.",
                improvements=["카테고리 페이지에 비교·선택 가이드 본문 추가", "스키마 마크업(BreadcrumbList, ItemList) 적용", "내부 링크에서 카테고리로 권위 집중"],
                results=["카테고리 키워드 평균 노출 순위 개선", "카테고리 페이지 직접 방문 증가", "작업 기간 약 4개월"],
                caveats="구글의 카테고리·리스트 페이지 평가는 자주 바뀌므로 분기 단위 점검이 필요합니다."
            ) +
            case_card(
                badge="MEDIA",
                icon="📰",
                h3="산업 전문 미디어 — 기존 도메인 권위 활용",
                problem="기존 도메인 권위는 있지만, 신규 비즈니스 영역 키워드에서 거의 노출되지 않았습니다.",
                diagnosis="기존 콘텐츠와 신규 비즈니스 키워드 사이에 토픽 연결 고리가 없어 신규 페이지가 평가받지 못했습니다.",
                improvements=["기존 인기 콘텐츠에서 신규 페이지로 내부 링크", "신규 영역 토픽 클러스터 신규 구축", "메타·OG·스키마 일관성 정비"],
                results=["신규 영역 핵심 키워드 색인·노출 시작", "기존 트래픽 손실 없음", "작업 기간 약 5개월"],
                caveats="기존 인기 콘텐츠의 트래픽이 새 페이지로 이동하는 효과는 신중하게 관찰해야 합니다."
            ) +
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"SEO 개선 사례","url":"https://onesearchpro.org/case-studies/seo/","isPartOf":{"@type":"WebSite","name":"OneSearchPro"}}</script>',
        "active": "cases",
    },

    "/case-studies/local-seo/": {
        "title": "지역 SEO 성공사례 | 네이버 플레이스·구글 비즈니스 프로필 - OneSearchPro",
        "desc": "OneSearchPro의 지역 SEO 사례. \"지역명 + 서비스\" 키워드 노출 개선, 구글 비즈니스 프로필·네이버 플레이스 정비, 다지점 매장 지역 랜딩 분리 등 지역 기반 검색 유입을 회복시킨 작업 기록입니다.",
        "keywords": "지역 SEO 사례, 네이버 플레이스 사례, 구글 비즈니스 프로필, 지역 키워드 노출, 마사지 사이트 SEO, 다지점 SEO",
        "h1": "지역 SEO 사례",
        "eyebrow": "LOCAL SEO CASES",
        "lead": "지역명 + 서비스 키워드, 구글맵·네이버 지도 노출, 지역 랜딩페이지 설계 등 지역 기반 검색 유입을 정상화한 실제 작업 사례입니다.",
        "body": (
            '<section class="section"><div class="container"><div class="grid services case-grid">' +
            case_card(
                badge="MASSAGE",
                icon="💆",
                h3="지역 마사지 전문점 — 6개월간 단계적 개선",
                problem="네이버 플레이스에 등록은 되어 있었으나, \"지역명 + 마사지\" 검색에서 거의 노출되지 않았고 구글 비즈니스 프로필도 비어 있는 상태였습니다.",
                diagnosis="NAP(상호·주소·전화) 정보가 채널마다 달랐고, 카테고리 설정·서비스 항목·사진이 부족했습니다. 자체 사이트의 지역 키워드 사용도 거의 없었습니다.",
                improvements=["NAP 정보 통일과 GBP·플레이스 카테고리 재설정", "지역 랜딩페이지 신설(지역명 + 서비스 페이지 구조)", "지역 디렉토리 인용(citation) 등록과 일관성 확보", "리뷰 응대 매뉴얼과 사진·게시물 주간 운영"],
                results=["일부 핵심 지역 키워드에서 구글 1페이지 진입", "네이버 플레이스 노출과 예약 문의 증가", "작업 기간 약 6개월"],
                caveats="지역 검색은 경쟁 매장의 활동성에 따라 순위가 자주 바뀝니다. 작업 종료 후에도 리뷰·게시물 운영이 멈추면 다시 밀려날 수 있습니다."
            ) +
            case_card(
                badge="DENTAL",
                icon="🦷",
                h3="다지점 치과 — 지점별 지역 랜딩 정비",
                problem="여러 지점이 있지만 사이트는 본점 정보만 있고, 지점별 검색에서 노출이 되지 않았습니다.",
                diagnosis="모든 지점이 같은 페이지를 공유해 지역 시그널이 분산되어 있었고, 각 지점의 GBP가 미정비 상태였습니다.",
                improvements=["지점별 랜딩페이지 분리(지역명·진료 항목 별)", "지점별 GBP 분리 운영과 카테고리·서비스 정비", "지역 리뷰 응대 SLA 수립"],
                results=["일부 지점에서 \"지역명 + 진료과목\" 검색 노출 회복", "지점 단위 신규 방문 문의 증가", "작업 기간 약 5개월"],
                caveats="치과·의료 분야는 광고 관련 법규와 의료광고심의 대상 표현을 반드시 사전 검토해야 합니다."
            ) +
            case_card(
                badge="F&B",
                icon="🍱",
                h3="외식 프랜차이즈 — 매장 단위 검색 노출",
                problem="브랜드 검색은 잘 되지만 \"지역 + 음식 종류\" 검색에서는 경쟁 개인 식당에 밀렸습니다.",
                diagnosis="브랜드 페이지에는 지역 키워드가 없었고, 매장 단위 페이지는 PDF·이미지 위주여서 검색엔진이 텍스트를 읽지 못했습니다.",
                improvements=["매장별 텍스트 기반 랜딩페이지 구축", "메뉴·운영시간·예약 정보 스키마 적용", "지역 리뷰 응답 가이드라인 운영"],
                results=["일부 매장 검색에서 노출 회복", "지도 결과 노출 빈도 증가", "작업 기간 약 6개월"],
                caveats="프랜차이즈는 본사·가맹점 간 NAP 일관성과 콘텐츠 중복 관리가 지속적으로 필요합니다."
            ) +
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"지역 SEO 사례","url":"https://onesearchpro.org/case-studies/local-seo/","isPartOf":{"@type":"WebSite","name":"OneSearchPro"}}</script>',
        "active": "cases",
    },

    "/case-studies/content/": {
        "title": "콘텐츠 SEO 개선 사례 | 키워드·구조·E-E-A-T 적용 기록 - OneSearchPro",
        "desc": "OneSearchPro의 콘텐츠 SEO 개선 사례. 오래된 글 리프레시, 제품 페이지 재작성, 검색 의도 매칭, E-E-A-T 신호 강화로 콘텐츠 자산이 다시 작동하기 시작한 실제 작업 기록입니다.",
        "keywords": "콘텐츠 SEO 사례, 콘텐츠 리프레시, 제품 페이지 SEO, E-E-A-T 사례, 검색 의도 매칭",
        "h1": "콘텐츠 개선 사례",
        "eyebrow": "CONTENT IMPROVEMENT CASES",
        "lead": "키워드 설계·H태그·검색 의도·E-E-A-T 신호를 보완해 잠자던 콘텐츠 자산이 다시 트래픽을 만들기 시작한 실제 작업 사례입니다.",
        "body": (
            '<section class="section"><div class="container"><div class="grid services case-grid">' +
            case_card(
                badge="MEDIA",
                icon="📰",
                h3="라이프스타일 미디어 — 오래된 글 리프레시",
                problem="과거 글이 많지만 대부분 색인은 되어 있어도 트래픽이 거의 없었습니다.",
                diagnosis="검색 의도가 변한 키워드를 따라가지 못했고, 본문 길이·이미지·내부 링크가 빈약했습니다. 일부 글은 중복 토픽으로 카니발리제이션 상태였습니다.",
                improvements=["트래픽 잠재력이 높은 글 50개 선별 후 리프레시", "중복 토픽 통합과 301 리다이렉트 정리", "본문 구조(H2·H3) 재정렬과 내부 링크 재배치"],
                results=["리프레시 대상 글의 평균 순위 상승", "오가닉 유입 회복 추세 확인", "작업 기간 약 4개월"],
                caveats="콘텐츠 리프레시 효과는 곧바로 나타나지 않습니다. 색인 재크롤·재평가에 수 주 이상 걸릴 수 있습니다."
            ) +
            case_card(
                badge="ECOMMERCE",
                icon="🛍️",
                h3="D2C 커머스 — 제품 페이지 SEO 재작성",
                problem="제품 페이지가 이미지 중심으로만 만들어져 검색엔진이 제품을 이해하지 못했습니다.",
                diagnosis="제품명·H1·메타·본문이 동일 문구의 반복이었고, 리뷰·FAQ·사양 정보가 구조화되어 있지 않았습니다.",
                improvements=["제품별 본문(특징·재질·사용법·FAQ) 추가", "Product·FAQ·Review 스키마 적용", "이미지 alt·파일명·이미지맵 sitemap 정비"],
                results=["롱테일 제품 키워드 노출 증가", "검색 결과의 리치 스니펫(별점·가격) 노출 시작", "작업 기간 약 3개월"],
                caveats="제품 정보가 자주 바뀌면 sitemap·구조화 데이터를 함께 갱신해야 합니다."
            ) +
            case_card(
                badge="B2B",
                icon="📚",
                h3="전문 컨설팅 — 저자 신뢰도(E-E-A-T) 신호 강화",
                problem="전문성 있는 콘텐츠를 만들고 있지만 검색 노출이 약했습니다.",
                diagnosis="저자 정보가 없고, 사례·인용·출처가 본문에 잘 드러나지 않아 \"누가 쓴 글인지\"에 대한 신호가 부족했습니다.",
                improvements=["저자 페이지·약력 신설과 Author 스키마 적용", "본문 내 실제 사례·출처·인용 보강", "외부 매체 기고로 저자 권위 신호 누적"],
                results=["전문 키워드에서 노출·체류시간 개선", "기고 매체에서 자연 유입 증가", "작업 기간 약 6개월"],
                caveats="E-E-A-T 신호는 빠르게 만들 수 없습니다. 6개월 이상의 누적 작업과 진정성 있는 활동이 필요합니다."
            ) +
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"콘텐츠 개선 사례","url":"https://onesearchpro.org/case-studies/content/","isPartOf":{"@type":"WebSite","name":"OneSearchPro"}}</script>',
        "active": "cases",
    },

    "/case-studies/web-design/": {
        "title": "SEO 웹사이트 제작 사례 | 검색엔진 친화 구조 제작 기록 - OneSearchPro",
        "desc": "OneSearchPro의 SEO 웹사이트 제작 사례. 신규 사이트 SEO 기초 공사, 리뉴얼 시 URL 마이그레이션, Core Web Vitals 최적화 등 처음부터 검색 친화로 만든 제작 기록입니다.",
        "keywords": "SEO 웹사이트 제작 사례, 사이트 리뉴얼, URL 마이그레이션, Core Web Vitals 사례, 신규 사이트 SEO",
        "h1": "웹사이트 제작 사례",
        "eyebrow": "WEB DESIGN CASES",
        "lead": "처음부터 검색엔진이 이해하기 쉬운 구조로 만든 사이트 제작·리뉴얼 사례입니다. 런칭 후 빠른 색인, 트래픽 손실 없는 마이그레이션이 핵심 목표였습니다.",
        "body": (
            '<section class="section"><div class="container"><div class="grid services case-grid">' +
            case_card(
                badge="STARTUP",
                icon="🚀",
                h3="스타트업 신규 웹사이트 — SEO 기초 공사 포함 제작",
                problem="기존 사이트가 외주로 만들어진 디자인 중심 페이지여서 메타·sitemap·스키마가 없는 상태였습니다.",
                diagnosis="페이지 구조·URL·내부 링크가 검색엔진 친화적이지 않았고, Core Web Vitals 점수가 낮았습니다.",
                improvements=["정보 구조 재설계(서비스·사례·인사이트 허브 구분)", "Core Web Vitals 90+ 기준으로 코드 최적화", "메타·OG·sitemap·robots·구조화 데이터 셋업", "GA4·서치콘솔·픽셀 연동까지 납품"],
                results=["런칭 직후부터 색인 정상화", "초기 키워드 노출이 일반 신규 사이트보다 빠르게 형성됨", "제작·셋업 기간 약 6주"],
                caveats="신규 사이트는 도메인 권위가 낮아 경쟁 키워드 진입까지 추가 시간이 필요합니다. 제작 후 콘텐츠·외부 신호 작업이 이어져야 합니다."
            ) +
            case_card(
                badge="B2B",
                icon="🏗️",
                h3="B2B 기업 사이트 — 리뉴얼과 URL 마이그레이션",
                problem="기존 사이트의 URL 구조 변경이 필요했지만 트래픽 손실이 우려되는 상황이었습니다.",
                diagnosis="기존 페이지 다수가 핵심 키워드에서 노출되고 있어, 잘못된 리다이렉트 시 트래픽 손실 가능성이 컸습니다.",
                improvements=["기존 URL·키워드·트래픽 매핑 시트 작성", "1:1 301 리다이렉트 매핑과 사전 검증", "출시 직후 서치콘솔로 색인 재요청과 모니터링"],
                results=["리뉴얼 이후 핵심 키워드 순위 대부분 유지", "오가닉 트래픽 손실 최소화", "프로젝트 기간 약 2개월"],
                caveats="대규모 마이그레이션은 사전 계획이 부족하면 회복까지 수개월 걸릴 수 있습니다."
            ) +
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"웹사이트 제작 사례","url":"https://onesearchpro.org/case-studies/web-design/","isPartOf":{"@type":"WebSite","name":"OneSearchPro"}}</script>',
        "active": "cases",
    },

    "/case-studies/visibility/": {
        "title": "검색 노출 문제 해결 사례 | 색인·페널티·중복 URL - OneSearchPro",
        "desc": "OneSearchPro의 검색 노출 문제 해결 사례. 색인 누락, 페널티, 중복 URL, robots 설정 오류 등 \"검색 노출 자체가 막혀 있던\" 사이트를 정상화한 작업 기록입니다.",
        "keywords": "검색 노출 사례, 색인 문제, 중복 URL, robots 설정, 페널티 회복, 색인 누락",
        "h1": "검색 노출 문제 해결 사례",
        "eyebrow": "VISIBILITY FIX CASES",
        "lead": "색인·페널티·중복 콘텐츠 등 검색 노출 자체가 막혀 있던 사이트를 진단하고 정상화한 실제 작업 사례입니다. 이런 문제는 콘텐츠가 좋아도 검색에 잡히지 않으므로 가장 먼저 해결해야 합니다.",
        "body": (
            '<section class="section"><div class="container"><div class="grid services case-grid">' +
            case_card(
                badge="INDEXING",
                icon="🔍",
                h3="신규 도메인 — 색인 자체가 안 되던 사이트",
                problem="런칭 후 몇 달이 지나도 구글 색인에 거의 잡히지 않았습니다.",
                diagnosis="robots.txt에서 일부 디렉토리가 차단되어 있었고, canonical과 메타 robots noindex가 잘못 설정된 페이지가 다수였습니다.",
                improvements=["robots.txt 재작성과 차단 규칙 해제", "canonical·noindex 설정 점검과 수정", "sitemap 재생성과 서치콘솔 색인 요청"],
                results=["주요 페이지 대부분 색인 정상화", "키워드 노출 시작", "작업 기간 약 4주"],
                caveats="색인 정상화 자체와 상위 노출은 별개입니다. 색인 이후에도 콘텐츠·외부 신호 작업이 필요합니다."
            ) +
            case_card(
                badge="DUPLICATE",
                icon="🧩",
                h3="대형 쇼핑몰 — 중복 URL 문제 정리",
                problem="제품 페이지가 옵션·필터·정렬에 따라 수만 개의 중복 URL로 색인되어 크롤링 예산이 낭비되고 있었습니다.",
                diagnosis="canonical 미설정·중복 메타·중복 콘텐츠가 누적되어 핵심 페이지가 평가받지 못하는 상태였습니다.",
                improvements=["옵션·필터 파라미터에 대한 canonical 설정", "파라미터별 noindex·meta robots 규칙 정비", "sitemap에서 핵심 페이지만 포함"],
                results=["크롤링 통계상 핵심 페이지 방문 증가", "중복 색인 페이지 점진적 감소", "작업 기간 약 3개월"],
                caveats="대규모 색인 정리는 단기 트래픽 변동이 발생할 수 있으며, 분기 단위 추적이 필요합니다."
            ) +
            case_card(
                badge="MANUAL ACTION",
                icon="⚠️",
                h3="중소 비즈니스 — 수동 조치(Manual Action) 회복",
                problem="과거 대량 백링크 작업의 영향으로 서치콘솔에서 수동 조치 메시지를 받은 상태였습니다.",
                diagnosis="위험한 외부 백링크가 다수 식별되었고, 일부 자체 콘텐츠에서도 가이드라인 위반 패턴이 확인되었습니다.",
                improvements=["위험 백링크 식별과 Disavow 파일 제출", "내부 가이드라인 위반 콘텐츠 정비", "서치콘솔 재심사 요청과 결과 모니터링"],
                results=["수동 조치 해제", "기본 검색 노출 복귀", "회복 기간 약 3~4개월"],
                caveats="수동 조치 회복은 자동으로 보장되지 않습니다. 재심사 통과까지 여러 번 시도가 필요할 수 있으며, 회복 후에도 신뢰 회복은 별개입니다."
            ) +
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"검색 노출 문제 해결 사례","url":"https://onesearchpro.org/case-studies/visibility/","isPartOf":{"@type":"WebSite","name":"OneSearchPro"}}</script>',
        "active": "cases",
    },

    # ========== Insights subpages ==========
    "/insights/google-seo/": {
        "title": "구글 SEO 가이드 | E-E-A-T·알고리즘·검색 의도 - OneSearchPro 인사이트",
        "desc": "구글 SEO 실무 가이드 모음. 신규 사이트 시작 체크리스트, E-E-A-T 적용 방법, 코어 업데이트 대응, 검색 의도 분류 등 구글 검색 결과 페이지의 작동 원리를 다룹니다.",
        "keywords": "구글 SEO 가이드, E-E-A-T, 코어 업데이트, 검색 의도, 구글 알고리즘, 구글 SEO 입문",
        "h1": "구글 SEO",
        "eyebrow": "GOOGLE SEO GUIDES",
        "lead": "구글 검색 결과 페이지의 작동 원리, 알고리즘 업데이트, E-E-A-T 가이드라인을 다루는 실무 가이드 모음입니다. 단발성 트렌드보다 오랫동안 유효한 SEO 원칙에 가중치를 두고 작성합니다.",
        "body": (
            '<section class="section"><div class="container"><div class="grid services">' +
            insight_card("구글 SEO 처음 시작할 때 가장 먼저 봐야 할 5가지", "신규 사이트 운영자가 첫 달에 점검해야 할 색인·서치콘솔·메타·내부 링크·핵심 키워드 점검 항목을 정리한 입문 가이드.") +
            insight_card("E-E-A-T란 무엇이고 왜 점점 중요해지는가", "Experience·Expertise·Authoritativeness·Trustworthiness 4가지 신호를 사이트 안에 자연스럽게 녹이는 구체적인 방법.") +
            insight_card("구글 코어 업데이트가 발표됐을 때의 대응 체크리스트", "트래픽 변동이 발생했을 때 \"패닉 작업\" 대신 사용해야 하는 진단 순서와 4주간의 관찰 가이드.") +
            insight_card("검색 의도 4가지 유형과 콘텐츠 매칭 전략", "정보형·내비게이션형·상업형·트랜잭션형 의도에 맞는 페이지 유형과 헤딩 구조 가이드.") +
            insight_card("Helpful Content System — 구글이 평가하는 \"도움이 되는 콘텐츠\"", "구글이 공개한 셀프 평가 질문들을 실제 콘텐츠 점검에 적용하는 방법.") +
            insight_card("SERP 기능별 노출 전략 — 스니펫·People Also Ask·이미지", "다양한 SERP 기능에 노출되기 위한 콘텐츠 구조와 마크업 가이드.") +
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"구글 SEO","url":"https://onesearchpro.org/insights/google-seo/","isPartOf":{"@type":"Blog","name":"SEO 인사이트"}}</script>',
        "active": "insights",
    },

    "/insights/technical-seo/": {
        "title": "기술 SEO 가이드 | 색인·sitemap·Core Web Vitals - OneSearchPro 인사이트",
        "desc": "기술 SEO 실무 가이드. 색인 누락 진단, robots·sitemap·canonical 설정, Core Web Vitals 90+ 만들기, JavaScript SEO 등 테크니컬 영역의 가이드 모음.",
        "keywords": "기술 SEO 가이드, 테크니컬 SEO, Core Web Vitals, 색인 누락, sitemap, canonical, JavaScript SEO",
        "h1": "기술 SEO",
        "eyebrow": "TECHNICAL SEO GUIDES",
        "lead": "색인·속도·구조화 데이터·중복 URL 등 기술 요소에 대한 실무 가이드 모음입니다. 콘텐츠가 충분한데 노출이 안 되는 경우 대부분 이 영역에서 답을 찾을 수 있습니다.",
        "body": (
            '<section class="section"><div class="container"><div class="grid services">' +
            insight_card("페이지가 색인되지 않을 때 확인할 8가지 항목", "robots.txt, noindex, canonical, 크롤링 예산, JavaScript 렌더링 등 색인 실패 원인 진단 순서.") +
            insight_card("Core Web Vitals 점수를 90점 이상으로 끌어올리는 실무 체크리스트", "LCP·INP·CLS 개선을 위한 이미지·CSS·JS·서버 측 작업 가이드.") +
            insight_card("canonical 태그, 언제 어떻게 써야 하나", "파라미터·페이지네이션·다국어·복제 콘텐츠 상황별 canonical 설정 가이드.") +
            insight_card("sitemap.xml 설계 — 큰 사이트는 어떻게 분리해야 하나", "다중 sitemap, 이미지/뉴스/비디오 sitemap, sitemap 인덱스 활용 가이드.") +
            insight_card("JavaScript SEO — SPA·CSR 사이트의 색인 문제", "React/Vue/Next 사이트에서 색인이 어려운 이유와 SSR·prerender 대안.") +
            insight_card("구조화 데이터(JSON-LD) — 어떤 스키마를 적용해야 할까", "Organization, FAQ, Article, Product 등 비즈니스 유형별 적합한 스키마 가이드.") +
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"기술 SEO","url":"https://onesearchpro.org/insights/technical-seo/","isPartOf":{"@type":"Blog","name":"SEO 인사이트"}}</script>',
        "active": "insights",
    },

    "/insights/content-seo/": {
        "title": "콘텐츠 SEO 가이드 | 키워드·H태그·토픽 권위 - OneSearchPro 인사이트",
        "desc": "콘텐츠 SEO 실무 가이드. 키워드 의도 분류, H태그 구조, 토픽 클러스터 설계, 콘텐츠 리프레시 전략 등 검색 자산이 되는 콘텐츠를 만드는 방법.",
        "keywords": "콘텐츠 SEO 가이드, 키워드 리서치, 토픽 클러스터, H태그 구조, 콘텐츠 리프레시, 검색 의도",
        "h1": "콘텐츠 SEO",
        "eyebrow": "CONTENT SEO GUIDES",
        "lead": "키워드 설계·H태그·검색 의도·콘텐츠 클러스터링·리프레시 전략을 다루는 콘텐츠 SEO 실무 가이드 모음입니다.",
        "body": (
            '<section class="section"><div class="container"><div class="grid services">' +
            insight_card("키워드 리서치 — 검색량이 아니라 의도로 분류하는 방법", "검색량 중심 키워드 시트의 한계와 의도 중심 키워드 매핑으로 바꾸는 단계별 가이드.") +
            insight_card("H1·H2·H3 헤딩 구조, SEO에 실제로 얼마나 영향을 주는가", "헤딩 태그의 역할과 자주 하는 실수, 검색 결과 스니펫에 미치는 영향 정리.") +
            insight_card("토픽 클러스터로 토픽 권위(Topical Authority)를 만드는 방법", "필러 콘텐츠 1개 + 클러스터 6~12개의 구조 설계와 내부 링크 흐름 가이드.") +
            insight_card("오래된 글 리프레시 — 새 글보다 효과가 큰 이유", "트래픽 잠재력이 높은 글을 선별하는 기준과 리프레시 작업 순서, 측정 방법.") +
            insight_card("AI 콘텐츠 시대의 SEO — 자동 생성 글은 어디까지 허용되나", "구글의 AI 콘텐츠 정책과 실무에서 안전하게 활용하는 방법.") +
            insight_card("롱폼 vs 숏폼 — 어떤 길이의 글이 SEO에 유리한가", "키워드 유형별 적합 본문 길이와 글 쪼개기·합치기 의사결정 기준.") +
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"콘텐츠 SEO","url":"https://onesearchpro.org/insights/content-seo/","isPartOf":{"@type":"Blog","name":"SEO 인사이트"}}</script>',
        "active": "insights",
    },

    "/insights/local-seo/": {
        "title": "지역 SEO 가이드 | GBP·네이버 플레이스·NAP - OneSearchPro 인사이트",
        "desc": "지역 SEO 실무 가이드. 구글 비즈니스 프로필 최적화, 네이버 플레이스 운영, 지역 랜딩페이지 설계, NAP 일관성 등 지역 기반 검색 유입 가이드 모음.",
        "keywords": "지역 SEO 가이드, 구글 비즈니스 프로필, 네이버 플레이스, 지역 랜딩페이지, NAP 일관성, 로컬 SEO",
        "h1": "지역 SEO",
        "eyebrow": "LOCAL SEO GUIDES",
        "lead": "구글 비즈니스 프로필·네이버 플레이스·지역 랜딩페이지·NAP 일관성을 다루는 지역 SEO 실무 가이드입니다.",
        "body": (
            '<section class="section"><div class="container"><div class="grid services">' +
            insight_card("구글 비즈니스 프로필(GBP) 최적화 체크리스트", "카테고리·서비스·사진·리뷰·게시물 관리에서 자주 빠뜨리는 항목.") +
            insight_card("네이버 플레이스 상위 노출에 영향을 주는 신호들", "스마트플레이스 정보·블로그 연동·영수증 리뷰·톡톡 응대의 우선순위 정리.") +
            insight_card("\"지역명 + 서비스\" 키워드용 지역 랜딩페이지 설계법", "다지점 비즈니스에서 지역 키워드를 잡기 위한 페이지 구조와 콘텐츠 작성 가이드.") +
            insight_card("NAP 일관성과 로컬 인용(citation)이 왜 중요한가", "디렉토리·SNS·자체 사이트의 상호·주소·전화 정보 통일 가이드.") +
            insight_card("리뷰 관리 — 부정 리뷰 대응 매뉴얼", "감정적 대응 없이 검색 신호로 작용할 수 있는 리뷰 응답 템플릿과 절차.") +
            insight_card("지역 SEO와 일반 SEO의 우선순위 차이", "오프라인 매장과 온라인 비즈니스의 SEO 작업 순서 차이 가이드.") +
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"지역 SEO","url":"https://onesearchpro.org/insights/local-seo/","isPartOf":{"@type":"Blog","name":"SEO 인사이트"}}</script>',
        "active": "insights",
    },

    "/insights/backlink-pr/": {
        "title": "백링크·디지털 PR 가이드 | 링크 리스크·평판 관리 - OneSearchPro 인사이트",
        "desc": "안전한 외부 신호 확보 가이드. 백링크 리스크 진단, Disavow 활용, 디지털 PR과 게스트 포스트의 차이, 브랜드 언급 링크 전환 등 외부 신뢰 신호 가이드.",
        "keywords": "백링크 가이드, 디지털 PR, Disavow, 백링크 리스크, 브랜드 언급, 외부 신뢰 신호",
        "h1": "백링크 · 디지털 PR",
        "eyebrow": "BACKLINK & DIGITAL PR GUIDES",
        "lead": "안전한 외부 신호 확보, 백링크 리스크 진단, 디지털 PR 전략을 다루는 가이드입니다. 양이 아닌 신뢰가 핵심인 접근법을 다룹니다.",
        "body": (
            '<section class="section"><div class="container"><div class="grid services">' +
            insight_card("위험한 백링크를 식별하는 7가지 지표", "Toxic Score·앵커 분포·발신 사이트 품질·언어·지역 시그널 등 점검 항목.") +
            insight_card("Google Disavow 도구 — 언제 써야 하고 언제 쓰지 말아야 하나", "Disavow의 실제 효과와 잘못된 사용으로 인한 위험, 단계적 의사결정 가이드.") +
            insight_card("게스트 포스트와 디지털 PR의 차이", "스팸과 합법적 PR을 가르는 기준, 자연스러운 신뢰 링크 확보 전략.") +
            insight_card("브랜드 언급(unlinked mention)을 링크로 전환하는 방법", "언급 모니터링 도구 활용과 정중한 컨택 템플릿, 전환율 높이는 팁.") +
            insight_card("디지털 PR 캠페인 — 데이터 리서치·전문가 인터뷰 활용", "자연스럽게 언론 인용이 따라오는 콘텐츠 기획 패턴.") +
            insight_card("백링크 프로파일 점검 주기와 모니터링 도구 비교", "Ahrefs·SEMrush·Majestic 등 도구별 강점과 분기 점검 루틴.") +
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"백링크 · 디지털 PR","url":"https://onesearchpro.org/insights/backlink-pr/","isPartOf":{"@type":"Blog","name":"SEO 인사이트"}}</script>',
        "active": "insights",
    },

    "/insights/sns/": {
        "title": "SNS 마케팅 가이드 | 인스타·유튜브·틱톡 SEO 보조 - OneSearchPro 인사이트",
        "desc": "SNS 마케팅과 SEO의 관계를 다루는 가이드. 소셜 신호가 SEO에 미치는 영향, 유튜브 SEO, 인스타그램 검색 활용 등 외부 유입과 브랜드 신뢰 보조 전략.",
        "keywords": "SNS 마케팅 가이드, 유튜브 SEO, 인스타그램 SEO, 소셜 신호, 외부 유입, SNS와 SEO",
        "h1": "SNS 마케팅",
        "eyebrow": "SOCIAL MEDIA GUIDES",
        "lead": "인스타그램·유튜브·틱톡·네이버 채널이 SEO에 어떻게 작용하는지, 외부 유입과 브랜드 신뢰를 보조하는 방법을 다루는 가이드입니다.",
        "body": (
            '<section class="section"><div class="container"><div class="grid services">' +
            insight_card("SNS는 SEO에 직접 영향을 주는가 — 통념과 사실", "소셜 신호와 검색 순위의 실제 관계, 간접적으로 작용하는 경로 정리.") +
            insight_card("유튜브 SEO 기본 — 제목·설명·태그·썸네일의 우선순위", "유튜브 알고리즘이 평가하는 요소와 콘텐츠 갱신 주기 가이드.") +
            insight_card("인스타그램 검색 탭과 구글 인덱싱 — 활용 포인트", "프로필·릴스·해시태그를 어떻게 검색 자산으로 만들 수 있는지에 대한 실무 가이드.") +
            insight_card("틱톡·쇼츠 — 짧은 영상이 SEO를 어떻게 보조하나", "숏폼 콘텐츠와 웹사이트 유입을 연결하는 운영 가이드.") +
            insight_card("네이버 블로그·카페·인플루언서 마케팅 — SEO 보조 전략", "네이버 생태계에서 검색 신호로 연결되는 운영 패턴 정리.") +
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"SNS 마케팅","url":"https://onesearchpro.org/insights/sns/","isPartOf":{"@type":"Blog","name":"SEO 인사이트"}}</script>',
        "active": "insights",
    },

    "/insights/visibility/": {
        "title": "검색 노출 문제 해결 가이드 | 색인 누락·트래픽 급락 진단 - OneSearchPro 인사이트",
        "desc": "검색 노출 문제 진단 가이드. 색인 누락 진단, 트래픽 급락 4주 매뉴얼, 수동 조치 회복, 중복 콘텐츠 정리 등 \"검색 노출이 안 될 때\" 점검할 항목 모음.",
        "keywords": "검색 노출 진단, 색인 누락, 트래픽 급락, 수동 조치, 중복 콘텐츠, 페널티 회복",
        "h1": "검색 노출 문제 해결",
        "eyebrow": "VISIBILITY TROUBLESHOOTING",
        "lead": "색인·페널티·중복·트래픽 급락 등 \"검색 노출이 안 될 때\" 단계적으로 진단하는 가이드 모음입니다.",
        "body": (
            '<section class="section"><div class="container"><div class="grid services">' +
            insight_card("트래픽이 갑자기 떨어졌을 때 4주 진단 매뉴얼", "코어 업데이트·알고리즘 변경·사이트 문제·계절성을 구분하는 진단 순서.") +
            insight_card("색인 누락 원인 7가지와 단계별 진단 방법", "Crawl·Render·Index 3단계에서 일어날 수 있는 실패 패턴 분류.") +
            insight_card("\"수동 조치(manual action)\" 메시지를 받았을 때 대응 가이드", "서치콘솔에서 메시지를 받은 경우 단계별 점검 항목과 재심사 요청 절차.") +
            insight_card("중복 콘텐츠 문제 — canonical, 301, noindex 중 어떤 걸 써야 하나", "상황별 의사결정 트리와 실제 사례 기반 가이드.") +
            insight_card("서치콘솔 \"발견됨 - 현재 색인되지 않음\" 해석법", "구글이 발견은 했지만 색인 안 한 이유를 분류하는 방법.") +
            insight_card("크롤링 예산이 부족한 사이트 — 우선순위 정리법", "큰 사이트에서 핵심 페이지로 크롤러를 집중시키는 구조 설계 가이드.") +
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"검색 노출 문제 해결","url":"https://onesearchpro.org/insights/visibility/","isPartOf":{"@type":"Blog","name":"SEO 인사이트"}}</script>',
        "active": "insights",
    },

    # ========== About subpages ==========
    "/about/principles/": {
        "title": "작업 원칙 | OneSearchPro의 화이트햇 SEO 원칙 6가지",
        "desc": "OneSearchPro가 모든 프로젝트에서 지키는 6가지 작업 원칙. 화이트햇·투명한 공유·데이터 기반·업종 특화·과장 없는 커뮤니케이션·검색 자산 누적을 통한 신뢰 기반 SEO 작업 방식.",
        "keywords": "OneSearchPro 작업 원칙, 화이트햇 SEO, 투명한 SEO, 데이터 기반 마케팅, SEO 윤리",
        "h1": "작업 원칙",
        "eyebrow": "OUR PRINCIPLES",
        "lead": "에이전시의 가치는 결국 \"신뢰\"에서 나온다고 믿습니다. OneSearchPro가 모든 프로젝트에서 양보하지 않는 6가지 작업 원칙입니다.",
        "body": (
            section("PRINCIPLES", "OneSearchPro 6대 원칙",
                "단기 트릭이 아닌 정공법으로 일하는 이유.",
                [
                    {"icon":"✅","h":"화이트햇 원칙","p":"구글 웹마스터 가이드라인을 우선합니다. 단기 트릭, 자동화 도구, 대량 발주 방식은 사용하지 않습니다.","li":["수동 검수 100%","리스크 사전 고지"]},
                    {"icon":"🤝","h":"투명한 공유","p":"모든 백링크 URL, 작업 내역, 키워드 순위 변화, 비용 구조를 고객과 공유합니다.","li":["월간 리포트 발송","대시보드 접근권 제공"]},
                    {"icon":"📊","h":"데이터 기반 의사결정","p":"가설 → 실험 → 측정 → 개선 사이클을 반복합니다. 추정이 아닌 숫자로 보고합니다.","li":["서치콘솔·GA4 연동","A/B 테스트 운영"]},
                    {"icon":"🎯","h":"업종 특화 전략","p":"리테일·F&B·뷰티·핀테크·교육·여행 등 산업별 검색 의도와 경쟁 구도를 분리해 접근합니다.","li":["업종별 케이스북","경쟁사 갭 분석"]},
                    {"icon":"🧭","h":"과장 없는 커뮤니케이션","p":"\"무조건 1위\", \"보장\" 같은 표현은 쓰지 않습니다. 예상 타임라인과 리스크를 사전에 명시합니다.","li":["진단 후 견적 제시","현실적 타임라인"]},
                    {"icon":"♻️","h":"검색 자산 누적","p":"광고를 끄면 사라지는 트래픽이 아니라, 작업을 멈춰도 남는 콘텐츠·링크·평판을 누적시킵니다.","li":["콘텐츠 IP 고객 귀속","링크 자산 분기 점검"]},
                ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"AboutPage","name":"OneSearchPro 작업 원칙","url":"https://onesearchpro.org/about/principles/","isPartOf":{"@type":"WebSite","name":"OneSearchPro"}}</script>',
        "active": "about",
    },

    "/about/process/": {
        "title": "진행 프로세스 | OneSearchPro 6단계 SEO 작업 방식",
        "desc": "OneSearchPro의 6단계 SEO 작업 프로세스. 사이트 진단 → 키워드 분석 → 콘텐츠 설계 → 기술 SEO 개선 → 외부 신뢰 강화 → 측정과 지속 개선까지 동일한 사이클로 운영합니다.",
        "keywords": "SEO 작업 프로세스, OneSearchPro 진행 방식, SEO 단계, SEO 진단, SEO 컨설팅 프로세스",
        "h1": "진행 프로세스",
        "eyebrow": "OUR PROCESS",
        "lead": "모든 프로젝트는 동일한 진단·실행·측정 사이클로 진행됩니다. 단계마다 명확한 산출물이 있어 작업이 객관적으로 추적됩니다.",
        "body": (
            steps_section("PROCESS", "6단계 SEO 작업 프로세스", [
                ("사이트 진단", "100+ 항목 기술 감사, 현재 키워드 순위, 백링크 프로파일, 경쟁사 갭 분석. 무료 1차 진단 리포트 제공."),
                ("키워드·경쟁 분석", "상업 의도 높은 타겟 키워드 선정, 경쟁사 콘텐츠·링크 패턴 분해, 12개월 키워드 로드맵 수립."),
                ("콘텐츠·구조 설계", "토픽 클러스터 설계, 내부 링크와 헤딩 구조, 스키마 마크업을 검색 의도에 맞춰 재배치."),
                ("기술 SEO 개선", "Core Web Vitals, 색인, sitemap, robots, 중복 URL, canonical 등 코드 레벨 개선 실행."),
                ("외부 신뢰 강화", "디지털 PR, 화이트햇 백링크, 브랜드 언급(citation) 누적으로 도메인·토픽 권위 확보."),
                ("측정·지속 개선", "월간 순위·트래픽·전환 리포트, 분기 전략 리뷰, 6개월 단위 콘텐츠 리프레시."),
            ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"AboutPage","name":"OneSearchPro 진행 프로세스","url":"https://onesearchpro.org/about/process/","isPartOf":{"@type":"WebSite","name":"OneSearchPro"}}</script>',
        "active": "about",
    },

    "/about/faq/": {
        "title": "자주 묻는 질문 | OneSearchPro SEO 컨설팅 FAQ",
        "desc": "OneSearchPro SEO 컨설팅에 대해 자주 받는 질문 정리. 효과 시점, 보장 가능 여부, 비용 구조, 계약 기간, 기존 백링크 위험, 네이버 SEO 등 실무 질문에 정직하게 답합니다.",
        "keywords": "SEO 컨설팅 FAQ, OneSearchPro 자주 묻는 질문, SEO 효과 기간, SEO 비용, 네이버 SEO, SEO 계약",
        "h1": "자주 묻는 질문",
        "eyebrow": "FREQUENTLY ASKED QUESTIONS",
        "lead": "SEO 컨설팅을 검토하시는 분들이 자주 묻는 질문을 정리했습니다. 보장 표현 대신 현실적인 답변을 드립니다.",
        "body": (
            '<section class="section"><div class="container faq-wrap"><div class="section-head left"><span class="eyebrow">FAQ</span><h2>SEO 컨설팅에 대해 자주 묻는 질문</h2></div><div class="faq">'
            '<details open><summary>SEO 효과는 언제부터 나타나나요?</summary><p>키워드 난이도와 사이트 상태에 따라 다르지만, 일반적으로 온페이지 개선은 4~8주, 외부 신호 누적 효과는 8~16주, 안정적인 상위 노출은 3~6개월 이후입니다. 무료 진단 단계에서 예상 타임라인을 함께 제시합니다.</p></details>'
            '<details><summary>"무조건 구글 1위 보장"이 가능한가요?</summary><p>가능하지 않습니다. 검색 결과는 구글 알고리즘이 결정하며, 어떤 에이전시도 순위를 보장할 수 없습니다. OneSearchPro는 보장 대신 진단 결과와 예상 시나리오, 작업 범위를 사전에 명시합니다.</p></details>'
            '<details><summary>월 비용은 얼마부터 시작하나요?</summary><p>서비스 종류와 사이트 규모에 따라 다릅니다. SEO 컨설팅은 월 단위 리테이너, 기술 SEO 진단은 일회성 진단도 가능합니다. 정확한 견적은 무료 진단 후 사이트 상태에 맞춰 맞춤 제안드립니다.</p></details>'
            '<details><summary>계약 기간은 어떻게 되나요?</summary><p>기본 3개월 단위 계약을 권장하지만, 1~2개월 시범 운영도 가능합니다. SEO는 누적 효과가 핵심이므로 6개월 이상 진행 시 가장 좋은 ROI가 나옵니다.</p></details>'
            '<details><summary>이전 대행사가 사용한 백링크가 위험할 수 있나요?</summary><p>가능합니다. 디지털 PR·백링크 진단 서비스로 기존 백링크를 전수 점검해 스팸·페널티 위험 링크를 식별하고, 필요 시 disavow 작업까지 진행합니다.</p></details>'
            '<details><summary>네이버 SEO도 함께 해주시나요?</summary><p>네. 구글과 네이버는 알고리즘이 다르므로 분리된 전략이 필요합니다. 통합 SEO 컨설팅에는 두 검색엔진 동시 대응이 포함됩니다.</p></details>'
            '<details><summary>이미 사이트가 운영 중인데 처음부터 새로 만들어야 하나요?</summary><p>대부분 그럴 필요는 없습니다. 기존 사이트의 SEO 자산(도메인 권위, 색인된 페이지)을 유지하면서 단계적으로 개선하는 것이 일반적이며, 구조적 문제가 심각할 때만 리뉴얼을 권장합니다.</p></details>'
            '<details><summary>광고는 같이 운영해야 하나요?</summary><p>필수는 아니지만 초기에 데이터를 빠르게 수집하기 위해 일부 광고와 병행하는 것을 권장하기도 합니다. SEO 자산이 누적된 후에는 광고 의존도를 줄일 수 있습니다.</p></details>'
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"SEO 효과는 언제부터 나타나나요?","acceptedAnswer":{"@type":"Answer","text":"키워드 난이도와 사이트 상태에 따라 다르지만, 일반적으로 온페이지 개선은 4~8주, 외부 신호 누적 효과는 8~16주, 안정적인 상위 노출은 3~6개월 이후입니다."}},{"@type":"Question","name":"무조건 구글 1위 보장이 가능한가요?","acceptedAnswer":{"@type":"Answer","text":"가능하지 않습니다. 검색 결과는 구글 알고리즘이 결정하며, 어떤 에이전시도 순위를 보장할 수 없습니다."}},{"@type":"Question","name":"월 비용은 얼마부터 시작하나요?","acceptedAnswer":{"@type":"Answer","text":"서비스 종류와 사이트 규모에 따라 다릅니다. 정확한 견적은 무료 진단 후 맞춤 제안드립니다."}},{"@type":"Question","name":"계약 기간은 어떻게 되나요?","acceptedAnswer":{"@type":"Answer","text":"기본 3개월 단위 계약을 권장하지만 1~2개월 시범 운영도 가능합니다."}},{"@type":"Question","name":"네이버 SEO도 함께 해주시나요?","acceptedAnswer":{"@type":"Answer","text":"네. 통합 SEO 컨설팅에는 구글과 네이버 동시 대응이 포함됩니다."}}]}</script>',
        "active": "about",
    },

    # ===================== BLOG ARTICLES =====================
    # Google SEO category
    "/insights/google-seo/post-core-update-mistakes/": {
        "title": "구글 코어 업데이트 직후 2주, 절대 손대지 말아야 할 5가지 | OneSearchPro 인사이트",
        "desc": "코어 업데이트 발표 후 트래픽이 흔들릴 때 가장 위험한 건 패닉 작업입니다. 첫 2주간 손대지 말아야 할 5가지와 그 이유, 그리고 대신 무엇을 해야 하는지 정리합니다.",
        "keywords": "구글 코어 업데이트, core update, 트래픽 급락, SEO 패닉, 코어 업데이트 대응",
        "h1": "구글 코어 업데이트 직후 2주, 절대 손대지 말아야 할 5가지",
        "eyebrow": "GOOGLE SEO · ARTICLE",
        "lead": "코어 업데이트 후 트래픽이 흔들릴 때 가장 위험한 건 \"뭐라도 해야 할 것 같다\"는 충동입니다. 첫 2주에 손대지 말아야 할 5가지와 그 대신 해야 할 일을 실무 관점에서 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=7,
            intro="구글이 코어 업데이트를 발표한 직후 가장 흔한 실수는 \"가만히 있기\"가 어렵다는 점에서 나옵니다. 트래픽 그래프가 떨어지는 걸 보면서 아무것도 안 하기란 쉽지 않습니다. 그런데 데이터가 안정되기 전에 손을 대면 진짜 원인이 무엇이었는지조차 영영 알 수 없게 됩니다.",
            sections=[
                ("왜 \"기다리기\"가 가장 어려운 작업인가",
                 "<p>코어 업데이트는 보통 7~14일에 걸쳐 단계적으로 롤아웃됩니다. 첫 며칠의 변동은 최종 결과가 아닙니다. 14일째 다시 보면 원래대로 돌아와 있는 경우도 많습니다.</p>"
                 "<p>그런데 이 기간에 콘텐츠를 대거 수정하거나 새 백링크를 발주하면 두 가지 문제가 생깁니다. 첫째, 변수가 섞여서 코어 업데이트의 영향만 분리할 수 없습니다. 둘째, 다음 작업의 효과 측정 기준선이 사라집니다. 진단도 못 하고 측정도 못 합니다.</p>"),
                ("손대지 말 것 1·2 — 콘텐츠 대량 수정, 디자인 리뉴얼",
                 "<p>가장 흔한 패닉 반응이 \"콘텐츠를 갈아엎자\"입니다. 그런데 코어 업데이트 직후의 콘텐츠 수정은 거의 항상 손해가 더 큽니다. 이미 평가받은 페이지를 무리하게 바꾸면 재평가 사이클이 다시 시작되고, 회복이 더 느려집니다.</p>"
                 "<p>디자인 리뉴얼도 마찬가지입니다. URL 구조, 내부 링크, 페이지 속도가 함께 바뀌면 트래픽 변동의 원인을 더 이상 알 수 없습니다. 리뉴얼이 정말 필요하다면 코어 업데이트 영향이 안정된 후로 미루세요.</p>"),
                ("손대지 말 것 3·4 — Disavow 신규 제출, 페이지 대량 삭제",
                 "<p>\"백링크가 문제일 것 같다\"는 가설로 Disavow 파일을 급하게 제출하는 경우가 있는데, 코어 업데이트는 보통 백링크 자체보다 콘텐츠 품질·E-E-A-T 신호를 본다는 게 구글의 공식 입장입니다. 위험하지 않은 링크를 disavow하면 오히려 손해입니다.</p>"
                 "<p>트래픽이 없는 페이지를 대량 삭제하는 것도 위험합니다. 일부는 검색량은 적어도 토픽 권위에 기여하고 있을 수 있습니다. 삭제는 항상 \"개별 페이지 단위 검토\" 후에 진행해야 합니다.</p>"),
                ("손대지 말 것 5 — 새 SEO 도구·플러그인 도입",
                 "<p>패닉 상태에서 새 SEO 플러그인을 깔거나 캐싱·CDN 설정을 바꾸는 경우가 자주 보입니다. 사이트가 흔들리는 시점에 추가 변수를 더하면 진단이 사실상 불가능해집니다.</p>"
                 "<p>실무에서 본 경우, 코어 업데이트 직후 새 캐싱 플러그인을 도입했다가 모바일 LCP가 망가져서 \"코어 업데이트 영향\"과 \"기술 SEO 후퇴\"가 동시에 일어난 사이트가 있었습니다. 회복까지 3개월 걸렸습니다.</p>"),
                ("그럼 무엇을 해야 하나 — 4주 관찰 매뉴얼",
                 "<p>대신 권장하는 작업은 \"기록과 관찰\"입니다.</p>"
                 "<ul>"
                 "<li><b>주 1·2:</b> 서치콘솔에서 어떤 쿼리·페이지가 빠졌는지 데이터만 수집. 수정 작업 없음.</li>"
                 "<li><b>주 3:</b> 빠진 페이지를 \"검색 의도 변화\", \"콘텐츠 깊이\", \"E-E-A-T 신호\" 3축으로 분류.</li>"
                 "<li><b>주 4:</b> 가장 영향 큰 페이지 1~2개만 우선 개선. 그 외는 대조군으로 남김.</li>"
                 "</ul>"
                 "<p>이 순서를 지키면 \"무엇이 효과 있었는지\"를 측정할 수 있습니다. 측정이 가능한 것만이 다음 업데이트에도 통용되는 노하우가 됩니다.</p>"),
            ],
            key_takeaways=[
                "코어 업데이트는 7~14일 단계적 롤아웃이라 첫 며칠의 변동이 최종 결과가 아닙니다.",
                "패닉 작업은 진단 변수만 늘리고 측정 기준선을 무너뜨립니다.",
                "Disavow·콘텐츠 대량 수정·디자인 리뉴얼·새 도구 도입은 안정 이후로 미루세요.",
                "대신 \"4주 관찰\"이 진짜 원인을 찾는 가장 빠른 길입니다.",
            ],
            related=[
                ("Helpful Content System 셀프 점검 — 한국 사이트가 자주 떨어지는 7가지 질문", "/insights/google-seo/helpful-content-self-check/", "구글 SEO"),
                ("트래픽이 갑자기 떨어졌을 때 4주 진단 매뉴얼", "/insights/visibility/", "검색 노출"),
                ("SEO 컨설팅 서비스", "/services/seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/google-seo/post-core-update-mistakes/",
            title="구글 코어 업데이트 직후 2주, 절대 손대지 말아야 할 5가지",
            desc="코어 업데이트 직후 패닉 작업이 위험한 이유와 4주 관찰 매뉴얼.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/google-seo/helpful-content-self-check/": {
        "title": "Helpful Content System 셀프 점검 — 한국 사이트가 자주 떨어지는 7가지 질문 | OneSearchPro 인사이트",
        "desc": "구글의 Helpful Content System은 사이트 전체 평가에 영향을 줍니다. 한국 사이트가 셀프 평가에서 자주 떨어지는 7가지 질문과 통과 기준을 정리합니다.",
        "keywords": "Helpful Content System, HCS, 도움이 되는 콘텐츠, 구글 셀프 평가, 콘텐츠 품질 평가",
        "h1": "Helpful Content System 셀프 점검 — 한국 사이트가 자주 떨어지는 7가지 질문",
        "eyebrow": "GOOGLE SEO · ARTICLE",
        "lead": "Helpful Content System(HCS)은 \"이 사이트가 사람에게 도움이 되는가\"를 사이트 전체 단위로 평가합니다. 글 한 편이 아닌 사이트 전체 신호이기 때문에 한 번 분류되면 회복이 느립니다. 구글이 공개한 셀프 점검 질문 중 한국 사이트가 가장 자주 떨어지는 7가지를 짚어봅니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=8,
            intro="HCS는 개별 페이지가 아닌 \"사이트 전체\"를 평가합니다. 좋은 글 100편이 있어도 도움 안 되는 글 30편 때문에 사이트 전체가 강등될 수 있다는 의미입니다. 구글이 가이드라인에 공개한 셀프 평가 질문은 길지만, 한국 사이트가 자주 빠뜨리는 항목은 의외로 일정합니다.",
            sections=[
                ("HCS가 진짜로 보는 것 — 페이지가 아닌 사이트",
                 "<p>가장 큰 오해는 \"좋은 글 더 쓰면 되겠지\"입니다. HCS는 사이트 전체 평가입니다. 즉, 새 좋은 글 1편보다 도움 안 되는 옛 글 1편을 정리하는 게 더 효과적인 경우가 많습니다.</p>"
                 "<p>이게 \"콘텐츠 가지치기(Content Pruning)\"가 다시 중요해진 이유입니다. 트래픽도 거의 없고 가치도 없는 글은 noindex 처리하거나 통합·삭제하는 결정이 사이트 전체 신호를 끌어올립니다.</p>"),
                ("질문 1·2 — 이 글의 1차 목적이 사람인가 검색엔진인가",
                 "<p>\"우리는 사람을 위해 씁니다\"라고 답하기는 쉽습니다. 하지만 본문 첫 줄에 키워드가 부자연스럽게 박혀있거나, 같은 정보를 다른 표현으로 5번 반복하거나, 1차 키워드만 H2에 들어가 있는 글은 즉시 들킵니다.</p>"
                 "<p>점검 방법: \"이 글에서 1차 키워드를 모두 빼도 본문이 자연스럽게 읽히는가?\" 빼면 어색해진다면 키워드를 위해 쓴 글입니다.</p>"),
                ("질문 3 — 이 분야에 대한 깊이를 보여주는가",
                 "<p>SEO 입문자가 쓴 \"SEO란?\" 글과, SEO 컨설턴트가 5년 일한 후 쓴 \"SEO란?\" 글은 본문 분량이 같아도 다릅니다. 깊이의 차이는 다음에서 드러납니다.</p>"
                 "<ul>"
                 "<li>예외 케이스 언급 (\"이 방법이 안 통하는 산업은\")</li>"
                 "<li>도구·플랫폼의 버전별 차이</li>"
                 "<li>실패 사례 또는 안티패턴</li>"
                 "<li>관련 분야와의 충돌·트레이드오프</li>"
                 "</ul>"),
                ("질문 4·5 — 저자의 경험·전문성이 본문에 드러나는가",
                 "<p>저자 페이지에 자격증·경력을 나열하는 것만으로는 부족합니다. 본문 안에서 그 경험이 드러나야 합니다.</p>"
                 "<p>예시: \"구글 비즈니스 프로필 운영 가이드\" 글에서 단순 절차 나열 vs \"5년간 80개 매장 GBP를 운영하면서 가장 자주 실수한 항목은…\" 두 가지는 같은 정보를 담아도 완전히 다른 신호를 줍니다.</p>"),
                ("질문 6·7 — 다른 데서 못 보는 정보가 있는가, 끝까지 읽었을 때 만족스러운가",
                 "<p>한국 사이트가 가장 자주 떨어지는 항목이 \"다른 데서 못 보는 정보\"입니다. 위키백과·블로그·뉴스의 정보를 재정리한 글이 압도적으로 많습니다.</p>"
                 "<p>\"못 보는 정보\"의 출처는 결국 둘 중 하나입니다. (1) 본인이 직접 실험·작업한 결과, (2) 1차 자료에 대한 본인의 해석. 외부 정보 재정리만으로는 HCS를 통과하기 어렵습니다.</p>"),
                ("한국 사이트가 자주 떨어지는 빈도순 패턴",
                 "<ol>"
                 "<li><b>옛 글 가지치기 부재:</b> 트래픽 0인 글을 그대로 두고 새 글만 추가하는 패턴.</li>"
                 "<li><b>저자 정보 부재:</b> \"관리자\" 또는 빈 저자.</li>"
                 "<li><b>출처 인용 없음:</b> 모든 주장이 자체 의견처럼 보임.</li>"
                 "<li><b>본문 첫 100자 키워드 스터핑:</b> 검색엔진 우선 의도가 노출됨.</li>"
                 "</ol>"
                 "<p>위 4가지를 정비하는 것만으로도 HCS 평가에 의미 있는 변화가 나타납니다.</p>"),
            ],
            key_takeaways=[
                "HCS는 페이지가 아닌 사이트 전체 평가입니다. 가지치기가 새 글 발행보다 효과적일 때가 많습니다.",
                "\"1차 목적이 사람인가\"는 키워드를 빼고 본문이 읽히는지로 검증할 수 있습니다.",
                "저자 페이지의 자격 나열보다, 본문 안에 경험이 드러나는지가 더 중요합니다.",
                "옛 글 정리·저자 정보·출처 인용·키워드 스터핑 제거가 가장 효과적인 시작점입니다.",
            ],
            related=[
                ("구글 코어 업데이트 직후 2주, 절대 손대지 말아야 할 5가지", "/insights/google-seo/post-core-update-mistakes/", "구글 SEO"),
                ("쇼핑몰 제품 페이지 본문이 비어있을 때 추가하는 6단락 구조", "/insights/content-seo/product-page-content-structure/", "콘텐츠 SEO"),
                ("콘텐츠 SEO 서비스", "/services/content-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/google-seo/helpful-content-self-check/",
            title="Helpful Content System 셀프 점검 — 한국 사이트가 자주 떨어지는 7가지 질문",
            desc="구글 HCS의 셀프 평가 질문 중 한국 사이트가 가장 자주 떨어지는 패턴 분석.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    # Technical SEO category
    "/insights/technical-seo/discovered-not-indexed/": {
        "title": "서치콘솔 '발견됨 - 현재 색인되지 않음' 7가지 원인과 진단 순서 | OneSearchPro 인사이트",
        "desc": "구글 서치콘솔의 '발견됨 - 현재 색인되지 않음' 메시지가 의미하는 것과 7가지 흔한 원인, 빈도 순으로 정렬한 진단 순서를 정리합니다.",
        "keywords": "발견됨 현재 색인되지 않음, Discovered currently not indexed, 색인 누락, 서치콘솔, 크롤링 예산",
        "h1": "서치콘솔 \"발견됨 - 현재 색인되지 않음\" 7가지 원인과 진단 순서",
        "eyebrow": "TECHNICAL SEO · ARTICLE",
        "lead": "서치콘솔 색인 커버리지에서 가장 헷갈리는 메시지가 \"발견됨 - 현재 색인되지 않음\"입니다. 크롤링도 안 했다는 뜻이라 \"크롤링됨 - 현재 색인되지 않음\"과는 진단 순서가 다릅니다. 흔한 원인 7가지와 빈도순 진단법을 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=9,
            intro="\"발견됨\"은 구글이 URL의 존재는 알지만, 아직 가져가지(크롤링) 않았다는 뜻입니다. \"크롤링됨 - 색인되지 않음\"과는 완전히 다른 단계의 문제이며, 진단도 다른 순서로 접근해야 합니다. 실무에서 가장 자주 보는 7가지 원인을 빈도순으로 정리합니다.",
            sections=[
                ("\"발견됨\"과 \"크롤링됨\"의 차이 — 다른 진단법이 필요한 이유",
                 "<p>두 상태는 비슷해 보이지만 의미가 다릅니다.</p>"
                 "<ul>"
                 "<li><b>발견됨 - 색인되지 않음:</b> 구글이 URL을 알지만 가져가지 않음. 가져갈 만한 가치를 못 느끼거나, 가져갈 여유(크롤링 예산)가 없음.</li>"
                 "<li><b>크롤링됨 - 색인되지 않음:</b> 가져가긴 했는데 색인 안 시킴. 콘텐츠 품질·중복·E-E-A-T 신호 부족 등.</li>"
                 "</ul>"
                 "<p>\"발견됨\" 단계 문제는 크롤링 예산·사이트 권위·내부 링크 같은 \"신뢰 신호\" 이슈가 많고, \"크롤링됨\" 단계 문제는 콘텐츠 품질 이슈가 많습니다.</p>"),
                ("원인 1·2 — 크롤링 예산 부족, 사이트 전체 신뢰도 낮음",
                 "<p>신규 도메인이거나 사이트 권위가 낮으면 구글은 크롤링 예산을 작게 할당합니다. 발견은 했지만 \"굳이 지금 가져가야 할까\" 판단을 미루는 상태입니다.</p>"
                 "<p>점검 방법: 서치콘솔 → 설정 → 크롤링 통계에서 \"하루 평균 크롤링 페이지 수\"가 사이트 페이지 수 대비 너무 적은지 확인합니다. 100페이지 사이트인데 하루 평균 크롤이 5건 미만이면 분명한 신호입니다.</p>"),
                ("원인 3·4 — 내부 링크 부재, 사이트맵 우선순위 미설정",
                 "<p>발견은 됐지만 다른 페이지에서 링크가 거의 없는 페이지는 구글이 \"중요하지 않다\"고 판단합니다. 사이트맵에만 있고 본문 어디서도 링크되지 않는 페이지가 가장 흔한 케이스입니다.</p>"
                 "<p>해결: 같은 주제 인기 페이지에서 해당 페이지로 본문 내 텍스트 링크 추가. 메뉴·푸터 링크보다 본문 내 컨텍스트 링크가 훨씬 강한 신호입니다.</p>"),
                ("원인 5 — 중복 콘텐츠 의심",
                 "<p>같은 사이트 내 다른 페이지와 본문이 유사하면, 구글은 \"이미 비슷한 페이지가 있으니 안 가져가도 되겠다\"고 판단합니다. 자주 보는 패턴은 카테고리·태그·페이지네이션이 모두 비슷한 본문을 노출하는 경우입니다.</p>"
                 "<p>점검: site:도메인 \"본문 첫 50자\" 로 구글에 검색해서 같은 본문을 가진 페이지가 여럿 나오는지 확인합니다. 나오면 canonical 정비가 필요합니다.</p>"),
                ("원인 6 — JS 렌더링 의존 콘텐츠",
                 "<p>SPA·React 사이트에서 본문이 JS로 렌더링된다면, 구글봇이 1차 크롤링 시 본문을 빈 페이지로 인식할 수 있습니다. \"발견됨\"에 머무는 시간이 길어지는 전형적 케이스입니다.</p>"
                 "<p>해결: SSR(서버 사이드 렌더링) 또는 pre-rendering 도입. 그 전에는 구글봇이 JS 렌더 큐에 들어가야 가져오는데, 큐가 길어 지연됩니다.</p>"),
                ("원인 7 — sitemap에만 있고 실제로는 노출 의도가 약한 URL",
                 "<p>자동 생성된 sitemap에 노이즈 URL(로그인, 파라미터 페이지, 카테고리 무한 페이지네이션)이 다량 포함되면 진짜 중요한 URL의 우선순위가 희석됩니다.</p>"
                 "<p>해결: sitemap을 \"수동 큐레이션\"으로 전환. 정말 색인 시키고 싶은 URL만 포함시킵니다. 100개의 진짜 URL이 1만 개의 자동 URL보다 효과적입니다.</p>"),
                ("진단 순서 — 가장 흔한 것부터",
                 "<ol>"
                 "<li>내부 링크 점검 (가장 빠르고 효과 큼)</li>"
                 "<li>sitemap 정리 (노이즈 URL 제거)</li>"
                 "<li>중복 콘텐츠 검사 (canonical 정비)</li>"
                 "<li>크롤링 통계 점검 (사이트 전체 권위 이슈인지)</li>"
                 "<li>JS 렌더링 의존 확인 (SPA인 경우)</li>"
                 "</ol>"
                 "<p>이 순서대로 점검하면 90% 케이스는 위 3단계에서 원인이 잡힙니다.</p>"),
            ],
            key_takeaways=[
                "\"발견됨\"과 \"크롤링됨\"은 다른 단계의 문제라 진단 순서가 다릅니다.",
                "가장 흔한 원인은 내부 링크 부재와 sitemap 노이즈입니다.",
                "JS 렌더링 의존 사이트는 \"발견됨\"에 오래 머무는 경향이 있습니다.",
                "sitemap은 자동 생성보다 큐레이션이 효과적입니다.",
            ],
            related=[
                ("워드프레스 사이트 LCP 4초 → 1.5초로 줄인 실제 작업 순서", "/insights/technical-seo/wordpress-lcp-fix/", "기술 SEO"),
                ("서치콘솔 \"크롤링됨 - 현재 색인되지 않음\" — 다른 상태와의 차이와 대응법", "/insights/visibility/crawled-not-indexed/", "검색 노출"),
                ("기술 SEO 진단 서비스", "/services/technical-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/technical-seo/discovered-not-indexed/",
            title="서치콘솔 \"발견됨 - 현재 색인되지 않음\" 7가지 원인과 진단 순서",
            desc="서치콘솔 '발견됨 - 색인되지 않음' 메시지의 원인 7가지와 빈도순 진단법.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/technical-seo/wordpress-lcp-fix/": {
        "title": "워드프레스 사이트 LCP 4초 → 1.5초로 줄인 실제 작업 순서 | OneSearchPro 인사이트",
        "desc": "워드프레스 사이트의 LCP(Largest Contentful Paint)가 느려지는 가장 흔한 4가지 원인과 효과 큰 순서로 정리한 작업 매뉴얼. 실측 기반.",
        "keywords": "워드프레스 LCP, Core Web Vitals, LCP 개선, 페이지 속도, 워드프레스 최적화",
        "h1": "워드프레스 사이트 LCP 4초 → 1.5초로 줄인 실제 작업 순서",
        "eyebrow": "TECHNICAL SEO · ARTICLE",
        "lead": "워드프레스 LCP가 느린 이유는 거의 정해져 있습니다. 4가지 핵심 원인을 효과 큰 순서로 정리하고, 실제 작업 단계와 측정 방법까지 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=8,
            intro="\"Core Web Vitals 90점+\"라는 목표는 추상적이라 막막합니다. 워드프레스 사이트에서 가장 자주 느려지는 원인은 LCP(Largest Contentful Paint)이고, LCP의 90%는 4가지 패턴에서 나옵니다. 이 4가지를 효과 순서대로 정리합니다.",
            sections=[
                ("워드프레스 LCP가 느려지는 4가지 빈도순 원인",
                 "<ol>"
                 "<li><b>Hero 이미지 비최적화</b> — 가장 큰 효과. 메인 비주얼이 압축 안 된 4MB PNG인 경우.</li>"
                 "<li><b>웹폰트 차단 렌더링</b> — Google Fonts 또는 무거운 한글 폰트가 본문 페인트를 지연.</li>"
                 "<li><b>플러그인·테마의 무거운 CSS/JS</b> — Elementor 같은 빌더가 본문에 200KB CSS 주입.</li>"
                 "<li><b>호스팅·캐싱 부재</b> — TTFB가 1초 넘는 호스팅, 캐싱 플러그인 미설정.</li>"
                 "</ol>"
                 "<p>실무에서 본 평균 분포는 위 순서가 그대로 영향력 순서입니다. 1번을 잡으면 보통 1~1.5초 단축, 2~4번은 각 0.3~0.7초 정도 단축합니다.</p>"),
                ("작업 1 — Hero 이미지 처리 (가장 큰 효과)",
                 "<p>워드프레스 사이트의 첫 화면 메인 이미지가 LCP 요소인 경우가 압도적으로 많습니다. 다음 순서로 처리합니다.</p>"
                 "<ol>"
                 "<li>이미지를 WebP로 변환 (PNG/JPG 대비 30~50% 절감)</li>"
                 "<li>실제 표시 크기로 리사이즈 (1920×1080을 1200×675로)</li>"
                 "<li><code>&lt;img&gt;</code>에 <code>fetchpriority=\"high\"</code> 속성 추가 (Chrome 우선 로딩)</li>"
                 "<li>preload 링크 추가: <code>&lt;link rel=\"preload\" as=\"image\" href=\"...\"&gt;</code></li>"
                 "<li>모바일/데스크탑 분기 (srcset)</li>"
                 "</ol>"
                 "<p>이 5가지만 처리하면 LCP가 4초→2초대로 떨어지는 경우가 흔합니다.</p>"),
                ("작업 2 — 웹폰트 로딩 최적화",
                 "<p>한글 폰트는 영문보다 파일 크기가 5~10배 큽니다. Pretendard, Noto Sans KR을 그대로 로드하면 LCP를 0.5초 이상 잡아먹는 경우가 많습니다.</p>"
                 "<ul>"
                 "<li><code>font-display: swap</code> 적용 (폰트 로딩 동안 시스템 폰트로 표시)</li>"
                 "<li>사용하지 않는 weight 제거 (보통 400, 600, 800만 있으면 충분)</li>"
                 "<li>Subset 사용 (필요한 글자 범위만 로드)</li>"
                 "<li>중요 폰트는 preload</li>"
                 "</ul>"),
                ("작업 3 — 플러그인·테마 CSS/JS 정리",
                 "<p>Elementor, WPBakery 같은 페이지 빌더는 사용하지 않는 CSS도 모든 페이지에 로드합니다. 다음 도구로 점검할 수 있습니다.</p>"
                 "<p>Chrome DevTools → Coverage 탭에서 \"사용되지 않는 CSS\" 비율 확인. 60% 이상이면 플러그인 정리가 필요합니다.</p>"
                 "<p>실무 권장: WP Asset CleanUp, Perfmatters 같은 도구로 페이지별 불필요한 스크립트 차단. 단, 일부 페이지에서 필요한 것을 차단하지 않도록 주의.</p>"),
                ("작업 4 — 호스팅·캐싱 점검",
                 "<p>TTFB(Time To First Byte)가 1초 넘으면 LCP 90점은 거의 불가능합니다. 호스팅 측정 방법:</p>"
                 "<ol>"
                 "<li>WebPageTest에서 측정 (실제 환경)</li>"
                 "<li>TTFB가 800ms 넘으면 호스팅 변경 또는 캐싱 강화 필요</li>"
                 "<li>WP Rocket, LiteSpeed Cache 같은 캐싱 플러그인 점검</li>"
                 "<li>Cloudflare CDN 무료 플랜으로도 TTFB 절반 가능</li>"
                 "</ol>"),
                ("측정 — PageSpeed Insights와 실측의 차이",
                 "<p>PageSpeed Insights 점수만 보면 안 됩니다. \"Lab Data\"(실험실 측정)와 \"Field Data\"(실제 사용자 데이터)가 다를 수 있습니다. 구글이 랭킹에 쓰는 건 Field Data입니다.</p>"
                 "<p>점검 순서: (1) 서치콘솔의 \"Core Web Vitals\" 리포트, (2) PageSpeed의 \"Origin Summary\", (3) CrUX Report. 이 3가지가 일치하면 진짜 개선된 것이고, Lab만 좋아졌다면 사용자 환경에서는 여전히 느릴 수 있습니다.</p>"),
            ],
            key_takeaways=[
                "워드프레스 LCP 90%는 Hero 이미지, 웹폰트, 플러그인 CSS/JS, 호스팅 4가지에서 결정됩니다.",
                "효과 순서로 작업하면 Hero 이미지 하나로 1~1.5초 단축이 가능합니다.",
                "한글 웹폰트는 파일 크기가 커서 swap, subset, preload가 필수입니다.",
                "PageSpeed Lab 점수가 아니라 서치콘솔 Field Data가 실제 랭킹 기준입니다.",
            ],
            related=[
                ("서치콘솔 \"발견됨 - 현재 색인되지 않음\" 7가지 원인과 진단 순서", "/insights/technical-seo/discovered-not-indexed/", "기술 SEO"),
                ("사이트 리뉴얼 후 트래픽 절반 — 301 리다이렉트 시 자주 빠뜨리는 12가지", "/insights/visibility/301-migration-mistakes/", "검색 노출"),
                ("기술 SEO 진단 서비스", "/services/technical-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/technical-seo/wordpress-lcp-fix/",
            title="워드프레스 사이트 LCP 4초 → 1.5초로 줄인 실제 작업 순서",
            desc="워드프레스 LCP 개선의 4가지 핵심 작업과 빈도순 매뉴얼.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    # Content SEO category
    "/insights/content-seo/medical-blog-first-100/": {
        "title": "병원·치과 블로그 첫 100자 — 환자 검색어로 시작해야 하는 이유와 예시 | OneSearchPro 인사이트",
        "desc": "병원·치과 블로그가 검색 노출이 약한 이유는 첫 100자에 있습니다. 환자가 실제로 검색하는 표현으로 시작하는 패턴과 의료광고심의 충돌을 피하는 작성법.",
        "keywords": "병원 블로그 SEO, 치과 블로그, 의료 콘텐츠, 환자 검색어, 의료광고심의",
        "h1": "병원·치과 블로그 첫 100자 — 환자 검색어로 시작해야 하는 이유와 예시",
        "eyebrow": "CONTENT SEO · ARTICLE",
        "lead": "병원·치과 블로그의 검색 노출이 약한 이유는 대개 첫 100자에 있습니다. 환자가 실제 검색하는 표현 대신 의료진의 학술적 표현으로 시작하기 때문입니다. 의료광고심의 규제와 충돌을 피하면서 검색 의도를 잡는 첫 문장 패턴을 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=7,
            intro="병원 블로그를 진단하면 가장 자주 보이는 문제가 두 가지입니다. 첫째, 첫 문장이 \"안녕하세요, ○○치과입니다\" 같은 인사로 시작. 둘째, 두 번째 문장부터 의학 용어로 들어감. 환자가 검색하는 표현과는 거의 겹치지 않습니다. 검색 노출의 절반은 첫 100자에서 결정됩니다.",
            sections=[
                ("왜 첫 100자가 결정적인가 — 메타 디스크립션 자동 생성",
                 "<p>메타 디스크립션을 따로 작성하지 않으면 구글이 본문 첫 부분을 추출해서 SERP에 표시합니다. 검색 결과에 노출되는 미리보기 문구가 \"안녕하세요\"로 시작하면 클릭률이 떨어집니다.</p>"
                 "<p>두 번째 이유는 검색 의도 매칭입니다. 구글은 첫 100~200자의 핵심 명사를 가장 비중 있게 평가합니다. 환자 검색어가 본문 첫 부분에 자연스럽게 들어있어야 \"이 글이 환자 질문에 답한다\"고 판단합니다.</p>"),
                ("환자가 실제로 검색하는 표현 vs 의료진 표현",
                 "<table><thead><tr><th>의료진 표현</th><th>환자 실제 검색어</th></tr></thead><tbody>"
                 "<tr><td>임플란트 식립</td><td>임플란트 시술 비용, 임플란트 아픈가요</td></tr>"
                 "<tr><td>치주염</td><td>잇몸 피, 잇몸 아픔, 양치할 때 피</td></tr>"
                 "<tr><td>교정 치료</td><td>치아 교정 얼마, 교정 몇 살부터, 투명교정 차이</td></tr>"
                 "<tr><td>충치 신경치료</td><td>이가 시리다, 신경치료 통증, 신경치료 후 통증</td></tr>"
                 "</tbody></table>"
                 "<p>실무에서 같은 글을 \"임플란트 식립 시 고려사항\" 대신 \"임플란트 시술 후 며칠 아픈가요?\"로 첫 문장을 바꿨더니 노출이 3배로 늘어난 경우가 있었습니다. 본문은 거의 그대로였습니다.</p>"),
                ("예시 분석 — 같은 주제, 다른 첫 100자",
                 "<p><b>나쁜 예:</b><br>\"안녕하세요, ○○치과입니다. 오늘은 임플란트 시술의 적응증과 시술 절차에 대해 알려드리겠습니다.\"</p>"
                 "<p><b>좋은 예:</b><br>\"임플란트 시술이 얼마나 아픈지, 회복까지 며칠 걸리는지 궁금하신 분들이 많습니다. 실제로 시술 당일과 다음 날, 1주일 차에 환자분들이 가장 자주 물어보시는 질문 5가지를 정리했습니다.\"</p>"
                 "<p>두 글은 같은 정보를 담을 수 있지만, 검색 의도와의 매칭이 다릅니다. \"임플란트 아픈가요\", \"임플란트 시술 회복\" 같은 실제 검색어를 첫 100자 안에 자연스럽게 담은 게 후자입니다.</p>"),
                ("의료광고심의 규제와의 충돌 — 무엇을 피해야 하나",
                 "<p>환자 검색어로 시작하되, 의료광고심의 규제를 위반하면 안 됩니다. 빈번한 위반 패턴은 다음과 같습니다.</p>"
                 "<ul>"
                 "<li>\"가장 빠른 치료\", \"부작용 없는 시술\" 같은 단정·과장 표현</li>"
                 "<li>치료 결과를 보장하는 표현 (\"확실히 낫습니다\")</li>"
                 "<li>비교 광고 (\"다른 치과보다 저렴\")</li>"
                 "<li>심사 받지 않은 가격 정보 노출</li>"
                 "</ul>"
                 "<p>해결책은 \"환자의 질문 자체를 인용\"하는 형식입니다. \"이렇게 효과적입니다\"가 아니라 \"이런 질문을 자주 받습니다\"로 시작하면 검색어 매칭과 규제 회피가 동시에 됩니다.</p>"),
                ("실무에서 쓰는 첫 100자 작성 공식",
                 "<ol>"
                 "<li><b>1~2문장:</b> 환자의 실제 질문 형식으로 시작 (\"~가 궁금하신 분들이 많습니다\")</li>"
                 "<li><b>3문장:</b> 이 글에서 답할 항목 명시 (\"이 글에서는 ~3가지를 정리했습니다\")</li>"
                 "<li><b>핵심 키워드:</b> 첫 100자 안에 1차 키워드 1번, 변형 표현 1번 자연스럽게 포함</li>"
                 "<li><b>금지:</b> \"안녕하세요\", \"○○병원입니다\" 같은 인사형 도입</li>"
                 "</ol>"
                 "<p>인사는 글 끝의 CTA 부분에 자연스럽게 옮기면 됩니다. 첫 100자는 검색 의도에 답하는 공간으로 비워두세요.</p>"),
            ],
            key_takeaways=[
                "검색 노출의 절반은 첫 100자에서 결정됩니다. 메타 디스크립션 자동 추출과 검색 의도 매칭이 모두 여기서 이루어집니다.",
                "환자 검색어와 의료진 표현은 거의 겹치지 않습니다. 환자 표현을 우선하세요.",
                "의료광고심의 규제는 \"단정·보장·비교\" 표현을 피하면 됩니다. \"질문 인용\" 형식이 안전합니다.",
                "\"안녕하세요\"는 글 끝으로 옮기세요. 첫 100자는 검색 의도에 답하는 자리입니다.",
            ],
            related=[
                ("쇼핑몰 제품 페이지 본문이 비어있을 때 추가하는 6단락 구조", "/insights/content-seo/product-page-content-structure/", "콘텐츠 SEO"),
                ("Helpful Content System 셀프 점검 — 한국 사이트가 자주 떨어지는 7가지 질문", "/insights/google-seo/helpful-content-self-check/", "구글 SEO"),
                ("콘텐츠 SEO 서비스", "/services/content-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/content-seo/medical-blog-first-100/",
            title="병원·치과 블로그 첫 100자 — 환자 검색어로 시작해야 하는 이유와 예시",
            desc="병원 블로그 첫 100자 작성법과 의료광고심의 회피 패턴.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/content-seo/product-page-content-structure/": {
        "title": "쇼핑몰 제품 페이지 본문이 비어있을 때 추가하는 6단락 구조 | OneSearchPro 인사이트",
        "desc": "쇼핑몰 제품 페이지가 이미지 중심으로만 만들어져 검색 노출이 안 될 때, 본문을 채우는 6단락 구조와 스키마 마크업 가이드.",
        "keywords": "쇼핑몰 제품 페이지 SEO, 제품 상세 페이지, 제품 본문, Product 스키마, 쇼핑몰 콘텐츠",
        "h1": "쇼핑몰 제품 페이지 본문이 비어있을 때 추가하는 6단락 구조",
        "eyebrow": "CONTENT SEO · ARTICLE",
        "lead": "쇼핑몰 제품 페이지가 검색에 안 잡히는 가장 흔한 원인은 \"본문 자체가 거의 없는 것\"입니다. 이미지 중심으로 만들어진 페이지에 본문을 채우는 6단락 구조와 스키마 마크업을 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=8,
            intro="쇼핑몰 제품 페이지를 분석하면 패턴이 거의 비슷합니다. 메인 이미지 1개, 가격, 옵션, 그리고 상세설명 자리에는 큰 이미지 5장. 텍스트 본문은 사실상 없음. 검색엔진은 이미지 안의 글자를 읽지 못하므로 \"이 제품이 무엇인지\" 판단할 단서가 없습니다. 6단락 구조로 텍스트 본문을 채우면 색인과 검색 노출이 함께 회복됩니다.",
            sections=[
                ("제품 페이지가 본문 없이 만들어지는 이유와 그 비용",
                 "<p>본문 없는 이미지 위주 페이지의 비용은 크게 3가지입니다.</p>"
                 "<ul>"
                 "<li><b>색인 신호 부족:</b> 구글은 페이지 분류를 위해 텍스트 본문을 읽습니다. 이미지 alt만으로는 부족합니다.</li>"
                 "<li><b>롱테일 키워드 손실:</b> \"○○ 재질 ××\", \"○○ 사이즈 후기\" 같은 변형 검색에 노출 안 됨.</li>"
                 "<li><b>리치 결과 누락:</b> Product 스키마에 필요한 정보가 본문에 없으면 별점·가격 스니펫 노출 불가.</li>"
                 "</ul>"
                 "<p>대안은 단순합니다. 6개 단락만 추가하세요.</p>"),
                ("단락 1·2 — 누가 사용하는 제품인가, 어떤 문제를 해결하는가",
                 "<p><b>단락 1 (Who):</b> 이 제품을 누가 사용하는지. 타겟 사용자의 상황을 한 문단으로 설명합니다. 예: \"이 제품은 매일 1시간 이상 컴퓨터 앞에 앉는 분들 중 손목 통증을 느끼는 분들을 위해 만들었습니다.\"</p>"
                 "<p><b>단락 2 (Problem-Solution):</b> 사용자가 겪는 문제와 이 제품이 어떻게 해결하는지. \"손목 통증의 주요 원인은 ~. 이 제품은 ~ 방식으로 그 부담을 줄입니다.\"</p>"
                 "<p>이 두 단락에서 자연스럽게 검색 키워드가 본문에 녹습니다. 의도적으로 키워드를 끼워넣을 필요 없이, 사용자 상황을 설명하다 보면 들어갑니다.</p>"),
                ("단락 3·4 — 사양·재질·치수, 사용법·관리법",
                 "<p><b>단락 3:</b> 사양·재질·치수를 텍스트로. 표 형태가 좋습니다. 이미지에 있는 사양표라도 텍스트로 한 번 더 적어주세요.</p>"
                 "<p><b>단락 4:</b> 사용법과 관리법. 세탁 가능 여부, 보관 방법, 호환 부속품 등. 이 부분은 사용자의 후속 검색(\"○○ 세탁 가능\", \"○○ 호환 부품\")을 잡습니다.</p>"
                 "<p>실무에서 이 두 단락만 추가해도 롱테일 키워드 노출이 의미 있게 늘어나는 경우를 자주 봅니다. 같은 제품군에서 사양·관리 정보가 텍스트로 명시된 페이지가 거의 없기 때문입니다.</p>"),
                ("단락 5·6 — FAQ, 환불·교환·배송 정보",
                 "<p><b>단락 5 (FAQ):</b> 실제로 받은 질문 4~6개. 가짜 FAQ는 즉시 들킵니다. CS팀에 \"이번 달 자주 받은 문의 5개\"를 받아서 그대로 정리하세요.</p>"
                 "<p><b>단락 6 (환불·교환·배송):</b> 환불 가능 기간, 교환 조건, 배송 소요일, 무료 배송 기준. 이 정보는 신뢰 신호로도 작용하고, FAQ로 검색 결과 노출 가능성도 높입니다.</p>"
                 "<p>FAQ 단락은 FAQPage 스키마 마크업과 함께 적용하면 검색 결과에서 펼쳐진 형태로 노출될 수 있습니다.</p>"),
                ("스키마 마크업 — Product, Review, FAQPage 3종",
                 "<p>본문을 채웠으면 스키마도 함께 적용합니다.</p>"
                 "<ul>"
                 "<li><b>Product:</b> 제품명, 가격, 통화, 재고 상태, 브랜드. 별점 스니펫의 전제 조건.</li>"
                 "<li><b>AggregateRating + Review:</b> 평균 별점과 리뷰 수. 실제 리뷰 데이터 기반.</li>"
                 "<li><b>FAQPage:</b> FAQ 단락에서 추출한 질문·답변. 마크업 위치는 FAQ가 본문 안에 있어야 합니다.</li>"
                 "</ul>"
                 "<p>3가지 스키마가 모두 정확히 적용된 페이지는 SERP에서 별점·가격·FAQ가 함께 노출되는 \"풍부한 결과\"를 받을 가능성이 높아집니다.</p>"),
                ("주의할 점 — 가짜 정보·과장 표현·자동 생성의 함정",
                 "<p>FAQ를 인위적으로 만들거나, 사양을 부풀리거나, \"베스트셀러\" 같은 검증 안 된 표현을 넣으면 신뢰 신호가 역으로 작용합니다. 특히 AggregateRating은 실제 리뷰 기반이 아니면 위반입니다.</p>"
                 "<p>또한 동일한 본문을 수천 개 제품에 자동 생성으로 복붙하면 중복 콘텐츠로 분류됩니다. 카테고리 단위로 본문 템플릿을 다르게 가져가세요.</p>"),
            ],
            key_takeaways=[
                "쇼핑몰 제품 페이지의 검색 노출 부족은 \"본문 자체가 없다\"는 데서 시작합니다.",
                "6단락(누가·문제·사양·사용법·FAQ·환불배송)만 추가해도 롱테일 검색 노출이 의미 있게 늘어납니다.",
                "Product·AggregateRating·FAQPage 3종 스키마를 함께 적용하면 풍부한 결과 노출 가능성이 높아집니다.",
                "본문 자동 생성·가짜 FAQ는 신뢰 신호가 역으로 작용하므로 피해야 합니다.",
            ],
            related=[
                ("병원·치과 블로그 첫 100자 — 환자 검색어로 시작해야 하는 이유와 예시", "/insights/content-seo/medical-blog-first-100/", "콘텐츠 SEO"),
                ("Helpful Content System 셀프 점검 — 한국 사이트가 자주 떨어지는 7가지 질문", "/insights/google-seo/helpful-content-self-check/", "구글 SEO"),
                ("콘텐츠 SEO 서비스", "/services/content-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/content-seo/product-page-content-structure/",
            title="쇼핑몰 제품 페이지 본문이 비어있을 때 추가하는 6단락 구조",
            desc="쇼핑몰 제품 페이지에 본문을 채우는 6단락 구조와 스키마 가이드.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    # Local SEO category
    "/insights/local-seo/new-store-naver-place/": {
        "title": "신규 매장 네이버 플레이스 — 영수증 리뷰 적을 때 첫 3개월 운영 패턴 | OneSearchPro 인사이트",
        "desc": "신규 매장이 네이버 플레이스에서 \"리뷰 0\" 상태로 시작할 때, 첫 3개월을 어떻게 운영해야 노출이 자연스럽게 자라는지 정리합니다.",
        "keywords": "네이버 플레이스, 신규 매장 SEO, 영수증 리뷰, 플레이스 노출, 로컬 SEO",
        "h1": "신규 매장 네이버 플레이스 — 영수증 리뷰 적을 때 첫 3개월 운영 패턴",
        "eyebrow": "LOCAL SEO · ARTICLE",
        "lead": "신규 매장이 네이버 플레이스에 등록하자마자 부딪히는 함정이 \"리뷰가 없어서 노출이 안 됨 → 노출 안 되니까 리뷰가 안 쌓임\"입니다. 첫 3개월을 어떻게 운영해야 이 함정에서 벗어나는지, 월별 우선순위로 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=7,
            intro="네이버 플레이스 노출은 영수증 리뷰가 큰 비중을 차지합니다. 그런데 신규 매장은 리뷰가 거의 없어서, 자연 노출이 약하고, 그래서 손님이 적어, 리뷰가 더 안 쌓이는 악순환이 생깁니다. 첫 3개월을 우선순위 있게 운영하면 이 함정을 빠져나올 수 있습니다.",
            sections=[
                ("첫 한 달 — 리뷰보다 정보 완성도가 먼저인 이유",
                 "<p>리뷰 유도 캠페인을 첫 한 달부터 시작하는 매장이 많습니다. 그런데 정보가 비어있으면 리뷰가 와도 노출이 잘 안 됩니다. 첫 한 달은 정보 완성도에 집중하세요.</p>"
                 "<ul>"
                 "<li>상호·주소·전화·영업시간 (NAP) 정확히, 변동 없이</li>"
                 "<li>카테고리 정확 설정 (대분류·소분류 모두)</li>"
                 "<li>서비스/메뉴 항목 (가능한 모든 항목 등록)</li>"
                 "<li>사진 30장 이상 (외관, 내부, 메뉴/제품, 디테일)</li>"
                 "<li>대표 키워드 3~5개를 자연스럽게 포함한 소개 문구</li>"
                 "</ul>"
                 "<p>이 단계 완성도가 낮으면 어떤 리뷰가 와도 노출이 약합니다.</p>"),
                ("둘째 달 — 블로그 연동과 게시물 운영",
                 "<p>네이버 플레이스는 같은 네이버 생태계의 블로그·카페와 신호를 주고받습니다. 둘째 달부터는 외부 콘텐츠 신호를 만들기 시작합니다.</p>"
                 "<ul>"
                 "<li>매장 블로그 1개 운영, 주 1편 발행</li>"
                 "<li>각 블로그 글에서 플레이스로 자연스럽게 링크</li>"
                 "<li>플레이스 게시물 주 1~2회 (이벤트·신메뉴·일상 모두 가능)</li>"
                 "<li>지역 키워드(\"○○동 ○○\")를 블로그 제목과 본문에 자연스럽게 포함</li>"
                 "</ul>"
                 "<p>이 시점부터 자연 유입이 천천히 시작됩니다.</p>"),
                ("셋째 달 — 영수증 리뷰 자연스럽게 유도",
                 "<p>정보·외부 신호가 갖춰진 다음에야 리뷰 유도가 효과를 봅니다. 단, 페널티 없는 방식이어야 합니다.</p>"
                 "<ul>"
                 "<li>매장 내 QR 코드로 영수증 리뷰 안내 (가장 자연스러운 방식)</li>"
                 "<li>결제 후 \"별점 안 주셔도 한 줄 후기 부탁드린다\" 같은 정중한 안내</li>"
                 "<li>리뷰 작성 고객에게 다음 방문 시 작은 혜택 (직접 금품 거래 금지)</li>"
                 "</ul>"
                 "<p>주의: 리뷰 대가로 즉시 금품 제공, 가짜 리뷰 의뢰, 리뷰 강요는 네이버 정책 위반이고 적발 시 매장이 노출에서 사라질 수 있습니다.</p>"),
                ("흔히 하는 실수와 패널티 위험",
                 "<p>신규 매장이 자주 빠지는 함정들입니다.</p>"
                 "<ol>"
                 "<li><b>NAP 불일치:</b> 플레이스, 사이트, SNS의 주소·전화가 미세하게 다름 (\"동\" vs \"로\").</li>"
                 "<li><b>카테고리 한 개만 설정:</b> 가능한 카테고리 1~2개 추가하면 노출 채널이 늘어납니다.</li>"
                 "<li><b>사진 5장 미만:</b> 첫 30일 안에 30장 이상 권장.</li>"
                 "<li><b>리뷰 어뷰징:</b> 지인 리뷰 대량 작성. 네이버가 패턴을 감지합니다.</li>"
                 "</ol>"),
                ("3개월 후 — 무엇을 측정해야 하나",
                 "<p>3개월 시점에 다음을 점검합니다.</p>"
                 "<ul>"
                 "<li>\"지역명 + 업종\" 검색에서 우리 매장 노출 순위</li>"
                 "<li>플레이스 방문자 수(유입 분석)</li>"
                 "<li>영수증 리뷰 수와 평균 별점</li>"
                 "<li>블로그 글의 검색 노출 키워드</li>"
                 "</ul>"
                 "<p>이 4가지가 함께 늘어나고 있다면 운영 방향이 맞다는 뜻입니다. 한두 가지만 늘고 나머지가 정체라면 우선순위 재조정이 필요합니다.</p>"),
            ],
            key_takeaways=[
                "첫 한 달은 리뷰 유도보다 정보 완성도(NAP, 카테고리, 사진)에 집중하세요.",
                "둘째 달부터 블로그·게시물로 외부 신호를 만들기 시작합니다.",
                "리뷰 유도는 셋째 달부터, 페널티 없는 자연스러운 방식으로만.",
                "3개월 후 노출·방문·리뷰·블로그 4가지를 함께 측정해 방향을 점검합니다.",
            ],
            related=[
                ("다지점 매장 구글 비즈니스 프로필 — 본사·지점 정보 분리 원칙과 흔한 실수", "/insights/local-seo/multi-location-gbp/", "지역 SEO"),
                ("지역 SEO 사례", "/case-studies/local-seo/", "성공사례"),
                ("지역 SEO 서비스", "/services/local-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/local-seo/new-store-naver-place/",
            title="신규 매장 네이버 플레이스 — 영수증 리뷰 적을 때 첫 3개월 운영 패턴",
            desc="신규 매장 네이버 플레이스 운영 첫 3개월의 우선순위 매뉴얼.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/local-seo/multi-location-gbp/": {
        "title": "다지점 매장 구글 비즈니스 프로필 — 본사·지점 정보 분리 원칙과 흔한 실수 | OneSearchPro 인사이트",
        "desc": "지점 여러 개를 운영하는 매장이 구글 비즈니스 프로필을 통합 관리할 때, 본사·지점 정보를 어떻게 분리해야 지역 키워드 노출이 분산되지 않는지 정리합니다.",
        "keywords": "구글 비즈니스 프로필, GBP, 다지점 매장, 프랜차이즈 SEO, NAP 일관성",
        "h1": "다지점 매장 구글 비즈니스 프로필 — 본사·지점 정보 분리 원칙과 흔한 실수",
        "eyebrow": "LOCAL SEO · ARTICLE",
        "lead": "지점 여러 개를 운영하면서 본사 정보를 모든 지점에 복붙해두면 \"○○동 ○○\" 같은 지역 키워드 노출이 분산됩니다. 본사와 지점이 가져가야 할 정보를 분리하는 원칙과 흔한 실수를 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=7,
            intro="3개 이상의 지점을 운영하는 매장의 구글 비즈니스 프로필(GBP)을 진단하면 공통 패턴이 보입니다. 본사 정보가 모든 지점에 복붙되어 있고, 지점별 차별점이 사라져 있습니다. 그 결과 \"○○동 ○○\" 검색에서 본사 페이지만 노출되거나, 또는 지점 어디도 명확히 노출되지 않습니다. 분리 원칙이 필요합니다.",
            sections=[
                ("본사 정보를 모든 지점에 복붙하면 안 되는 이유",
                 "<p>구글은 같은 본문·사진·카테고리를 가진 여러 GBP를 \"비슷한 후보\"로 인식합니다. 결과적으로 어느 지점도 명확한 1순위가 되지 못합니다.</p>"
                 "<p>또한 \"○○동 ○○\" 같은 지역 키워드 검색에서, 본사 정보만 가진 지점들은 모두 동일한 권위 신호를 받습니다. 구글이 지점 간 우선순위를 결정할 단서가 없으므로 노출 위치가 일관되게 잡히지 않습니다.</p>"),
                ("분리 원칙 1·2 — 위치, 카테고리",
                 "<p><b>위치(주소):</b> 각 지점의 실제 주소를 정확히 입력. 본사 주소를 그대로 두면 안 됨. 카카오맵·네이버 지도와 좌표가 일치해야 합니다.</p>"
                 "<p><b>카테고리:</b> 같은 업종이라도 지점마다 주력 카테고리가 다르면 분리. 예: 본점은 \"디저트 카페\", 2호점은 \"브런치 카페\"로 1차 카테고리 다르게 설정.</p>"
                 "<p>카테고리는 1차 외에 2~3개 부카테고리를 추가할 수 있으니, 지점별 강점을 반영하세요.</p>"),
                ("분리 원칙 3·4 — 사진, 리뷰 응대",
                 "<p><b>사진:</b> 본사 사진을 그대로 쓰지 마세요. 지점별로 실제 외관·내부·메뉴 사진을 따로 촬영해서 올립니다. 같은 사진을 여러 GBP에 쓰면 신뢰 신호가 감점됩니다.</p>"
                 "<p><b>리뷰 응대:</b> 본사가 모든 지점 리뷰를 동일한 템플릿으로 응대하면 패턴이 보입니다. 지점 매니저가 직접 답하는 게 가장 좋고, 본사가 응대해야 한다면 응대 문구를 지점·상황별로 다양화하세요.</p>"),
                ("본사가 통합 관리해야 할 항목",
                 "<p>모든 걸 지점에 맡기면 일관성이 떨어집니다. 본사가 가져가야 할 항목은 다음과 같습니다.</p>"
                 "<ul>"
                 "<li>브랜드명 표기 통일 (\"○○카페 강남점\" vs \"○○카페강남점\" 같은 미세 차이 방지)</li>"
                 "<li>본사 차원의 프로모션·이벤트 게시</li>"
                 "<li>로고·브랜드 자산 일관성</li>"
                 "<li>운영 정책·환불 정책 등 공통 정보</li>"
                 "<li>위기 대응 매뉴얼 (부정 리뷰·언론 보도 등)</li>"
                 "</ul>"),
                ("흔한 실수와 페널티 위험",
                 "<ol>"
                 "<li><b>가짜 지점 등록:</b> 실제 운영하지 않는 주소에 GBP 만들기. 즉시 정지 사유.</li>"
                 "<li><b>키워드 스터핑:</b> 상호에 \"○○카페 강남 디저트 브런치\" 같은 키워드 나열. 정책 위반.</li>"
                 "<li><b>리뷰 매수:</b> 지점 평균 별점 올리려고 가짜 리뷰. 구글이 패턴 감지하면 지점·본사 모두 페널티.</li>"
                 "<li><b>주소 변경 잦음:</b> 6개월 안에 주소를 두 번 이상 바꾸면 신뢰도 떨어집니다.</li>"
                 "</ol>"),
                ("3개월·6개월 시점에 측정할 것",
                 "<p>다지점 GBP 운영 효과는 6개월 단위로 봅니다.</p>"
                 "<ul>"
                 "<li>\"지역명 + 업종\" 검색에서 각 지점의 노출 위치</li>"
                 "<li>지도 결과(로컬 팩) 노출 빈도</li>"
                 "<li>지점별 통화·방향 안내 클릭 수</li>"
                 "<li>지점별 평균 별점과 리뷰 수의 균형</li>"
                 "</ul>"
                 "<p>특정 지점만 매우 강하고 다른 지점이 약하다면, 분리 원칙이 제대로 적용 안 됐을 가능성이 큽니다.</p>"),
            ],
            key_takeaways=[
                "본사 정보를 지점에 복붙하면 지역 키워드 노출이 분산됩니다.",
                "위치·카테고리·사진·리뷰 응대 4가지는 지점별로 분리해야 합니다.",
                "브랜드명 표기, 정책, 위기 대응은 본사가 통합 관리하세요.",
                "가짜 지점·키워드 스터핑·리뷰 매수는 본사·지점 모두 페널티 위험입니다.",
            ],
            related=[
                ("신규 매장 네이버 플레이스 — 영수증 리뷰 적을 때 첫 3개월 운영 패턴", "/insights/local-seo/new-store-naver-place/", "지역 SEO"),
                ("지역 SEO 사례", "/case-studies/local-seo/", "성공사례"),
                ("지역 SEO 서비스", "/services/local-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/local-seo/multi-location-gbp/",
            title="다지점 매장 구글 비즈니스 프로필 — 본사·지점 정보 분리 원칙과 흔한 실수",
            desc="다지점 매장의 GBP 운영 원칙과 본사·지점 정보 분리 가이드.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    # Backlink & Digital PR category
    "/insights/backlink-pr/disavow-decision/": {
        "title": "이전 대행사가 남긴 위험한 백링크 — 어디서부터 Disavow 결정해야 하나 | OneSearchPro 인사이트",
        "desc": "이전 대행사가 만든 백링크 중 위험한 것을 식별하고 Disavow 여부를 결정하는 기준. 즉시 처리·보류·유지 3단계 분류와 단계적 제출 전략.",
        "keywords": "Disavow, 백링크 진단, 위험한 백링크, 백링크 정리, 페널티 회복",
        "h1": "이전 대행사가 남긴 위험한 백링크 — 어디서부터 Disavow 결정해야 하나",
        "eyebrow": "BACKLINK & DIGITAL PR · ARTICLE",
        "lead": "이전 대행사가 만든 백링크 프로파일을 받아서 정리할 때 가장 어려운 건 \"어디서부터 어디까지가 위험한가\"의 경계가 모호하다는 점입니다. 즉시 Disavow 후보·보류·유지로 분류하는 실무 기준을 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=9,
            intro="과거 대행사 작업으로 만들어진 백링크를 받아서 정리할 때, 무차별 Disavow는 가장 위험합니다. 살아있는 신호까지 차단해서 트래픽이 추가로 떨어지는 경우가 흔합니다. \"위험\"을 3단계로 분류하고, 단계적으로 처리하는 게 정답입니다.",
            sections=[
                ("\"위험\"의 정의가 모호한 이유 — 도구 점수의 한계",
                 "<p>Ahrefs Toxic Score, SEMrush Toxic Score, Moz Spam Score는 점수가 다 다르게 나옵니다. 한 도구에서 위험으로 분류된 링크가 다른 도구에서는 정상으로 나오는 경우도 흔합니다.</p>"
                 "<p>도구 점수만 신뢰하면 안 됩니다. 점수는 1차 필터로만 쓰고, 실제 위험 여부는 사이트 직접 방문 후 사람이 판단해야 합니다.</p>"),
                ("즉시 Disavow 후보 — 명백한 스팸",
                 "<p>다음 조건 중 2개 이상에 해당하면 즉시 Disavow 후보입니다.</p>"
                 "<ul>"
                 "<li>도메인 자체가 스팸 디렉토리·자동 생성 사이트</li>"
                 "<li>한 줄짜리 \"링크 모음\" 페이지에 우리 링크가 박혀있음</li>"
                 "<li>발신 사이트의 다른 외부 링크가 명백히 도박·성인·약품 사이트</li>"
                 "<li>본문이 자동 번역 또는 의미 없는 문자열</li>"
                 "<li>사이트 자체가 다운되어 있음 (404·연결 불가)</li>"
                 "</ul>"
                 "<p>이 카테고리는 disavow 대상으로 확정해도 손해가 거의 없습니다.</p>"),
                ("보류 대상 — 애매한 중간 지대",
                 "<p>가장 어려운 게 이 카테고리입니다. 다음 같은 링크들입니다.</p>"
                 "<ul>"
                 "<li>업종이 다르지만 본문은 정상인 사이트의 게스트 포스트</li>"
                 "<li>도구가 \"위험\"으로 분류했지만 실제로는 평범한 블로그</li>"
                 "<li>오래된 디렉토리 사이트 (스팸은 아니지만 가치도 낮음)</li>"
                 "<li>실제 트래픽이 있는 PBN 의심 사이트</li>"
                 "</ul>"
                 "<p>이런 링크는 즉시 disavow 하지 말고 3~6개월 관찰 권장. 추가 신호(다른 위험 패턴, 페널티 메시지 등)가 보이면 그때 처리합니다.</p>"),
                ("Disavow 하지 말아야 할 링크",
                 "<p>다음은 도구가 위험으로 분류해도 disavow 하면 안 됩니다.</p>"
                 "<ul>"
                 "<li>실제 트래픽이 있는 일반 블로그·매거진</li>"
                 "<li>도메인 권위(DR)는 낮지만 본문 컨텍스트가 자연스러운 링크</li>"
                 "<li>지역 디렉토리·업종 디렉토리 (NAP 신호 가치)</li>"
                 "<li>SNS·커뮤니티 링크 (nofollow라도 신뢰 신호)</li>"
                 "</ul>"
                 "<p>이런 링크를 무차별 disavow하면 도메인 권위가 빠지면서 검색 노출이 더 떨어질 수 있습니다.</p>"),
                ("단계적 제출 전략 — 한 번에 다 올리지 마세요",
                 "<p>Disavow 파일은 한 번에 1,000개씩 올리지 마세요. 다음 단계로 나눠 제출합니다.</p>"
                 "<ol>"
                 "<li><b>1차 (확정 스팸 100~200개):</b> 즉시 처리 후 4주 관찰</li>"
                 "<li><b>2차 (1차 분석 후 확신 갖춘 추가 100~200개):</b> 4~8주차에 제출</li>"
                 "<li><b>3차 (보류 대상 중 재평가):</b> 3~6개월 후 필요 시 추가</li>"
                 "</ol>"
                 "<p>단계적 제출의 이유는 효과 측정입니다. 1차 처리 후 어떤 키워드가 회복됐는지 보면, 어떤 종류의 링크가 진짜 문제였는지 알 수 있습니다.</p>"),
                ("주의 — 수동 조치 회복과는 다른 작업",
                 "<p>수동 조치(Manual Action) 메시지를 받은 경우와, 알고리즘 페널티가 의심되는 경우는 disavow 우선순위가 다릅니다.</p>"
                 "<ul>"
                 "<li><b>수동 조치:</b> Disavow + 재심사 요청이 같이 가야 합니다. 광범위하게 처리하는 게 안전.</li>"
                 "<li><b>알고리즘 의심:</b> Disavow는 단계적으로. 재심사 요청은 의미 없음.</li>"
                 "</ul>"
                 "<p>두 경우를 구분하지 않고 같은 전략으로 가면 손해가 큽니다.</p>"),
            ],
            key_takeaways=[
                "도구 점수는 1차 필터일 뿐, 위험 판단은 사이트 직접 확인 후 사람이 해야 합니다.",
                "즉시 Disavow는 명백한 스팸(스팸 디렉토리·자동 생성·도박/성인 인접 등)만.",
                "보류 대상은 3~6개월 관찰 후 결정. 무차별 처리는 살아있는 신호까지 차단합니다.",
                "Disavow는 단계적으로(1차→4주 관찰→2차) 제출해야 효과 측정이 가능합니다.",
            ],
            related=[
                ("한국 언론사 보도자료 배포 — 백링크 따라오는 매체와 안 오는 매체 구분법", "/insights/backlink-pr/korean-press-release/", "백링크 · 디지털 PR"),
                ("서치콘솔 \"크롤링됨 - 현재 색인되지 않음\" — 다른 상태와의 차이와 대응법", "/insights/visibility/crawled-not-indexed/", "검색 노출"),
                ("디지털 PR · 백링크 진단 서비스", "/services/digital-pr/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/backlink-pr/disavow-decision/",
            title="이전 대행사가 남긴 위험한 백링크 — 어디서부터 Disavow 결정해야 하나",
            desc="위험한 백링크의 3단계 분류와 단계적 Disavow 제출 전략.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/backlink-pr/korean-press-release/": {
        "title": "한국 언론사 보도자료 배포 — 백링크 따라오는 매체와 안 오는 매체 구분법 | OneSearchPro 인사이트",
        "desc": "한국 언론사에 보도자료를 뿌렸을 때 백링크가 따라오는 매체와 안 오는 매체의 차이. 본문 링크 vs 텍스트 언급, 발행 패턴, 측정 방법.",
        "keywords": "보도자료 SEO, 언론사 백링크, 디지털 PR, 보도자료 배포, 한국 언론 SEO",
        "h1": "한국 언론사 보도자료 배포 — 백링크 따라오는 매체와 안 오는 매체 구분법",
        "eyebrow": "BACKLINK & DIGITAL PR · ARTICLE",
        "lead": "같은 보도자료를 같은 시점에 여러 언론사에 뿌렸는데, 결과는 매체마다 다릅니다. 본문에 우리 사이트 링크를 그대로 두는 매체가 있고, 텍스트로만 언급하는 매체가 있고, 아예 우리 회사명만 노출하는 매체가 있습니다. 구분 기준을 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=7,
            intro="한국 언론사 보도자료의 SEO 효과는 매체마다 천차만별입니다. 같은 비용을 들였는데도 백링크가 따라오는 매체와 안 오는 매체가 명확히 구분됩니다. 우리는 어떤 매체에 우선순위를 둬야 할까요?",
            sections=[
                ("왜 같은 보도자료인데 결과가 다른가",
                 "<p>이유는 매체 편집 정책 때문입니다. 외부 링크를 본문에 그대로 두는 매체는 점점 줄어들고 있습니다. 광고·홍보성 콘텐츠 구분 강화 흐름 때문입니다.</p>"
                 "<p>매체는 크게 3가지 패턴으로 갈립니다.</p>"
                 "<ul>"
                 "<li><b>본문 링크 그대로 (가장 적음):</b> 보내준 보도자료의 링크가 본문에 dofollow로 살아남음.</li>"
                 "<li><b>텍스트만 언급 (가장 흔함):</b> 회사명·서비스명만 텍스트로 노출, 링크 제거.</li>"
                 "<li><b>편집 후 재작성:</b> 보도자료 내용을 재작성, 회사명도 빠질 수 있음.</li>"
                 "</ul>"),
                ("백링크 따라오는 매체의 특징",
                 "<p>실무에서 본 패턴은 다음과 같습니다.</p>"
                 "<ul>"
                 "<li>중소·전문 언론(IT, 산업 전문지)이 종합 일간지보다 링크 살아남는 경향</li>"
                 "<li>유료 보도자료 플랫폼(뉴스와이어 등)은 본문 링크 정책이 명확</li>"
                 "<li>매체별 보도자료 섹션은 일반 기사보다 링크 보존율 높음</li>"
                 "<li>경제·산업 카테고리는 IT·라이프스타일보다 보존율 높음</li>"
                 "</ul>"
                 "<p>주요 일간지·방송사는 본문 링크를 거의 제거합니다. 브랜드 노출 가치는 있지만 SEO 백링크 가치는 낮습니다.</p>"),
                ("백링크 안 오는 매체와 대안 — 브랜드 언급의 가치",
                 "<p>본문 링크 없이 회사명만 텍스트로 노출되는 경우도 SEO 가치는 있습니다. 이게 \"링크 없는 브랜드 언급(unlinked mention)\"이고, 구글이 신뢰 신호로 평가합니다.</p>"
                 "<p>또한 \"○○사 발표에 따르면\" 같은 인용 표현이 본문에 들어가면 검색 결과의 \"엔티티(Entity) 신호\"로 작용합니다. 시간이 지나면 \"우리 회사\" 키워드 검색 결과의 안정성에 기여합니다.</p>"
                 "<p>대안 전략: 본문 링크가 안 살아남는 매체에는 회사명·임원명·서비스명을 정확히 노출시키는 방향으로 보도자료를 설계합니다.</p>"),
                ("보도자료 본문에 추가해야 할 SEO 요소",
                 "<p>매체가 편집해도 살아남기 쉬운 요소들입니다.</p>"
                 "<ul>"
                 "<li>회사명·서비스명 정확한 표기 (메인 사이트와 동일하게)</li>"
                 "<li>대표·임원의 직책과 이름</li>"
                 "<li>주소(시·구 단위)와 설립연도</li>"
                 "<li>구체적 수치 (성과·계약·투자 규모 등)</li>"
                 "<li>인용구 1~2개 (편집되어도 살아남는 경향)</li>"
                 "</ul>"
                 "<p>이 정보들은 검색 결과의 Knowledge Panel·Entity 인식에 기여합니다. 백링크보다 느리지만 더 안정적인 신호입니다.</p>"),
                ("측정 — 색인 vs 트래픽 vs 브랜드 검색",
                 "<p>보도자료 효과는 3가지 지표로 봅니다.</p>"
                 "<ul>"
                 "<li><b>색인:</b> 발행 매체 페이지가 구글에 색인됐는지 (site: 검색)</li>"
                 "<li><b>백링크 출처:</b> Ahrefs 등에서 신규 외부 링크로 잡히는지</li>"
                 "<li><b>브랜드 검색 증가:</b> 서치콘솔에서 회사명 검색 쿼리 증가</li>"
                 "</ul>"
                 "<p>가장 자주 놓치는 게 \"브랜드 검색 증가\"입니다. 보도자료 발행 후 2~4주 사이 회사명 검색이 늘었다면 보도자료가 노출은 됐다는 신호입니다. 백링크가 없어도 의미 있는 결과입니다.</p>"),
                ("주의 — 보도자료 남발의 위험",
                 "<p>한 달에 5건 이상 비슷한 보도자료를 뿌리면 매체 측에서 \"양산형\"으로 분류해 게재 거부하거나, 같은 내용 중복으로 구글이 사이트 권위에 부정적 신호를 줄 수 있습니다.</p>"
                 "<p>월 1~2건, 진짜 뉴스 가치가 있는 내용으로 제한하는 게 안전합니다.</p>"),
            ],
            key_takeaways=[
                "본문 링크가 살아남는 매체는 중소·전문 언론과 보도자료 섹션입니다.",
                "주요 일간지는 브랜드 노출 가치는 있지만 SEO 백링크 가치는 낮습니다.",
                "링크가 안 살아남아도 \"브랜드 언급\"과 \"엔티티 신호\"는 누적됩니다.",
                "측정은 색인·백링크·브랜드 검색 3가지를 함께 봐야 합니다.",
            ],
            related=[
                ("이전 대행사가 남긴 위험한 백링크 — 어디서부터 Disavow 결정해야 하나", "/insights/backlink-pr/disavow-decision/", "백링크 · 디지털 PR"),
                ("Helpful Content System 셀프 점검 — 한국 사이트가 자주 떨어지는 7가지 질문", "/insights/google-seo/helpful-content-self-check/", "구글 SEO"),
                ("디지털 PR · 백링크 진단 서비스", "/services/digital-pr/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/backlink-pr/korean-press-release/",
            title="한국 언론사 보도자료 배포 — 백링크 따라오는 매체와 안 오는 매체 구분법",
            desc="한국 언론 보도자료의 백링크 보존 패턴과 매체별 SEO 가치.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    # SNS Marketing category
    "/insights/sns/youtube-shorts-description/": {
        "title": "유튜브 쇼츠 설명란 — 본 영상 페이지로 트래픽 유도하는 텍스트 구조 | OneSearchPro 인사이트",
        "desc": "유튜브 쇼츠 설명란을 어떻게 써야 본 영상이나 외부 사이트로 트래픽이 흐르는지. 첫 줄·본문·해시태그 구조와 측정 방법.",
        "keywords": "유튜브 쇼츠 SEO, 쇼츠 설명란, 유튜브 마케팅, 쇼츠 클릭률, 외부 링크 유도",
        "h1": "유튜브 쇼츠 설명란 — 본 영상 페이지로 트래픽 유도하는 텍스트 구조",
        "eyebrow": "SNS MARKETING · ARTICLE",
        "lead": "유튜브 쇼츠는 짧고 빠르게 끝나는 콘텐츠라 설명란을 거의 안 보고 넘어갑니다. 그런데 알고리즘 노출과 외부 트래픽 유도 둘 다에 설명란이 영향을 줍니다. 클릭률을 높이는 텍스트 구조를 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=6,
            intro="쇼츠 설명란은 길게 안 보이지만 알고리즘과 검색에는 영향을 줍니다. 또한 \"더 보기\"를 펼친 사용자는 이미 관심이 있는 사람이라 외부 링크 클릭률이 높습니다. 짧은 시간에 결정되는 클릭을 잡는 텍스트 구조가 필요합니다.",
            sections=[
                ("쇼츠 설명란이 SEO에 미치는 영향",
                 "<p>유튜브 검색·추천 알고리즘은 영상 메타데이터를 평가합니다. 설명란은 그 중 핵심입니다.</p>"
                 "<ul>"
                 "<li>유튜브 내 검색 노출 (제목 다음으로 영향력 큼)</li>"
                 "<li>구글 검색에서 영상 결과 노출</li>"
                 "<li>외부 사이트로의 트래픽 유도</li>"
                 "<li>연관 영상 추천에 영향</li>"
                 "</ul>"
                 "<p>특히 쇼츠는 시청 시간이 짧아서 \"제목+설명\"이 알고리즘 판단의 큰 비중을 차지합니다.</p>"),
                ("첫 줄 — 핵심 키워드와 클릭 유도",
                 "<p>유튜브는 설명 첫 줄만 미리 노출하고 나머지는 \"더 보기\"로 가립니다. 첫 줄에 다음이 들어가야 합니다.</p>"
                 "<ol>"
                 "<li>핵심 키워드 1개 (영상 주제)</li>"
                 "<li>\"더 보기\"를 펼치게 만드는 후크 (질문·결과 예고)</li>"
                 "</ol>"
                 "<p>예: \"네이버 플레이스 노출 안 되는 진짜 이유 (대부분 이 5가지 중 하나입니다)\"</p>"
                 "<p>\"안녕하세요\"로 시작하지 마세요. 첫 줄은 검색 노출과 클릭률 둘 다에 영향을 줍니다.</p>"),
                ("본문 — 영상 내용 요약과 외부 링크 위치",
                 "<p>본문 구조는 다음 순서가 효과적입니다.</p>"
                 "<ol>"
                 "<li>2~3문장으로 영상 핵심 요약</li>"
                 "<li>본 영상(롱폼)이 있다면 그 링크 (\"전체 가이드는 여기서\")</li>"
                 "<li>관련 외부 사이트 링크 (블로그·서비스 페이지)</li>"
                 "<li>다음 영상 예고·시리즈 안내</li>"
                 "<li>해시태그 3~5개</li>"
                 "</ol>"
                 "<p>외부 링크는 본문 상단에 배치합니다. \"더 보기\"를 한 번 펼친 사용자가 스크롤 없이 바로 보는 위치입니다.</p>"),
                ("해시태그 전략과 함정",
                 "<p>쇼츠 해시태그는 3~5개가 적정입니다. 더 많이 달면 알고리즘이 \"스팸 신호\"로 처리할 수 있습니다.</p>"
                 "<ul>"
                 "<li>핵심 키워드 해시태그 1개 (\"#네이버플레이스\")</li>"
                 "<li>업종/카테고리 해시태그 1~2개</li>"
                 "<li>#shorts 자동 포함</li>"
                 "<li>금지: 영상과 무관한 인기 해시태그</li>"
                 "</ul>"
                 "<p>무관한 해시태그를 달면 잘못된 시청자에게 노출되어 시청 완료율이 떨어집니다. 알고리즘 평가가 부정적이 됩니다.</p>"),
                ("측정 — 쇼츠에서 본 영상·외부 사이트로 이동 비율",
                 "<p>유튜브 분석에서 다음을 추적합니다.</p>"
                 "<ul>"
                 "<li>설명란 클릭률 (\"더 보기\" 펼친 비율)</li>"
                 "<li>외부 링크 클릭 수</li>"
                 "<li>다른 영상으로 이동 (롱폼 본 영상)</li>"
                 "<li>채널 페이지 방문</li>"
                 "</ul>"
                 "<p>전체 시청자 대비 외부 링크 클릭률이 0.5~1%면 평균 수준, 2% 이상이면 설명란이 잘 작동하고 있는 것입니다.</p>"),
                ("주의 — 알고리즘 위반과 채널 페널티",
                 "<p>다음은 채널 단위 패널티 위험이 있습니다.</p>"
                 "<ul>"
                 "<li>영상 내용과 다른 설명·해시태그</li>"
                 "<li>외부 사이트 링크 과다 (여러 개 동시 노출)</li>"
                 "<li>저작권·민감 내용으로 연결되는 링크</li>"
                 "<li>설명란에 키워드 스터핑</li>"
                 "</ul>"
                 "<p>알고리즘이 채널 단위로 평가하므로 한 영상의 문제가 전체 채널 노출에 영향을 줍니다.</p>"),
            ],
            key_takeaways=[
                "쇼츠 설명란 첫 줄에 핵심 키워드와 클릭 후크를 함께 넣습니다.",
                "외부 링크는 본문 상단에 배치해야 \"더 보기\" 펼친 사용자가 바로 봅니다.",
                "해시태그는 3~5개, 영상과 무관한 인기 해시태그는 시청 완료율을 떨어뜨립니다.",
                "외부 링크 클릭률 0.5~1%가 평균, 2% 이상이면 설명란이 잘 작동하는 것입니다.",
            ],
            related=[
                ("인스타그램 프로필 링크 — 링크인바이오 vs 자체 랜딩, 어느 게 SEO에 도움될까", "/insights/sns/instagram-link-in-bio/", "SNS 마케팅"),
                ("쇼핑몰 제품 페이지 본문이 비어있을 때 추가하는 6단락 구조", "/insights/content-seo/product-page-content-structure/", "콘텐츠 SEO"),
                ("SNS 마케팅 서비스", "/services/social-media/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/sns/youtube-shorts-description/",
            title="유튜브 쇼츠 설명란 — 본 영상 페이지로 트래픽 유도하는 텍스트 구조",
            desc="유튜브 쇼츠 설명란의 첫 줄·본문·해시태그 구조와 클릭률 측정.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/sns/instagram-link-in-bio/": {
        "title": "인스타그램 프로필 링크 — 링크인바이오 vs 자체 랜딩, 어느 게 SEO에 도움될까 | OneSearchPro 인사이트",
        "desc": "인스타그램 프로필에 링크인바이오 서비스(Linktree 등)와 자체 랜딩 페이지 중 어느 것을 써야 하나. SEO·UX·트래킹 관점에서 비교.",
        "keywords": "인스타그램 프로필 링크, 링크인바이오, Linktree, 인스타 SEO, SNS 유입",
        "h1": "인스타그램 프로필 링크 — 링크인바이오 vs 자체 랜딩, 어느 게 SEO에 도움될까",
        "eyebrow": "SNS MARKETING · ARTICLE",
        "lead": "인스타그램은 프로필 링크를 단 하나만 허용합니다. Linktree 같은 링크인바이오 서비스를 쓸지, 자체 랜딩페이지를 만들지 결정해야 합니다. SEO·UX·측정 3가지 관점에서 비교합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=6,
            intro="\"링크는 프로필에\"라는 표현이 인스타그램에 자리잡으면서 링크인바이오 서비스가 폭발적으로 성장했습니다. Linktree, Beacons, Linkin.bio 등. 그런데 SEO와 비즈니스 측정 관점에서 보면 의외로 자체 랜딩페이지가 유리한 경우가 많습니다.",
            sections=[
                ("두 선택지의 차이 — UX·SEO·트래킹 관점",
                 "<p><b>링크인바이오:</b> 외부 서비스에 가입, 여러 링크를 한 페이지에 모아 보여줍니다. 별도 도메인.</p>"
                 "<p><b>자체 랜딩페이지:</b> 우리 도메인 안의 /links/ 같은 URL. 직접 디자인·코드 통제.</p>"
                 "<p>UX는 두 가지가 거의 비슷합니다. 차이가 큰 영역은 SEO와 트래킹입니다.</p>"),
                ("링크인바이오 장단점",
                 "<p><b>장점:</b></p>"
                 "<ul>"
                 "<li>5분 안에 셋업 완료</li>"
                 "<li>드래그앤드롭으로 링크 추가·삭제</li>"
                 "<li>모바일 최적화 자동</li>"
                 "<li>일부 서비스는 분석 대시보드 제공</li>"
                 "</ul>"
                 "<p><b>단점:</b></p>"
                 "<ul>"
                 "<li>도메인이 외부 서비스 (linktr.ee/...) — 우리 도메인 권위와 분리</li>"
                 "<li>리다이렉트 단계 추가 — 페이지 로드 살짝 느림</li>"
                 "<li>GA4 통합이 제한적 (서비스마다 다름)</li>"
                 "<li>광고 픽셀 연동 어려움</li>"
                 "<li>서비스 종료·정책 변경 위험</li>"
                 "</ul>"),
                ("자체 랜딩페이지 장단점",
                 "<p><b>장점:</b></p>"
                 "<ul>"
                 "<li>우리 도메인 안 — 모든 트래픽이 도메인 권위에 기여</li>"
                 "<li>GA4·서치콘솔·픽셀 완전 통제</li>"
                 "<li>디자인·UX 자유로움</li>"
                 "<li>SEO 신호 누적 (내부 링크 흐름의 일부)</li>"
                 "<li>외부 서비스 의존성 없음</li>"
                 "</ul>"
                 "<p><b>단점:</b></p>"
                 "<ul>"
                 "<li>최초 셋업에 코드·디자인 작업 필요</li>"
                 "<li>링크 추가·삭제 시 코드 수정 (CMS 사용 시 완화)</li>"
                 "<li>운영 부담 약간 더 큼</li>"
                 "</ul>"),
                ("사용자 유입 데이터 추적 차이",
                 "<p>가장 큰 차이는 데이터입니다. 자체 랜딩페이지의 경우 GA4에서 다음을 추적할 수 있습니다.</p>"
                 "<ul>"
                 "<li>인스타그램 → 랜딩 → 어떤 카드 클릭 → 최종 전환까지의 전체 경로</li>"
                 "<li>UTM 파라미터로 캠페인별 효과 분리</li>"
                 "<li>메타 픽셀로 인스타 광고 리타겟팅 가능</li>"
                 "<li>스크롤 깊이·클릭 히트맵 추가 가능</li>"
                 "</ul>"
                 "<p>링크인바이오는 위 데이터가 부분적이거나 외부 서비스에서만 볼 수 있어 의사결정 속도가 느려집니다.</p>"),
                ("어느 쪽이 답인가 — 비즈니스 단계별",
                 "<p>실무 권장은 다음과 같이 갈립니다.</p>"
                 "<ul>"
                 "<li><b>크리에이터·1인 사업:</b> 링크인바이오 무난. 데이터보다 셋업 속도가 중요.</li>"
                 "<li><b>중소 비즈니스 (월 광고 100만원+):</b> 자체 랜딩페이지. 픽셀·리타겟팅 가치가 큼.</li>"
                 "<li><b>이커머스·전환 중심 비즈니스:</b> 자체 랜딩페이지 거의 필수. 측정·픽셀이 결과를 좌우.</li>"
                 "<li><b>여러 매장 운영:</b> 자체 랜딩페이지에서 매장별 분기 처리.</li>"
                 "</ul>"
                 "<p>핵심 기준은 \"데이터로 의사결정 하는가\"입니다. 데이터를 보고 광고·콘텐츠를 조정하는 단계라면 자체 랜딩이 답입니다.</p>"),
                ("자체 랜딩 만들 때 체크 항목",
                 "<ul>"
                 "<li>URL은 /links/ 또는 /go/ 같이 짧게</li>"
                 "<li>외부 링크에 utm_source=instagram 자동 부여</li>"
                 "<li>GA4 이벤트 추적 (링크별 클릭)</li>"
                 "<li>메타 픽셀, GTM 셋업</li>"
                 "<li>모바일 LCP 1.5초 이하 (인스타에서 들어오는 사용자는 빠른 로딩 기대)</li>"
                 "<li>noindex 설정 (검색 결과에 노출될 필요 없음)</li>"
                 "</ul>"),
            ],
            key_takeaways=[
                "링크인바이오는 셋업이 빠르지만 데이터·픽셀 추적이 제한적입니다.",
                "자체 랜딩페이지는 운영 부담이 약간 더 크지만 측정과 광고 효율이 크게 좋아집니다.",
                "월 광고비 100만원 이상이라면 자체 랜딩페이지 권장.",
                "랜딩페이지는 noindex 처리해서 검색 결과 노이즈를 만들지 마세요.",
            ],
            related=[
                ("유튜브 쇼츠 설명란 — 본 영상 페이지로 트래픽 유도하는 텍스트 구조", "/insights/sns/youtube-shorts-description/", "SNS 마케팅"),
                ("쇼핑몰 제품 페이지 본문이 비어있을 때 추가하는 6단락 구조", "/insights/content-seo/product-page-content-structure/", "콘텐츠 SEO"),
                ("SNS 마케팅 서비스", "/services/social-media/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/sns/instagram-link-in-bio/",
            title="인스타그램 프로필 링크 — 링크인바이오 vs 자체 랜딩, 어느 게 SEO에 도움될까",
            desc="인스타 프로필 링크 두 선택지의 SEO·UX·측정 관점 비교.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    # Visibility category
    "/insights/visibility/301-migration-mistakes/": {
        "title": "사이트 리뉴얼 후 트래픽 절반 — 301 리다이렉트 시 자주 빠뜨리는 12가지 | OneSearchPro 인사이트",
        "desc": "사이트 리뉴얼 후 트래픽이 절반으로 떨어지는 가장 흔한 원인은 301 리다이렉트 매핑 누락입니다. 자주 빠뜨리는 12가지 항목과 출시 후 모니터링 방법.",
        "keywords": "사이트 리뉴얼, 301 리다이렉트, URL 마이그레이션, 트래픽 손실, 리뉴얼 SEO",
        "h1": "사이트 리뉴얼 후 트래픽 절반 — 301 리다이렉트 시 자주 빠뜨리는 12가지",
        "eyebrow": "VISIBILITY · ARTICLE",
        "lead": "리뉴얼 후 트래픽이 절반으로 떨어지면 거의 대부분 301 리다이렉트 매핑에서 빠뜨린 항목이 있습니다. 실무에서 가장 자주 누락되는 12가지를 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=8,
            intro="\"디자이너가 만든 새 사이트로 다 옮겼는데 트래픽이 절반으로 떨어졌어요.\" 이 메시지를 자주 받습니다. 진단해보면 90% 케이스가 301 리다이렉트 매핑 누락입니다. 새 사이트의 디자인이 아무리 좋아도 색인된 옛 URL에서 새 URL로 이어지는 다리가 없으면 트래픽은 사라집니다.",
            sections=[
                ("리뉴얼 트래픽 손실의 진짜 원인",
                 "<p>구글이 기존에 색인한 URL은 \"검색 결과에 노출 중인 자산\"입니다. 그 URL이 갑자기 404가 되면 노출이 즉시 끊깁니다. 새 URL은 색인까지 시간이 걸리므로 그 사이에 트래픽 공백이 생깁니다.</p>"
                 "<p>301 리다이렉트는 \"이 옛 주소는 이제 이 새 주소로 봐달라\"는 신호입니다. 매핑이 정확하면 트래픽·권위가 거의 그대로 이전됩니다. 매핑이 빠지면 모든 게 끊깁니다.</p>"),
                ("매핑 작업 시 자주 빠뜨리는 항목 1~4",
                 "<ol>"
                 "<li><b>https → https 매핑은 했지만 http → https 매핑 누락:</b> 옛 사이트가 http였다면 두 가지 모두 처리.</li>"
                 "<li><b>www 유무 매핑 누락:</b> www.example.com과 example.com 양쪽 모두.</li>"
                 "<li><b>대소문자 URL:</b> /Page와 /page를 다르게 인식하는 서버에서 양쪽 모두 매핑.</li>"
                 "<li><b>슬래시 유무:</b> /page와 /page/ 양쪽 모두 매핑.</li>"
                 "</ol>"
                 "<p>이 4가지만 빠뜨려도 트래픽의 20~30%가 사라집니다.</p>"),
                ("자주 빠뜨리는 항목 5~8",
                 "<ol start=\"5\">"
                 "<li><b>파라미터 URL:</b> ?utm_source=, ?ref= 등이 붙은 URL도 매핑 대상.</li>"
                 "<li><b>이미지 URL:</b> 이미지 검색에서 들어오는 트래픽도 무시 못 함. 이미지 경로도 매핑.</li>"
                 "<li><b>PDF·다운로드 파일:</b> /files/guide.pdf 같은 비-HTML 자원.</li>"
                 "<li><b>피드 URL:</b> /rss/, /feed/ 같은 구독자 URL.</li>"
                 "</ol>"),
                ("자주 빠뜨리는 항목 9~12",
                 "<ol start=\"9\">"
                 "<li><b>다국어 hreflang URL:</b> /en/, /ko/ 등 다국어 경로 양쪽 모두.</li>"
                 "<li><b>페이지네이션 URL:</b> /blog/page/2/ 같은 페이지네이션도 매핑 대상.</li>"
                 "<li><b>카테고리·태그 URL:</b> /category/seo/, /tag/keyword/ 등.</li>"
                 "<li><b>외부에서 들어오는 백링크 URL:</b> 옛 보도자료·블로그 글이 가리키는 정확한 URL.</li>"
                 "</ol>"
                 "<p>특히 12번 항목이 중요합니다. 외부 백링크가 가리키는 URL을 매핑해야 \"권위 신호\"가 새 사이트로 이전됩니다.</p>"),
                ("출시 후 모니터링 매뉴얼",
                 "<p>출시 첫 4주는 다음을 매일 점검합니다.</p>"
                 "<ul>"
                 "<li>서치콘솔 \"커버리지\" 리포트의 404 증가 여부</li>"
                 "<li>서치콘솔 \"크롤링 통계\"에서 응답 코드 분포</li>"
                 "<li>GA4의 신규 페이지 트래픽 분포</li>"
                 "<li>주요 키워드 순위 (Ahrefs·SEMrush)</li>"
                 "</ul>"
                 "<p>404가 갑자기 늘어나면 즉시 그 URL들을 매핑에 추가하고 sitemap 재제출. 첫 2주의 빠른 대응이 회복 속도를 결정합니다.</p>"),
                ("주의 — 리다이렉트 체인의 위험",
                 "<p>301 → 301 → 301로 이어지는 \"리다이렉트 체인\"이 길어지면 권위 신호가 약해지고 페이지 속도가 느려집니다. 매핑 시 항상 \"옛 URL → 최종 새 URL\" 1단계로 직접 매핑하세요.</p>"
                 "<p>또한 무한 루프(/a → /b → /a)는 페이지가 아예 안 열리니 출시 전 자동 검증 도구로 모든 매핑을 테스트해야 합니다.</p>"),
            ],
            key_takeaways=[
                "리뉴얼 후 트래픽 손실의 90%는 301 매핑 누락에서 발생합니다.",
                "http/www/대소문자/슬래시 변형, 파라미터·이미지·PDF·피드·페이지네이션을 모두 점검하세요.",
                "외부 백링크가 가리키는 정확한 URL 매핑이 권위 신호 이전에 가장 중요합니다.",
                "출시 첫 4주는 매일 404 증가와 키워드 순위를 모니터링해야 합니다.",
            ],
            related=[
                ("서치콘솔 \"크롤링됨 - 현재 색인되지 않음\" — 다른 상태와의 차이와 대응법", "/insights/visibility/crawled-not-indexed/", "검색 노출"),
                ("워드프레스 사이트 LCP 4초 → 1.5초로 줄인 실제 작업 순서", "/insights/technical-seo/wordpress-lcp-fix/", "기술 SEO"),
                ("SEO 웹사이트 제작 서비스", "/services/web-design/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/visibility/301-migration-mistakes/",
            title="사이트 리뉴얼 후 트래픽 절반 — 301 리다이렉트 시 자주 빠뜨리는 12가지",
            desc="사이트 리뉴얼 시 301 매핑에서 자주 누락되는 12가지 항목과 모니터링.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/visibility/crawled-not-indexed/": {
        "title": "서치콘솔 '크롤링됨 - 현재 색인되지 않음' — 다른 상태와의 차이와 대응법 | OneSearchPro 인사이트",
        "desc": "서치콘솔 색인 커버리지에서 '크롤링됨 - 현재 색인되지 않음' 메시지가 의미하는 것, '발견됨'과의 차이, 색인 거부의 5가지 원인.",
        "keywords": "크롤링됨 현재 색인되지 않음, Crawled currently not indexed, 색인 거부, 서치콘솔",
        "h1": "서치콘솔 \"크롤링됨 - 현재 색인되지 않음\" — 다른 상태와의 차이와 대응법",
        "eyebrow": "VISIBILITY · ARTICLE",
        "lead": "구글이 페이지를 가져갔는데 색인을 안 시키는 상태입니다. \"발견됨 - 색인되지 않음\"과는 완전히 다른 단계의 문제이고, 대응법도 다릅니다. 흔한 원인 5가지와 단계적 개선 방법을 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=8,
            intro="\"크롤링됨 - 현재 색인되지 않음\"은 가장 답답한 메시지입니다. 구글이 페이지를 가져갔으니 기술적 문제는 아니지만, 그럼에도 색인 안 시킨다는 건 \"이 페이지는 색인 가치가 없다\"는 신호입니다. 5가지 원인을 짚어봅니다.",
            sections=[
                ("\"크롤링됨\"의 의미 — 발견됨과의 차이",
                 "<p>두 상태를 다시 짧게 정리합니다.</p>"
                 "<ul>"
                 "<li><b>발견됨 - 색인되지 않음:</b> URL을 알지만 아직 가져가지 않음. 크롤링 예산·신뢰도 문제일 가능성.</li>"
                 "<li><b>크롤링됨 - 색인되지 않음:</b> 가져갔지만 색인 가치를 못 느낌. 콘텐츠 품질·중복·E-E-A-T 문제 가능성.</li>"
                 "</ul>"
                 "<p>\"크롤링됨\" 단계 문제는 기술 SEO보다 콘텐츠 SEO에서 답을 찾아야 하는 경우가 많습니다.</p>"),
                ("색인 거부의 원인 1·2 — 콘텐츠 품질, 중복 콘텐츠",
                 "<p><b>콘텐츠 품질 부족:</b> 본문이 너무 짧거나, 다른 데서 본 정보의 재정리거나, 사용자에게 새로운 가치가 없는 경우. 구글의 Helpful Content System이 \"색인 가치 없음\"으로 판단합니다.</p>"
                 "<p><b>중복 콘텐츠:</b> 같은 사이트 내 다른 페이지와 본문이 유사하거나, 외부 사이트와 유사한 경우. 구글은 \"이미 비슷한 페이지가 있으니 안 색인\" 판단을 합니다.</p>"
                 "<p>점검 방법: 페이지 본문의 50~100자를 따옴표로 묶어 구글에 검색. 같은 문구를 가진 페이지가 여럿 나오면 중복 가능성.</p>"),
                ("원인 3·4 — 검색 의도 미스매치, 페이지 가치 부족",
                 "<p><b>검색 의도 미스매치:</b> 타겟 키워드의 검색 의도와 페이지 내용이 다른 경우. 예: \"○○ 가격\" 검색에 답하는 페이지에 가격이 안 나오는 경우.</p>"
                 "<p><b>페이지 가치 부족:</b> 카테고리 페이지·태그 페이지·페이지네이션 같이 \"링크 모음\"만 있는 경우. 본문 없이 카드 나열만 있으면 색인 가치 평가가 낮음.</p>"),
                ("원인 5 — 사이트 전체 신뢰도가 낮은 경우",
                 "<p>개별 페이지는 괜찮은데 사이트 전체 평가가 낮으면 색인 우선순위가 떨어집니다. 신호:</p>"
                 "<ul>"
                 "<li>도메인 권위(DR) 매우 낮음</li>"
                 "<li>옛 글 가지치기 안 됨 (트래픽 0인 글 다량 존재)</li>"
                 "<li>E-E-A-T 신호 부족 (저자·연락처·정책 페이지 빈약)</li>"
                 "<li>외부 백링크 거의 없음</li>"
                 "</ul>"
                 "<p>이 경우 개별 페이지를 고쳐도 잘 안 됩니다. 사이트 전체 신뢰 신호를 같이 끌어올려야 합니다.</p>"),
                ("단계적 개선과 재요청",
                 "<p>대응은 다음 순서로 진행합니다.</p>"
                 "<ol>"
                 "<li><b>본문 보강:</b> 페이지에 실제 가치 추가 (사용자 질문에 답, 새로운 데이터, 구체 예시).</li>"
                 "<li><b>내부 링크:</b> 권위 있는 페이지에서 이 페이지로 본문 내 텍스트 링크.</li>"
                 "<li><b>중복 정리:</b> 유사 페이지 통합 또는 canonical 설정.</li>"
                 "<li><b>서치콘솔 \"색인 요청\":</b> URL 검사 → 색인 요청 (개선 후에만).</li>"
                 "<li><b>2~4주 관찰:</b> 색인되면 성공. 안 되면 추가 개선 필요.</li>"
                 "</ol>"),
                ("주의 — 무리한 색인 요청과 패널티",
                 "<p>같은 페이지를 매일 색인 요청하거나, 본문 거의 안 바꾸고 반복 요청하면 서치콘솔에서 요청 자체가 제한됩니다. 변화 없이는 요청 안 하는 게 안전합니다.</p>"
                 "<p>또한 \"색인 안 되는 페이지\"가 사이트의 50% 이상이라면 개별 페이지 대응으로는 부족합니다. HCS·E-E-A-T 차원의 전면 점검이 필요한 시점입니다.</p>"),
            ],
            key_takeaways=[
                "\"크롤링됨 - 색인되지 않음\"은 콘텐츠 가치 평가에서 떨어진 상태입니다.",
                "가장 흔한 원인은 콘텐츠 품질·중복 콘텐츠·검색 의도 미스매치입니다.",
                "사이트의 50%+ 가 이 상태면 개별 대응이 아닌 사이트 전체 신뢰 신호 점검이 필요합니다.",
                "본문 보강 없이 색인 요청만 반복하면 서치콘솔이 요청을 제한할 수 있습니다.",
            ],
            related=[
                ("서치콘솔 \"발견됨 - 현재 색인되지 않음\" 7가지 원인과 진단 순서", "/insights/technical-seo/discovered-not-indexed/", "기술 SEO"),
                ("Helpful Content System 셀프 점검 — 한국 사이트가 자주 떨어지는 7가지 질문", "/insights/google-seo/helpful-content-self-check/", "구글 SEO"),
                ("기술 SEO 진단 서비스", "/services/technical-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/visibility/crawled-not-indexed/",
            title="서치콘솔 \"크롤링됨 - 현재 색인되지 않음\" — 다른 상태와의 차이와 대응법",
            desc="\"크롤링됨 - 색인되지 않음\" 메시지의 5가지 원인과 단계적 개선법.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },
}

for path, p in PAGES.items():
    out_dir = ROOT / path.strip("/")
    out_dir.mkdir(parents=True, exist_ok=True)
    html = page(
        path=path,
        title=p["title"],
        desc=p["desc"],
        keywords=p["keywords"],
        h1=p["h1"],
        eyebrow=p["eyebrow"],
        lead=p["lead"],
        body=p["body"],
        json_ld=p.get("json_ld", ""),
        active=p.get("active", "svc"),
    )
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"wrote {path}index.html")

print("done")

#!/usr/bin/env python3
"""Generate remaining service & company pages from a shared template."""
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
SITE = "https://onesearchpro.org"

HEADER = '''<header class="site-header">
    <div class="container nav-wrap">
      <a href="/" class="brand" aria-label="OneSearchPro 홈"><picture><source type="image/webp" srcset="/assets/images/logo-140.webp 1x, /assets/images/logo-280.webp 2x" /><img src="/assets/images/logo-140.png" alt="OneSearchPro - 검색의 기준을 바꾸다" class="brand-logo" width="180" height="60" decoding="async" /></picture></a>
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
            <a href="/about/team/">팀 · 저자 소개</a>
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
      <div><h5>연락처</h5><ul><li>contact@onesearchpro.com</li><li>인천 부평구</li></ul></div>
      <div><h5>약관·정책</h5><ul><li><a href="/privacy/">개인정보처리방침</a></li><li><a href="/terms/">이용약관</a></li><li><a href="/sitemap-html/">사이트맵</a></li><li><a href="/rss.xml">RSS 피드</a></li></ul></div>
    </div>
    <div class="container biz-info">
      <span>상호 <b>YH기획</b></span>
      <span class="biz-sep">·</span>
      <span>사업자등록번호 503-30-66944</span>
      <span class="biz-sep">·</span>
      <span>주소 인천광역시 부평구 부평대로 283 부평우림라이온스밸리</span>
    </div>
    <div class="container footer-sns">
      <span class="footer-sns-label">Follow OneSearchPro</span>
      <div class="footer-sns-icons">
        <a href="https://www.linkedin.com/in/%EB%B0%B1%ED%98%B8-%EA%B0%95-a84273261/" target="_blank" rel="noopener noreferrer me" aria-label="LinkedIn"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg></a>
        <a href="https://medium.com/@88smartbro88" target="_blank" rel="noopener noreferrer me" aria-label="Medium"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M13.54 12a6.8 6.8 0 01-6.77 6.82A6.8 6.8 0 010 12a6.8 6.8 0 016.77-6.82A6.8 6.8 0 0113.54 12zM20.96 12c0 3.54-1.51 6.42-3.38 6.42-1.87 0-3.39-2.88-3.39-6.42s1.52-6.42 3.39-6.42 3.38 2.88 3.38 6.42M24 12c0 3.17-.53 5.75-1.19 5.75-.66 0-1.19-2.58-1.19-5.75s.53-5.75 1.19-5.75C23.47 6.25 24 8.83 24 12z"/></svg></a>
        <a href="https://x.com/gugeulmake84173" target="_blank" rel="noopener noreferrer me" aria-label="X (Twitter)"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
        <a href="https://t.me/googleseolab" target="_blank" rel="noopener noreferrer me" aria-label="Telegram"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.14.18-.357.295-.6.295l.213-3.053 5.56-5.022c.24-.213-.054-.334-.373-.121l-6.869 4.326-2.96-.924c-.64-.203-.66-.643.135-.953l11.566-4.458c.538-.196 1.006.128.832.938z"/></svg></a>
      </div>
    </div>
    <div class="container foot-bottom"><span>© <span id="year"></span> YH기획 (OneSearchPro). All rights reserved.</span><span><a href="/privacy/">개인정보처리방침</a> · <a href="/terms/">이용약관</a></span></div>
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
    breadcrumb_trail = []  # list of (name, url) for JSON-LD
    if path.startswith("/services/") and path != "/services/":
        breadcrumb_trail = [("홈", "/"), ("서비스", "/services/seo/"), (h1, path)]
        breadcrumb_html = f'<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <a href="/services/seo/">서비스</a> <span>›</span> <span>{h1}</span></div></nav>'
    elif path == "/about/":
        breadcrumb_trail = [("홈", "/"), ("회사소개", path)]
        breadcrumb_html = '<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <span>회사소개</span></div></nav>'
    elif path.startswith("/about/") and path != "/about/":
        breadcrumb_trail = [("홈", "/"), ("회사소개", "/about/"), (h1, path)]
        breadcrumb_html = f'<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <a href="/about/">회사소개</a> <span>›</span> <span>{h1}</span></div></nav>'
    elif path == "/contact/":
        breadcrumb_trail = [("홈", "/"), ("내 사이트 진단받기", path)]
        breadcrumb_html = '<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <span>내 사이트 진단받기</span></div></nav>'
    elif path == "/case-studies/":
        breadcrumb_trail = [("홈", "/"), ("성공사례", path)]
        breadcrumb_html = '<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <span>성공사례</span></div></nav>'
    elif path.startswith("/case-studies/") and path != "/case-studies/":
        breadcrumb_trail = [("홈", "/"), ("성공사례", "/case-studies/"), (h1, path)]
        breadcrumb_html = f'<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <a href="/case-studies/">성공사례</a> <span>›</span> <span>{h1}</span></div></nav>'
    elif path == "/insights/":
        breadcrumb_trail = [("홈", "/"), ("SEO 인사이트", path)]
        breadcrumb_html = '<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <span>SEO 인사이트</span></div></nav>'
    elif path.startswith("/insights/") and path != "/insights/":
        breadcrumb_trail = [("홈", "/"), ("SEO 인사이트", "/insights/"), (h1, path)]
        breadcrumb_html = f'<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <a href="/insights/">SEO 인사이트</a> <span>›</span> <span>{h1}</span></div></nav>'
    elif path == "/privacy/":
        breadcrumb_trail = [("홈", "/"), ("개인정보처리방침", path)]
        breadcrumb_html = '<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <span>개인정보처리방침</span></div></nav>'
    elif path == "/terms/":
        breadcrumb_trail = [("홈", "/"), ("이용약관", path)]
        breadcrumb_html = '<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <span>이용약관</span></div></nav>'
    elif path == "/sitemap-html/":
        breadcrumb_trail = [("홈", "/"), ("사이트맵", path)]
        breadcrumb_html = '<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <span>사이트맵</span></div></nav>'

    # BreadcrumbList JSON-LD 자동 생성
    breadcrumb_jsonld = ""
    if breadcrumb_trail:
        items = []
        for i, (name, url) in enumerate(breadcrumb_trail, 1):
            full_url = f"{SITE}{url}"
            items.append(f'{{"@type":"ListItem","position":{i},"name":"{name}","item":"{full_url}"}}')
        breadcrumb_jsonld = f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{",".join(items)}]}}</script>'

    # 모든 페이지에 공통 적용되는 사이트 차원 JSON-LD
    # sameAs: 구글 Knowledge Panel·E-E-A-T Authoritativeness 신호
    site_wide_jsonld = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"OneSearchPro","alternateName":"원서치프로","url":"https://onesearchpro.org/","inLanguage":"ko-KR","publisher":{"@type":"Organization","name":"OneSearchPro","legalName":"YH기획"}}</script><script type="application/ld+json">{"@context":"https://schema.org","@type":"LocalBusiness","name":"YH기획 (OneSearchPro)","alternateName":"OneSearchPro","url":"https://onesearchpro.org/","logo":"https://onesearchpro.org/assets/images/logo.png","image":"https://onesearchpro.org/assets/images/logo.png","telephone":"","email":"contact@onesearchpro.com","priceRange":"₩₩","address":{"@type":"PostalAddress","streetAddress":"부평대로 283 부평우림라이온스밸리","addressLocality":"부평구","addressRegion":"인천광역시","postalCode":"21389","addressCountry":"KR"},"areaServed":"KR","taxID":"503-30-66944","sameAs":["https://www.linkedin.com/in/%EB%B0%B1%ED%98%B8-%EA%B0%95-a84273261/","https://medium.com/@88smartbro88","https://x.com/gugeulmake84173","https://t.me/googleseolab"]}</script>'''

    # 페이지 본문 내에 자체 CTA가 있는 페이지는 글로벌 CTA를 생략 (중복 방지)
    has_own_cta = path in {
        "/case-studies/seo/",
        "/case-studies/local-seo/",
        "/case-studies/content/",
        "/case-studies/web-design/",
        "/case-studies/visibility/",
    }
    global_cta_html = "" if has_own_cta else '''<section class="section section-cta">
      <div class="container cta-grid">
        <div><h2>무료 진단 후 정확한 견적을 받아보세요</h2><p>24시간 내 분석 리포트와 맞춤 제안서를 보내드립니다.</p></div>
        <div class="cta-actions"><a href="https://t.me/googleseolab" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-lg">무료 진단 신청 →</a><a href="/case-studies/" class="btn btn-outline btn-lg btn-light">성공사례 보기</a></div>
      </div>
    </section>'''

    # 책임자 미니 바이라인 — 비블로그 페이지의 E-E-A-T Authoritativeness 신호
    # 블로그 글은 이미 본문 상단에 바이라인이 있으므로 제외
    is_byline_target = (
        path.startswith("/services/")
        or path.startswith("/case-studies/")
        or (path.startswith("/about/") and path not in {"/about/", "/about/team/"})
    )
    page_byline_html = ""
    if is_byline_target:
        page_byline_html = (
            '<div class="container"><aside class="page-byline">'
            '<span class="page-byline-label">이 페이지의 책임 컨설턴트</span>'
            '<a href="/about/team/" rel="author" class="page-byline-author">'
            '<span class="page-byline-avatar">👤</span>'
            '<span><b>강백호</b> · OneSearchPro 대표</span>'
            '</a>'
            '<span class="page-byline-note">SEO·디지털 마케팅 실무 10년+, 페널티 사례 0건 화이트햇 원칙. '
            '<a href="/about/team/">저자 프로필 보기 →</a></span>'
            '</aside></div>'
        )

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
  <link rel="alternate icon" type="image/png" href="/assets/images/favicon-32.png" />
  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png" />
  <link rel="alternate" type="application/rss+xml" title="OneSearchPro · SEO 인사이트" href="/rss.xml" />
  <meta name="theme-color" content="#7c5cff" />
  <!-- 검색엔진 소유권 인증 (등록 시 코드 입력) -->
  <meta name="google-site-verification" content="kAFnt3jSs27vJ3oCex9SwynDq07pqYXZmVtITkFZBPQ" />
  <meta name="naver-site-verification" content="eb0c4d732c1b024809d2ab52ff1ea457bb9189dc" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" as="image" href="/assets/images/logo-140.webp" type="image/webp" fetchpriority="high" />
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap" media="print" onload="this.media='all'" />
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap" /></noscript>
  <link rel="stylesheet" href="/styles.css" />
  {site_wide_jsonld}
  {breadcrumb_jsonld}
  {json_ld}
</head>
<body class="{body_class}">
  <div class="reading-progress" id="readingProgress"></div>
  {header}
  {breadcrumb_html}
  <main>
    {hero_html}
    {body}
    {page_byline_html}
    {global_cta_html}
  </main>
  {FOOTER}
  <script src="/script.js" defer></script>
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


def case_card(*, badge, icon, h3, problem, diagnosis, improvements, results, caveats,
              tools=None, verification=None, comment=None, insight=None, checklist=None,
              related_service=None, related_insight=None):
    """사례 카드. tools/verification/comment/insight/checklist/related_service/related_insight 는 E-E-A-T 보강용 (선택)."""
    imp_list = "".join(f"<li>{x}</li>" for x in improvements)
    res_list = "".join(f"<li>{x}</li>" for x in results)

    eeat_html = ""
    if tools or comment or insight or checklist or related_service:
        tools_html = ""
        if tools:
            tools_items = "".join(f"<li>{t}</li>" for t in tools)
            tools_html = f'<div class="case-eeat-item"><h5>🔧 사용한 도구</h5><ul>{tools_items}</ul></div>'

        verification_html = ""
        if verification:
            verification_html = f'<div class="case-eeat-item"><h5>✅ 작업 후 확인 방식</h5><p>{verification}</p></div>'

        comment_html = ""
        if comment:
            comment_html = f'<div class="case-eeat-item"><h5>💬 담당자 코멘트</h5><blockquote>{comment}</blockquote></div>'

        insight_html = ""
        if insight:
            insight_html = f'<div class="case-eeat-item case-eeat-insight"><h5>💡 이 사례에서 얻은 인사이트</h5><p>{insight}</p></div>'

        checklist_html = ""
        if checklist:
            items = "".join(f"<li>{c}</li>" for c in checklist)
            checklist_html = f'<div class="case-eeat-checklist"><h5>🔍 비슷한 문제가 있다면 확인할 것</h5><ul>{items}</ul></div>'

        related_html = ""
        if related_service or related_insight:
            link_items = []
            if related_service:
                link_items.append(f'<div class="case-eeat-related-item"><a href="{related_service[1]}">{related_service[0]}</a> <span class="case-eeat-related-type">(서비스)</span></div>')
            if related_insight:
                link_items.append(f'<div class="case-eeat-related-item"><a href="{related_insight[1]}">{related_insight[0]}</a> <span class="case-eeat-related-type">(인사이트)</span></div>')
            related_inner = "".join(link_items)
            related_html = f'<div class="case-eeat-related"><h5>🔗 관련 페이지</h5>{related_inner}</div>'

        eeat_html = (
            f'<div class="case-eeat-block">'
            f'<div class="case-eeat-grid">{tools_html}{verification_html}{comment_html}{insight_html}</div>'
            f'{checklist_html}{related_html}'
            f'</div>'
        )

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
        f'{eeat_html}'
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
    # Placeholder 카드는 Helpful Content System의 사이트 단위 평가에 부정 신호로 작용하므로,
    # 실제 글이 발행되어 insight_article_card 로 교체되기 전까지는 렌더링하지 않는다.
    return ""


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


def blog_post(*, date, reading_time, author="강백호", author_url="/about/team/", date_modified=None, intro, sections, key_takeaways=None, related=None):
    """블로그 글 본문 HTML을 생성합니다.
    sections: list of (h2, html_content) tuples
    key_takeaways: 글 끝부분에 들어가는 요약 리스트 (optional)
    related: list of (title, url, badge) tuples - 내부 링크용
    date_modified: 발행 후 본문이 실제 수정된 경우의 최종 갱신일 (Freshness 신호)
    """
    # date_modified가 발행일과 다를 때만 표기하여 redundancy 회피
    modified_html = ""
    if date_modified and date_modified != date:
        modified_html = f'<span>🔄 마지막 업데이트 <time datetime="{date_modified}">{date_modified}</time></span>'
    # 저자 바이라인은 Person 프로필 페이지로 링크 (E-E-A-T Authoritativeness)
    meta = (
        f'<div class="article-meta">'
        f'<span>📅 발행 <time datetime="{date}">{date}</time></span>'
        f'{modified_html}'
        f'<span>⏱ 읽는 시간 약 {reading_time}분</span>'
        f'<span>✍ <a href="{author_url}" rel="author">{author}</a> · OneSearchPro</span>'
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


def blog_jsonld(*, url, title, desc, date_published, date_modified=None, author_name="강백호", author_url="https://onesearchpro.org/about/team/"):
    date_modified = date_modified or date_published
    # author는 Person + Organization 배열로 표기 (E-E-A-T Authoritativeness 신호 강화)
    return (
        f'<script type="application/ld+json">'
        f'{{"@context":"https://schema.org","@type":"BlogPosting",'
        f'"headline":"{title}",'
        f'"description":"{desc}",'
        f'"url":"{url}",'
        f'"datePublished":"{date_published}",'
        f'"dateModified":"{date_modified}",'
        f'"author":[{{"@type":"Person","name":"{author_name}","url":"{author_url}"}},'
        f'{{"@type":"Organization","name":"OneSearchPro","url":"https://onesearchpro.org/"}}],'
        f'"publisher":{{"@type":"Organization","name":"OneSearchPro","logo":{{"@type":"ImageObject","url":"https://onesearchpro.org/assets/images/logo.png"}}}},'
        f'"image":"https://onesearchpro.org/assets/images/logo.png",'
        f'"mainEntityOfPage":{{"@type":"WebPage","@id":"{url}"}},'
        f'"inLanguage":"ko-KR"}}'
        f'</script>'
    )


PAGES = {
    "/services/seo/": {
        "title": "SEO 컨설팅 | 통합 SEO 진단·개선 - OneSearchPro",
        "desc": "검색 노출이 안 되는 원인을 사이트 구조·콘텐츠·기술 요소까지 통합 진단·개선하는 SEO 컨설팅 대표 서비스. 화이트햇 방식·투명한 리포트.",
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
        "title": "지역 SEO 서비스 | 구글맵·플레이스 | OneSearchPro",
        "desc": "GBP·네이버 플레이스·지역 디렉토리·리뷰 관리를 통합 운영하는 지역 SEO 서비스. 오프라인 매장의 지역 검색 노출 강화.",
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
        "title": "SNS 마케팅 | 인스타·유튜브·틱톡 - OneSearchPro",
        "desc": "인스타그램·유튜브·틱톡·네이버 채널 운영. SEO 외부 유입과 브랜드 신뢰를 보조하는 SNS 마케팅 서비스.",
        "keywords": "SNS 마케팅, 소셜미디어마케팅, 인스타그램마케팅, 유튜브마케팅, 틱톡마케팅, 네이버 채널",
        "h1": "SNS 마케팅 서비스",
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
        "title": "기업 마케팅 | B2B·B2C 통합 - OneSearchPro",
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
        "title": "SEO 웹사이트 제작 | 반응형 SEO 사이트 - OneSearchPro",
        "desc": "처음부터 검색엔진 친화 구조·메타·스키마·속도로 설계하는 SEO 웹사이트 제작. 기초 SEO 공사 완료 상태로 납품.",
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
                        {"icon":"⚡","h":"속도 최적화","p":"Core Web Vitals 90점+ 기준 점검."},
                        {"icon":"📱","h":"반응형 디자인","p":"모든 디바이스 완벽 대응."},
                        {"icon":"🔍","h":"SEO 셋업","p":"메타·OG·sitemap·robots·스키마 마크업."},
                        {"icon":"📊","h":"분석 연동","p":"GA4, GTM, 서치콘솔, 픽셀 연동."},
                    ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","serviceType":"Web Design & Development","provider":{"@type":"Organization","name":"OneSearchPro"}}</script>',
    },

    "/about/": {
        "title": "회사 소개 | OneSearchPro - SEO 마케팅 에이전시",
        "desc": "OneSearchPro는 서울에 거점을 둔 SEO·디지털 마케팅 전문 에이전시입니다. 화이트햇 방식과 투명한 데이터로 180+ 프로젝트를 성공시킨 작업 원칙과 프로세스를 소개합니다.",
        "keywords": "OneSearchPro, 원서치프로, SEO 에이전시, 마케팅 에이전시, 작업 원칙, 진행 프로세스, 서울",
        "h1": "원서치프로 소개",
        "eyebrow": "ABOUT ONESEARCHPRO",
        "lead": "OneSearchPro(원서치프로)는 검색에서 시작되는 비즈니스 성장을 만듭니다. 서울에 거점을 두고 SEO·디지털 마케팅을 제공하며, 단기 트릭이 아닌 정공법으로 검색 자산을 누적시키는 것을 원칙으로 합니다.",
        "body": (
            # 책임 저자 prominent 카드 — E-E-A-T Authoritativeness 신호 (회사 소개 페이지 최상단)
            '<section class="section"><div class="container">'
            '<div class="lead-author-card">'
            '<div class="lead-author-avatar">👤</div>'
            '<div class="lead-author-body">'
            '<span class="eyebrow">LEAD AUTHOR & FOUNDER</span>'
            '<h2 style="margin: 0.5rem 0 0.75rem;">강백호 · OneSearchPro 운영자</h2>'
            '<p>SEO·디지털 마케팅 실무 10년+. 구글 코어 업데이트와 Helpful Content System 대응, 한국형 네이버·구글 동시 워크플로우 설계를 직접 담당합니다. OneSearchPro의 모든 SEO 인사이트 글과 컨설팅 작업의 1차 책임자입니다.</p>'
            '<div class="cta-row" style="margin-top: 1rem;">'
            '<a href="/about/team/" rel="author" class="btn btn-primary">저자 상세 프로필 →</a>'
            '<a href="https://www.linkedin.com/in/%EB%B0%B1%ED%98%B8-%EA%B0%95-a84273261/" target="_blank" rel="noopener noreferrer me" class="btn btn-outline">LinkedIn</a>'
            '</div>'
            '</div>'
            '</div>'
            '</div></section>' +

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

            '<section class="section"><div class="container"><div class="section-head left"><span class="eyebrow">COMPANY INFO</span><h2>사업자 정보</h2><p>OneSearchPro는 YH기획이 운영하는 SEO·디지털 마케팅 브랜드입니다.</p></div><div class="company-info"><dl><dt>상호</dt><dd>YH기획</dd><dt>브랜드</dt><dd>OneSearchPro (원서치프로)</dd><dt>사업자등록번호</dt><dd>503-30-66944</dd><dt>주소</dt><dd>인천광역시 부평구 부평대로 283 부평우림라이온스밸리</dd><dt>이메일</dt><dd><a href="mailto:contact@onesearchpro.com">contact@onesearchpro.com</a></dd><dt>문의 채널</dt><dd>텔레그램 <a href="https://t.me/googleseolab" target="_blank" rel="noopener noreferrer">@googleseolab</a></dd></dl></div></div></section>' +

            '<section class="section" id="faq-anchor"><a id="faq"></a><div class="container faq-wrap"><div class="section-head left"><span class="eyebrow">FAQ</span><h2>자주 묻는 질문</h2></div><div class="faq">'
            '<details open><summary>SEO 효과는 언제부터 나타나나요?</summary><p>키워드 난이도와 사이트 상태에 따라 다르지만, 일반적으로 온페이지 개선은 4~8주, 외부 신호 누적 효과는 8~16주, 안정적인 상위 노출은 3~6개월 이후입니다. 무료 진단 단계에서 예상 타임라인을 함께 제시합니다.</p></details>'
            '<details><summary>"무조건 구글 1위 보장"이 가능한가요?</summary><p>가능하지 않습니다. 검색 결과는 구글 알고리즘이 결정하며, 어떤 에이전시도 순위를 보장할 수 없습니다. OneSearchPro는 보장 대신 진단 결과와 예상 시나리오, 작업 범위를 사전에 명시합니다.</p></details>'
            '<details><summary>월 비용은 얼마부터 시작하나요?</summary><p>서비스 종류와 사이트 규모에 따라 다릅니다. SEO 컨설팅은 월 단위 리테이너, 기술 SEO 진단은 일회성 진단도 가능합니다. 정확한 견적은 무료 진단 후 사이트 상태에 맞춰 맞춤 제안드립니다.</p></details>'
            '<details><summary>계약 기간은 어떻게 되나요?</summary><p>기본 3개월 단위 계약을 권장하지만, 1~2개월 시범 운영도 가능합니다. SEO는 누적 효과가 핵심이므로 6개월 이상 진행 시 가장 좋은 ROI가 나옵니다.</p></details>'
            '<details><summary>이전 대행사가 사용한 백링크가 위험할 수 있나요?</summary><p>가능합니다. 디지털 PR·백링크 진단 서비스로 기존 백링크를 전수 점검해 스팸·페널티 위험 링크를 식별하고, 필요 시 disavow 작업까지 진행합니다.</p></details>'
            '<details><summary>네이버 SEO도 함께 해주시나요?</summary><p>네. 구글과 네이버는 알고리즘이 다르므로 분리된 전략이 필요합니다. 통합 SEO 컨설팅에는 두 검색엔진 동시 대응이 포함됩니다.</p></details>'
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"AboutPage","name":"원서치프로 소개","url":"https://onesearchpro.org/about/","mainEntity":{"@type":"Organization","name":"OneSearchPro","alternateName":["원서치프로","YH기획"],"legalName":"YH기획","url":"https://onesearchpro.org/","logo":"https://onesearchpro.org/assets/images/logo.png","description":"SEO·디지털 마케팅 전문 에이전시","taxID":"503-30-66944","address":{"@type":"PostalAddress","streetAddress":"부평대로 283 부평우림라이온스밸리","addressLocality":"부평구","addressRegion":"인천광역시","addressCountry":"KR"},"email":"contact@onesearchpro.com","sameAs":["https://www.linkedin.com/in/%EB%B0%B1%ED%98%B8-%EA%B0%95-a84273261/","https://medium.com/@88smartbro88","https://x.com/gugeulmake84173","https://t.me/googleseolab"]}}</script>',
        "active": "about",
    },

    "/services/technical-seo/": {
        "title": "기술 SEO 진단 | 기술 SEO 점검 - OneSearchPro",
        "desc": "색인·robots·sitemap·canonical·CWV·모바일·중복 URL·구조화 데이터까지 100+ 항목 점검. 코드 레벨 개선 실행 가능한 기술 SEO 진단.",
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
        "title": "콘텐츠 SEO | 키워드·H태그·E-E-A-T - OneSearchPro",
        "desc": "키워드 설계·H태그 구조·검색 의도·E-E-A-T 기반 콘텐츠 개선·블로그 전략을 통합한 콘텐츠 SEO 서비스.",
        "keywords": "콘텐츠 SEO, 키워드 설계, H태그 구조, 검색 의도, E-E-A-T, 블로그 SEO, 콘텐츠 전략",
        "h1": "콘텐츠 SEO 서비스",
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
        "title": "디지털 PR · 백링크 진단 | OneSearchPro",
        "desc": "위험한 백링크 식별·브랜드 언급 추적·외부 평판·디지털 PR로 자연스러운 신뢰 신호를 확보하는 진단 서비스.",
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
        "title": "성공사례 | SEO 작업 기록 | OneSearchPro",
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
        "title": "SEO 인사이트 | 구글·네이버 SEO 가이드 | OneSearchPro",
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
                        "코어 업데이트 직후 SEO 주의사항 5가지",
                        "트래픽이 흔들릴 때 가장 위험한 건 패닉 작업입니다. 첫 2주에 손대지 말아야 할 5가지와 대신 무엇을 해야 하는지.",
                        "/insights/google-seo/post-core-update-mistakes/",
                        7
                    ),
                    insight_article_card(
                        "Helpful Content System 셀프 점검 7가지",
                        "HCS는 사이트 전체 평가입니다. 한국 사이트가 셀프 평가에서 자주 떨어지는 패턴과 통과 기준.",
                        "/insights/google-seo/helpful-content-self-check/",
                        8
                    ),
                    insight_article_card(
                        "신규 사이트 첫 1개월 SEO 우선순위 5가지",
                        "신규 도메인이 첫 달에 해야 할 SEO를 우선순위 순으로. 측정 기반·색인 확보·핵심 페이지·CWV·첫 콘텐츠.",
                        "/insights/google-seo/first-month-priorities/",
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
                        "워드프레스 LCP 개선 작업 순서",
                        "워드프레스 LCP 90%는 4가지 패턴에서 결정됩니다. 효과 큰 순서로 정리한 작업 매뉴얼.",
                        "/insights/technical-seo/wordpress-lcp-fix/",
                        8
                    ),
                    insight_article_card(
                        "모바일 우선 색인 점검 가이드",
                        "반응형 사이트도 안심할 수 없는 6가지 점검 항목과 콘텐츠 패리티의 의미.",
                        "/insights/technical-seo/mobile-first-indexing/",
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
                        "병원·치과 블로그 첫 100자 작성법",
                        "첫 100자에서 검색 의도 매칭과 메타 디스크립션이 결정됩니다. 의료광고심의 충돌도 피하는 작성법.",
                        "/insights/content-seo/medical-blog-first-100/",
                        7
                    ),
                    insight_article_card(
                        "쇼핑몰 제품 페이지 본문 6단락 구조",
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
                        "신규 매장 네이버 플레이스 3개월 운영",
                        "리뷰 없는 신규 매장이 빠지는 함정과, 정보·블로그·리뷰 우선순위로 짠 월별 운영 매뉴얼.",
                        "/insights/local-seo/new-store-naver-place/",
                        7
                    ),
                    insight_article_card(
                        "다지점 매장 GBP 본사·지점 분리 원칙",
                        "본사 정보를 모든 지점에 복붙하면 안 되는 이유. 위치·카테고리·사진·리뷰 응대 4가지 분리 원칙.",
                        "/insights/local-seo/multi-location-gbp/",
                        7
                    ),
                    insight_article_card(
                        "네이버 플레이스 부정 리뷰 대응 — 자주 하는 실수 5가지",
                        "부정 리뷰는 제거 대상이 아니라 응답 대상. 사장님들이 자주 빠지는 5가지 실수와 신뢰를 유지하는 4단계 응답 프로세스.",
                        "/insights/local-seo/negative-review-response-mistakes/",
                        8
                    ),
                    insight_card("\"지역명 + 서비스\" 키워드용 지역 랜딩페이지 설계법", "다지점 비즈니스에서 지역 키워드를 잡기 위한 페이지 구조와 콘텐츠 작성 가이드."),
                    insight_card("NAP 일관성과 로컬 인용(citation)이 왜 중요한가", "디렉토리·SNS·자체 사이트의 상호·주소·전화 정보 통일 가이드.")
                ]
            ) +

            insights_section("backlink-pr", "BACKLINK & DIGITAL PR", "백링크 · 디지털 PR",
                "안전한 외부 신호 확보, 백링크 리스크 진단, 디지털 PR 전략을 다룹니다.",
                [
                    insight_article_card(
                        "위험한 백링크 Disavow 결정 기준",
                        "도구 점수의 한계와 즉시·보류·유지 3단계 분류, 단계적 Disavow 제출 전략.",
                        "/insights/backlink-pr/disavow-decision/",
                        9
                    ),
                    insight_article_card(
                        "한국 언론사 보도자료 백링크 구분법",
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
                        "유튜브 쇼츠 설명란 트래픽 유도법",
                        "쇼츠 설명란의 첫 줄·본문·해시태그 구조와 외부 사이트 클릭률을 높이는 패턴.",
                        "/insights/sns/youtube-shorts-description/",
                        6
                    ),
                    insight_article_card(
                        "인스타그램 프로필 링크 SEO 비교",
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
                        "사이트 리뉴얼 301 매핑 실수 12가지",
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
        "title": "SEO 개선 사례 | 검색 유입·순위·구조·메타·내부링크 | OneSearchPro",
        "desc": "검색 유입 감소, 키워드 순위 정체, 사이트 구조 문제, 내부 링크 부족, 메타 카피 미흡, 서비스 페이지 최적화까지 — SEO 개선 6대 시나리오를 작업 전 문제·진단·개선·변화·주의점 5단계로 기록한 실무 사례 모음.",
        "keywords": "SEO 개선 사례, 검색 유입 감소, 키워드 순위 정체, 사이트 구조 SEO, 내부 링크 개선, 메타 태그 최적화, 서비스 페이지 SEO",
        "h1": "SEO 개선 사례",
        "eyebrow": "SEO IMPROVEMENT CASES",
        "lead": "사이트가 정체·하락하는 6가지 대표 패턴별 실무 작업 기록입니다. 각 사례는 \"작업 전 문제 → 진단 결과 → 개선한 항목 → 적용 후 변화 → 주의할 점\" 5단계로 정리했으며, 과장된 수치나 \"무조건 1위\" 표현은 사용하지 않습니다.",
        "body": (
            # 6대 시나리오 인덱스 (앵커 점프)
            '<section class="section case-index"><div class="container">'
            '<div class="section-head left"><span class="eyebrow">QUICK INDEX</span><h2>이 페이지에서 다루는 6가지 SEO 시나리오</h2><p>어느 상황에 해당하는지 먼저 골라 보고, 사례 카드로 이동하세요.</p></div>'
            '<div class="case-index-grid">'
            '<a href="#traffic-drop" class="case-index-item"><span class="case-index-num">01</span><div><b>검색 유입 감소</b><span>트래픽이 갑자기 줄어든 사이트의 원인 분리법</span></div></a>'
            '<a href="#ranking-stall" class="case-index-item"><span class="case-index-num">02</span><div><b>키워드 순위 정체</b><span>10~20위에서 1페이지 진입 못 하는 키워드 진단</span></div></a>'
            '<a href="#site-structure" class="case-index-item"><span class="case-index-num">03</span><div><b>사이트 구조 문제</b><span>정보 구조가 산만한 사이트의 카테고리 재설계</span></div></a>'
            '<a href="#internal-linking" class="case-index-item"><span class="case-index-num">04</span><div><b>내부 링크 개선</b><span>글은 많은데 서로 연결 안 된 사이트</span></div></a>'
            '<a href="#meta-optimization" class="case-index-item"><span class="case-index-num">05</span><div><b>메타 타이틀·디스크립션 개선</b><span>노출은 있지만 클릭이 안 되는 사이트</span></div></a>'
            '<a href="#service-page" class="case-index-item"><span class="case-index-num">06</span><div><b>서비스 페이지 최적화</b><span>거래형 키워드에서 서비스 페이지가 안 잡히는 사이트</span></div></a>'
            '</div></div></section>'

            # Case 1 — 검색 유입 감소
            '<section class="section" id="traffic-drop"><div class="container">'
            '<div class="case-section-head"><span class="case-num">01</span><span class="eyebrow">TRAFFIC DROP</span><h2>검색 유입 감소</h2><p class="lead">콘텐츠 작업은 그대로인데 검색 트래픽이 떨어졌을 때, 가장 위험한 건 \"감으로 손대기\" 입니다. 원인을 분리하는 게 먼저입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="MEDIA · B2B",
                icon="📉",
                h3="트래픽이 갑자기 줄어든 사이트 — 원인 분리부터",
                problem="3개월간 검색 트래픽이 단계적으로 감소. 콘텐츠 발행·기술 변경은 없었지만 핵심 페이지의 노출과 클릭이 함께 빠지는 패턴이었습니다.",
                diagnosis="구글 코어 업데이트 영향과 사이트 자체 이슈가 혼재된 상태로 확인. 일부 페이지는 알고리즘 평가 변화, 일부는 색인 누락이 원인이었습니다. 서치콘솔 \"커버리지\" 리포트와 코어 업데이트 발표 시점을 매칭해 분리했습니다.",
                improvements=["서치콘솔 시점별 데이터로 코어 영향 페이지 vs 사이트 이슈 페이지 분리", "색인 누락 페이지는 우선 진단·복구 (robots·canonical 점검)", "코어 영향 페이지는 즉시 대응 보류 (4주 관찰)", "원인이 분리된 후 우선순위 적용"],
                results=["색인 이슈 페이지 4주 내 노출 회복", "코어 영향 페이지는 다음 업데이트 사이클에서 부분 회복 관찰", "전체 작업 기간 약 8주"],
                caveats="코어 업데이트 영향에 패닉으로 콘텐츠를 대거 수정하면 측정 기준선이 사라집니다. 첫 2주는 데이터 수집·관찰 단계로 두는 게 가장 효과적입니다.",
                tools=["Google Search Console (커버리지·성능 리포트)", "GA4 (트래픽 시점·페이지별 분석)", "구글 코어 업데이트 발표 캘린더", "Ahrefs Site Explorer (외부 변화 점검)"],
                verification="서치콘솔에서 4주·8주·12주 시점의 노출수·평균 게재 순위 추이를 페이지군별로 분리해 비교. 색인 누락 페이지는 \"URL 검사\" 도구로 직접 색인 상태 확인.",
                comment="트래픽 그래프만 보면 패닉이 옵니다. 그래도 첫 2주는 데이터만 모으는 게 정답입니다. 패닉 작업이 진짜 원인을 찾을 기회를 빼앗아요.",
                insight="코어 업데이트와 사이트 자체 이슈는 원인이 다르므로 대응 시점도 달라야 합니다. 동시에 잡으려 하면 어느 것이 효과 있었는지 측정이 불가능해집니다.",
                checklist=["트래픽 하락 시점이 구글 코어 업데이트 발표와 일치하는지", "특정 페이지군에만 하락이 집중되는지(부분 영향)", "서치콘솔 커버리지 리포트에서 색인 누락 페이지가 늘었는지", "최근 외부 백링크 변화·페널티 메시지가 있었는지", "사이트 자체 변경(디자인·코드·플러그인) 시점과 일치하는지"],
                related_service=("기술 SEO 진단 서비스", "/services/technical-seo/"),
                related_insight=("코어 업데이트 직후 2주 손대지 말 5가지", "/insights/google-seo/post-core-update-mistakes/")
            ) +
            '</div></div></section>'

            # Case 2 — 키워드 순위 정체
            '<section class="section section-soft" id="ranking-stall"><div class="container">'
            '<div class="case-section-head"><span class="case-num">02</span><span class="eyebrow">RANKING STAGNATION</span><h2>키워드 순위 정체</h2><p class="lead">10~20위 권에 머무르며 1페이지 진입을 못 하는 키워드는 \"콘텐츠 부족\"이 아니라 \"신호 부족\"인 경우가 많습니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="SAAS · B2B",
                icon="⏳",
                h3="1페이지 진입을 못 하는 핵심 키워드 — 정체 원인 진단",
                problem="자체 블로그가 있지만 핵심 상업 키워드에서 6개월 이상 10~20위에 머무르는 상태. 콘텐츠 발행은 꾸준했지만 1페이지 진입이 안 되었습니다.",
                diagnosis="개별 페이지 품질은 충분했지만 토픽 권위가 분산되어 있었습니다. 같은 토픽을 다루는 글이 흩어져 있고 내부 링크로 연결되지 않아 검색엔진이 \"이 사이트는 ○○ 전문\"이라 판단할 신호가 부족했습니다.",
                improvements=["필러 페이지 1개 + 클러스터 8편으로 토픽 구조 재설계", "기존 인기 글에서 신규 필러로 컨텍스트 내부 링크", "타이틀·H1·메타를 검색 의도에 맞춰 재작성"],
                results=["타겟 키워드 중 다수가 1~2페이지로 이동", "오가닉 세션 약 2~3배 수준으로 증가", "전체 작업 기간 약 6개월"],
                caveats="정체 원인은 키워드마다 다릅니다. 어떤 키워드는 토픽 권위 부족, 어떤 키워드는 검색 의도 미스매치가 원인이라 일괄 대응으로는 해결되지 않습니다.",
                tools=["Ahrefs Keyword Explorer (키워드 난이도·SERP 분석)", "Google Search Console (쿼리별 평균 게재 순위)", "Screaming Frog (내부 링크 매핑)", "SEMrush Position Tracking"],
                verification="타겟 키워드의 평균 게재 순위를 4주 단위로 비교. 토픽 클러스터 도입 후 8주차에 노출 변화·12주차에 클릭 변화 측정.",
                comment="정체된 키워드는 글을 더 쓰는 게 답이 아닙니다. 흩어진 글들을 연결해서 신호를 모아주는 게 답이에요.",
                insight="토픽 권위는 글 1편의 품질로 만들어지지 않고, 같은 토픽을 다루는 글들의 \"묶음과 연결\"로 만들어집니다. 100편 흩어진 글보다 10편 연결된 글이 더 강합니다.",
                checklist=["같은 토픽 글들이 본문 내부 링크로 연결되어 있는지", "필러 콘텐츠(요약·허브 글)가 명시적으로 있는지", "SERP 상위 결과 유형과 우리 페이지 유형이 일치하는지", "타이틀·H1·메타가 검색 의도를 직접 표현하는지", "신규 글 발행 시 기존 인기 글에서 컨텍스트 링크가 추가되는지"],
                related_service=("SEO 컨설팅 서비스", "/services/seo/"),
                related_insight=("Helpful Content System 셀프 점검", "/insights/google-seo/helpful-content-self-check/")
            ) +
            '</div></div></section>'

            # Case 3 — 사이트 구조 문제
            '<section class="section" id="site-structure"><div class="container">'
            '<div class="case-section-head"><span class="case-num">03</span><span class="eyebrow">SITE STRUCTURE</span><h2>사이트 구조 문제</h2><p class="lead">페이지는 많은데 검색엔진이 \"이 사이트가 무엇인지\" 파악하기 어려운 경우, 카테고리·계층·내부 링크의 재설계가 필요합니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="EDU",
                icon="🏗️",
                h3="정보 구조가 산만한 사이트 — 카테고리·계층 재설계",
                problem="강의 페이지가 200개 넘게 쌓였지만 카테고리 페이지가 부재. URL 계층도 일관성이 없어 같은 주제가 여러 경로에 흩어져 있었습니다. 카테고리 단위 키워드(\"○○ 강의 추천\") 검색에서 노출 자체가 없었습니다.",
                diagnosis="URL 구조에 일관성이 없고(예: /course/abc, /lesson/xyz, /classes/123 혼재), 카테고리 허브 페이지가 부재. 사이드바·태그 외에 본문 내부 링크가 없어 \"고립 페이지(orphan)\"가 다수였습니다.",
                improvements=["URL을 /courses/[category]/[slug]/ 형식으로 통일 + 1:1 301 리다이렉트", "카테고리 허브 페이지 신설 (소개 본문 + 강의 리스트 + 비교 가이드)", "BreadcrumbList·ItemList 스키마 적용", "본문 내부 컨텍스트 링크로 고립 페이지 연결"],
                results=["카테고리 단위 키워드에서 노출 시작", "카테고리 페이지 자체 직접 방문 증가", "작업 기간 약 4개월"],
                caveats="URL 변경 시 301 매핑이 부실하면 트래픽 손실이 큽니다. 변경 전 기존 URL·키워드·트래픽 매핑 시트를 반드시 만들어두세요.",
                tools=["Screaming Frog (사이트 구조·URL 패턴 스캔)", "Google Search Console (URL 검사·색인 상태)", "Ahrefs Site Audit (구조 이슈 식별)", "자체 URL 매핑 스프레드시트"],
                verification="URL 변경 후 4주간 서치콘솔에서 404 페이지 변화·신규 URL 색인 속도 추적. 카테고리 키워드의 노출 회복은 8~12주 단위로 측정.",
                comment="사이트 구조는 디자인이 아니라 검색엔진과 사용자가 사이트를 이해하는 방식입니다. 깊이가 4단 넘으면 크롤러도 사용자도 못 찾아요.",
                insight="카테고리 허브 페이지가 없으면 카테고리 단위 키워드는 절대 잡히지 않습니다. 본문이 있는 카테고리 페이지 + 1:1 301 매핑이 핵심입니다.",
                checklist=["사용자가 핵심 페이지에 3클릭 안에 도달하는지", "URL 패턴이 일관성 있는지(혼재 없는지)", "카테고리 허브 페이지가 본문과 함께 존재하는지", "고립 페이지(어디서도 링크 안 되는 페이지) 가 있는지", "URL 변경 시 1:1 301 매핑 시트가 있는지"],
                related_service=("SEO 웹사이트 제작 서비스", "/services/web-design/"),
                related_insight=("301 리다이렉트 자주 빠뜨리는 12가지", "/insights/visibility/301-migration-mistakes/")
            ) +
            '</div></div></section>'

            # Case 4 — 내부 링크 개선
            '<section class="section section-soft" id="internal-linking"><div class="container">'
            '<div class="case-section-head"><span class="case-num">04</span><span class="eyebrow">INTERNAL LINKING</span><h2>내부 링크 개선</h2><p class="lead">글이 많아도 서로 연결되지 않으면 검색엔진이 사이트 전체 가치를 인식하지 못합니다. 자동 \"관련 글\" 만으로는 부족합니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="MEDIA",
                icon="🔗",
                h3="글은 많은데 서로 연결 안 된 사이트 — 내부 링크 재구성",
                problem="라이프스타일 미디어 사이트로 글이 100편 넘게 누적. 그런데 핵심 글에서도 다른 글로 가는 본문 내 컨텍스트 링크가 거의 없었고, 사이드바·푸터의 자동 \"인기 글\"만 있는 상태였습니다.",
                diagnosis="사이드바·자동 추천 위젯 링크는 검색엔진이 컨텍스트 신호로 약하게 평가합니다. 본문 한가운데에서 자연스럽게 \"○○에 대해 더 알려면 [○○ 글 보기]\" 같은 텍스트 링크가 사실상 없었습니다.",
                improvements=["트래픽 상위 20개 글에서 관련 글로 가는 본문 텍스트 링크 추가 (글당 평균 3~5개)", "앵커텍스트를 정확한 타겟 키워드로 통일", "허브-스포크 구조로 필러 글과 클러스터 글 연결", "고립 페이지(어디서도 링크되지 않는 글) 식별·연결"],
                results=["연결된 페이지의 노출·체류 시간이 함께 회복", "사이트 전체 권위 신호 강화로 신규 글 색인 속도도 개선", "작업 기간 약 3개월"],
                caveats="자동 생성된 \"관련 글\" 위젯에 의존하지 마세요. 컨텍스트가 어색한 위치에 강제 링크를 박는 것도 역효과입니다.",
                tools=["Ahrefs Internal Backlinks", "Screaming Frog (Inlinks 리포트)", "GA4 (페이지 흐름·이동 경로)", "자체 내부 링크 매트릭스 시트"],
                verification="8주간 인기 글 → 신규 글의 트래픽 흐름 측정. 사이드바와 본문 컨텍스트 링크의 클릭률 비교. 신규 글의 평균 색인 소요 시간 단축 확인.",
                comment="사이드바·자동 위젯 링크는 검색엔진 신호로 거의 안 잡힙니다. 본문 한가운데에 자연스럽게 들어간 한 줄이 푸터 30개 링크보다 강합니다.",
                insight="내부 링크는 권위가 흐르는 수도관입니다. 본문 컨텍스트 안에서 자연스러운 위치에 박힌 한 줄이 사이드바·푸터의 자동 링크보다 훨씬 강한 신호입니다.",
                checklist=["트래픽 상위 20개 글에 본문 내부 링크가 평균 3개+ 있는지", "고립 페이지(어디서도 본문 링크 없는 페이지)가 있는지", "앵커텍스트가 \"여기 클릭\" 대신 정확한 키워드인지", "필러 글 → 클러스터 글 흐름이 설계되어 있는지", "신규 글 발행 시 기존 글에서 컨텍스트 링크 추가 루틴이 있는지"],
                related_service=("SEO 컨설팅 서비스", "/services/seo/"),
                related_insight=("쇼핑몰 제품 페이지 6단락 구조", "/insights/content-seo/product-page-content-structure/")
            ) +
            '</div></div></section>'

            # Case 5 — 메타 타이틀·디스크립션 개선
            '<section class="section" id="meta-optimization"><div class="container">'
            '<div class="case-section-head"><span class="case-num">05</span><span class="eyebrow">META OPTIMIZATION</span><h2>메타 타이틀·디스크립션 개선</h2><p class="lead">검색 결과에 노출은 되는데 클릭이 안 되는 사이트는 메타 카피의 문제일 가능성이 큽니다. 같은 노출로 더 많은 유입을 만드는 작업.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="ECOMMERCE",
                icon="🏷️",
                h3="노출은 있지만 클릭이 안 되는 사이트 — 메타 카피 재작성",
                problem="서치콘솔 평균 게재 순위는 8~12위로 나쁘지 않은데 CTR이 평균보다 현저히 낮았습니다. 검색 결과에 우리 페이지가 보여도 사용자가 다른 결과를 클릭하는 패턴이었습니다.",
                diagnosis="타이틀이 \"키워드 + 회사명\" 형식으로만 작성되어 있고 클릭 후크가 없었습니다. 디스크립션은 200자가 넘어 검색 결과에서 잘리거나, 페이지 본문 첫 부분이 자동으로 추출되어 광고 카피 없는 상태로 노출되고 있었습니다.",
                improvements=["타이틀을 \"키워드 + 사용자 혜택·구체 숫자\" 형식으로 재작성 (50~60자)", "디스크립션을 120~155자로 단축하면서 CTA 1줄 명시", "특정 페이지에는 FAQ·리뷰 등 리치 결과 유도 스키마 추가", "A/B 테스트 가능한 페이지 그룹은 분기별 메타 카피 교체로 효과 측정"],
                results=["주요 페이지의 CTR이 상승 추세로 전환", "같은 노출수에서 클릭이 의미 있게 증가", "작업 기간 약 6주"],
                caveats="클릭 후크가 본문과 어긋나면 이탈률이 오히려 늘어납니다. 메타 개선 후 \"클릭률은 올랐는데 체류 시간이 떨어졌다\" 면 본문이 메타 약속을 지키지 못하는 신호입니다.",
                tools=["Google Search Console (성능 리포트 CTR)", "PageSpeed Insights (Rich Results 미리보기)", "Schema.org Validator", "자체 메타 작성 시트 + A/B 테스트"],
                verification="메타 변경 후 4주간 같은 페이지의 노출수·평균 게재 순위 대비 CTR 변화 추적. 변경 안 한 페이지를 대조군으로 비교.",
                comment="메타는 검색자가 우리 페이지를 클릭할지 결정하는 1초짜리 면접입니다. 키워드만 박으면 면접에서 떨어집니다.",
                insight="키워드만 박힌 타이틀은 색인 가치는 있지만 클릭 가치가 없습니다. 노출은 되는데 안 클릭되는 페이지가 많다면 메타부터 점검하세요.",
                checklist=["타이틀 길이가 50~60자 안에 들어오는지", "디스크립션이 120~155자에 CTA 포함되었는지", "검색 결과에서 디스크립션이 자동 추출되지 않는지", "OG title·description이 별도로 작성되었는지", "리치 결과 유도 스키마(FAQ·Review·Product)가 적용되었는지"],
                related_service=("SEO 컨설팅 서비스", "/services/seo/"),
                related_insight=("Helpful Content System 셀프 점검", "/insights/google-seo/helpful-content-self-check/")
            ) +
            '</div></div></section>'

            # Case 6 — 서비스 페이지 최적화
            '<section class="section section-soft" id="service-page"><div class="container">'
            '<div class="case-section-head"><span class="case-num">06</span><span class="eyebrow">SERVICE PAGE OPTIMIZATION</span><h2>서비스 페이지 최적화</h2><p class="lead">블로그 글은 트래픽을 만들어도 정작 매출과 연결되는 \"서비스 페이지\"가 검색에 잡히지 않으면 SEO의 비즈니스 가치는 절반입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="B2B · SAAS",
                icon="💼",
                h3="거래형 키워드에서 서비스 페이지가 안 잡히는 사이트 — 서비스 페이지 강화",
                problem="정보형 블로그 글은 검색에 잘 나오지만 \"서비스명 + 가격\", \"서비스명 + 비교\" 같은 거래형 키워드에서는 서비스 페이지가 아예 노출되지 않았습니다. 트래픽은 많은데 문의 전환은 약한 구조였습니다.",
                diagnosis="서비스 페이지에 본문이 거의 없고 이미지 위주로 구성되어 있었습니다. 거래형 검색 의도 키워드(\"가격\", \"비교\", \"신청\")가 본문에 등장하지 않아 매칭 실패. 또한 블로그 글에서 서비스 페이지로 가는 내부 링크가 거의 없어 권위 신호도 약했습니다.",
                improvements=["서비스 페이지 본문 강화 (대상 고객·문제·해결·차별점·FAQ·가격 안내)", "Service / Product / Offer 스키마 적용", "관련 블로그 글에서 서비스 페이지로 본문 내부 링크 5~10개", "거래형 키워드 매핑 (블로그=정보형 / 서비스=거래형으로 의도 분리)"],
                results=["거래형 키워드에서 서비스 페이지가 직접 노출", "블로그 트래픽이 서비스 페이지로 흐르는 비율 증가", "작업 기간 약 2~3개월"],
                caveats="블로그 글에 서비스 페이지 링크를 과도하게 박으면 글 자체의 신뢰도가 떨어집니다. 본문 컨텍스트가 자연스러운 위치에만 1~2개 배치하는 게 안전합니다.",
                tools=["Google Search Console (거래형 쿼리 분석)", "GA4 (페이지별 전환 추적)", "Microsoft Clarity (사용자 행동 히트맵)", "Schema.org Validator (Service·Offer)"],
                verification="서치콘솔에서 거래형 쿼리(가격·비교·신청)의 노출·클릭 변화를 8주 단위로 추적 + 폼 제출률(전환) 변화 측정.",
                comment="블로그는 트래픽을 만들고, 서비스 페이지는 매출을 만듭니다. 둘 다 SEO가 필요하지만 잡는 키워드가 다릅니다.",
                insight="정보형 키워드는 블로그 페이지로, 거래형 키워드는 서비스 페이지로 분리해야 두 의도 모두 잡을 수 있습니다. 한 페이지로 둘 다 잡으려 하면 둘 다 약해집니다.",
                checklist=["서비스 페이지에 \"대상·문제·해결·차별점·프로세스·FAQ\" 6단락이 있는지", "Service / Offer 스키마가 적용되었는지", "블로그에서 서비스 페이지로 본문 컨텍스트 링크 1~2개 있는지", "거래형 키워드(가격·비교·신청)가 서비스 페이지에 매핑되었는지", "페이지 하단에 명확한 CTA + 신뢰 신호(실적·후기)가 있는지"],
                related_service=("SEO 웹사이트 제작 서비스", "/services/web-design/"),
                related_insight=("쇼핑몰 제품 페이지 6단락 구조", "/insights/content-seo/product-page-content-structure/")
            ) +
            '</div></div></section>'

            # CTA
            '<section class="section section-cta"><div class="container cta-grid">'
            '<div><h2>위 시나리오 중 우리 사이트는 어디에 해당할까요?</h2><p>현재 사이트 상태를 진단해 어느 패턴인지, 어떤 우선순위로 작업해야 하는지 24시간 내 분석 리포트를 보내드립니다.</p></div>'
            '<div class="cta-actions"><a href="https://t.me/googleseolab" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-lg">무료 SEO 진단 받기 →</a><a href="/services/seo/" class="btn btn-outline btn-lg btn-light">SEO 컨설팅 서비스 보기</a></div>'
            '</div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"SEO 개선 사례","url":"https://onesearchpro.org/case-studies/seo/","description":"검색 유입·키워드 순위·사이트 구조·내부 링크·메타·서비스 페이지 6대 시나리오 SEO 개선 사례","isPartOf":{"@type":"WebSite","name":"OneSearchPro"}}</script>',
        "active": "cases",
    },

    "/case-studies/local-seo/": {
        "title": "지역 SEO 사례 | 지역 키워드·랜딩·지도·메타 개선 | OneSearchPro",
        "desc": "지역명 + 서비스 키워드, 지역 랜딩페이지 구조, 중복 페이지 정리, 내부 링크 설계, 지도·로컬 검색 대응, 지역별 메타 개선까지 — 지역 SEO 6대 시나리오 실무 작업 기록.",
        "keywords": "지역 SEO 사례, 지역 키워드, 지역 랜딩페이지, 중복 지역 페이지, GBP, 네이버 플레이스, 지점 SEO",
        "h1": "지역 SEO 사례",
        "eyebrow": "LOCAL SEO CASES",
        "lead": "지역 기반 검색 유입을 목표로 지역 랜딩페이지, 내부링크, 지역 키워드, 페이지 구조를 개선한 지역 SEO 사례입니다. 각 사례는 \"작업 전 문제 → 진단 결과 → 개선한 항목 → 적용 후 변화 → 주의할 점\" 5단계로 정리했습니다.",
        "body": (
            # 6대 시나리오 인덱스 (앵커 점프)
            '<section class="section case-index"><div class="container">'
            '<div class="section-head left"><span class="eyebrow">QUICK INDEX</span><h2>이 페이지에서 다루는 6가지 지역 SEO 시나리오</h2><p>어느 상황에 해당하는지 먼저 골라 보고, 사례 카드로 이동하세요.</p></div>'
            '<div class="case-index-grid">'
            '<a href="#local-keywords" class="case-index-item"><span class="case-index-num">01</span><div><b>지역명 + 서비스 키워드</b><span>"○○동 ○○" 검색에 안 잡히는 사이트의 키워드 트리</span></div></a>'
            '<a href="#landing-structure" class="case-index-item"><span class="case-index-num">02</span><div><b>지역 랜딩페이지 구조</b><span>지점 페이지가 사진뿐인 사이트의 6단락 본문 적용</span></div></a>'
            '<a href="#duplicate-cleanup" class="case-index-item"><span class="case-index-num">03</span><div><b>중복 지역 페이지 정리</b><span>지점들이 같은 본문 템플릿을 쓰는 사이트의 차별화</span></div></a>'
            '<a href="#local-internal-link" class="case-index-item"><span class="case-index-num">04</span><div><b>내부링크 설계</b><span>지점 페이지가 본사·블로그에서 분리된 사이트의 권위 흐름</span></div></a>'
            '<a href="#map-local-pack" class="case-index-item"><span class="case-index-num">05</span><div><b>지도/로컬 검색 대응</b><span>구글맵·네이버 플레이스에서 빠진 사이트의 NAP·GBP 정비</span></div></a>'
            '<a href="#regional-meta" class="case-index-item"><span class="case-index-num">06</span><div><b>지역별 제목·디스크립션 개선</b><span>지점 메타가 모두 똑같은 사이트의 CTR 회복</span></div></a>'
            '</div></div></section>'

            # Case 1 — 지역명 + 서비스 키워드
            '<section class="section" id="local-keywords"><div class="container">'
            '<div class="case-section-head"><span class="case-num">01</span><span class="eyebrow">LOCAL KEYWORD MAPPING</span><h2>지역명 + 서비스 키워드</h2><p class="lead">지점은 있는데 "○○동 ○○" 같은 지역 검색에서 노출되지 않는다면, 사이트 본문에 지역 키워드가 거의 등장하지 않는 경우가 대부분입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="MASSAGE",
                icon="📍",
                h3="지점은 있는데 \"○○동 ○○\"에 안 잡히는 사이트 — 지역 키워드 트리 설계",
                problem="브랜드 검색(\"○○ 마사지\")은 잡혔지만 \"○○동 마사지\", \"○○구 ○○\" 같은 지역 키워드 검색에서는 거의 노출되지 않았습니다. 모바일 사용자 대부분이 지역명을 함께 검색하는 업종이라 손실이 컸습니다.",
                diagnosis="자체 사이트 어디에도 지역명 + 서비스 조합이 본문 텍스트로 등장하지 않았습니다. 메타·H1에도 \"전국\", \"공식 사이트\" 같은 일반 표현만 있고 \"○○동·○○구\" 같은 검색자 표현이 없었습니다.",
                improvements=["지역 키워드 트리 구축 (시·도 → 구·군 → 동·읍·면 3단 분류)", "지점별 랜딩페이지의 H1·title·메타·본문에 지역명 자연스럽게 배치", "검색자가 실제로 쓰는 표현(\"○○동 ○○ 추천\", \"○○역 근처 ○○\") 본문 도입", "지역 키워드 우선순위(검색량 + 경쟁도) 기준 분기별 작업 순서 수립"],
                results=["일부 지역 키워드에서 자체 사이트 노출 시작", "지점 검색 트래픽 회복 추세", "작업 기간 약 4개월"],
                caveats="지역 키워드 검색은 경쟁 매장의 활동성·계절성에 따라 변동이 큽니다. 한 번 상위 노출됐다고 작업을 멈추면 다시 밀려나는 경우가 흔합니다.",
                tools=["네이버 키워드 도구", "구글 키워드 플래너", "Ahrefs Keyword Explorer", "GSC 쿼리 리포트"],
                verification="작업 후 8주 동안 GSC에서 신규 지역 키워드 노출·클릭 수를 주간 단위로 추적했습니다. 일부 키워드는 12주 시점부터 본격적으로 순위가 잡혔습니다.",
                comment="지역 키워드는 '한 번에 다 잡겠다'고 욕심내면 본문이 키워드 나열처럼 보입니다. 우선순위 3~5개부터 자연스럽게 본문에 녹이는 게 안전합니다.",
                insight="지역 검색은 '어디에서 ○○하는지'에 대한 답을 본문에 자연스럽게 담아야 합니다. 메뉴·푸터의 지역명 노출만으로는 검색 시그널로 약합니다.",
                checklist=["사이트 본문에 '시·도 + 구·군 + 동' 단위 지역명이 등장하는지", "검색자가 실제로 쓰는 표현(\"근처\", \"역 앞\", \"○○동\")이 메타·H1에 있는지", "지점별 지역 키워드 우선순위 시트가 있는지"],
                related_service=("지역 SEO 서비스", "/services/local-seo/"),
                related_insight=("신규 매장 네이버 플레이스 첫 30일", "/insights/local-seo/new-store-naver-place/")
            ) +
            '</div></div></section>'

            # Case 2 — 지역 랜딩페이지 구조
            '<section class="section section-soft" id="landing-structure"><div class="container">'
            '<div class="case-section-head"><span class="case-num">02</span><span class="eyebrow">LANDING PAGE STRUCTURE</span><h2>지역 랜딩페이지 구조</h2><p class="lead">지점 페이지가 사진과 영업시간만 있다면 검색엔진은 이 페이지가 \"지역 ○○ 서비스\"라고 판단할 단서가 없습니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="DENTAL",
                icon="🏠",
                h3="지점 페이지 본문이 비어있는 사이트 — 6단락 구조 적용",
                problem="다지점 치과 사이트로 지점 페이지가 있긴 했지만 사진 5장과 영업시간·전화번호만 있는 구조. 본문이 사실상 비어있어 검색엔진이 \"이 페이지는 ○○동 치과 페이지\"라고 인식할 텍스트가 없었습니다.",
                diagnosis="지역 랜딩페이지의 본문 부재가 핵심. 메타 디스크립션이 자동 추출되어 \"진료시간 09~18 · 점심 12~13\" 같은 의미 없는 내용이 검색 결과에 노출되고 있었습니다.",
                improvements=["지역 랜딩페이지에 6단락 본문 구조 도입: ① 지점 소개 + 지역 특성, ② 진료 항목·서비스, ③ 가는 길·교통편, ④ 주차·편의시설, ⑤ FAQ, ⑥ 예약 안내", "지역명·랜드마크·인근 정보를 본문에 자연스럽게 포함", "지점별 LocalBusiness 스키마 적용 (영업시간·주소·전화 정확히)", "메타 description을 사람이 직접 작성해 자동 추출 대체"],
                results=["지점 페이지의 지역 검색 노출 회복", "검색 결과 스니펫이 의미 있는 문장으로 표시 → CTR 회복", "작업 기간 약 3개월"],
                caveats="지점별 콘텐츠를 복붙으로 만들면 다음 사례(중복 페이지)와 같은 문제가 생깁니다. 지점마다 차별화된 내용을 작성하는 게 핵심입니다.",
                tools=["Screaming Frog", "GSC URL 검사", "Schema Markup Validator", "PageSpeed Insights"],
                verification="지점 페이지에 본문 6단락을 적용한 후, 4주·8주·12주 시점에 GSC에서 해당 페이지의 노출·평균 게재순위를 비교했습니다. 스키마 적용은 Schema Validator에서 무오류를 확인한 뒤 색인 재요청을 진행했습니다.",
                comment="\"지점 페이지는 사진만으로 충분하다\"는 가정을 가장 자주 봅니다. 실제로는 검색엔진이 '여기는 ○○동 ○○ 페이지'라고 해석할 텍스트가 한 단락도 없으면 노출 기회를 잡지 못합니다.",
                insight="지점 페이지에서 가장 효과가 큰 단락은 '가는 길·교통편'이었습니다. 검색자가 이미 위치를 파악하려는 의도로 들어오기 때문에 클릭률·체류시간이 함께 올라갑니다.",
                checklist=["지점 페이지 본문이 텍스트 300자 이상인지", "메타 description이 자동 추출이 아닌 사람 작성인지", "LocalBusiness 스키마가 적용되고 영업시간·주소가 정확한지"],
                related_service=("지역 SEO 서비스", "/services/local-seo/"),
                related_insight=("쇼핑몰 제품 페이지 6단락 구조", "/insights/content-seo/product-page-content-structure/")
            ) +
            '</div></div></section>'

            # Case 3 — 중복 지역 페이지 정리
            '<section class="section" id="duplicate-cleanup"><div class="container">'
            '<div class="case-section-head"><span class="case-num">03</span><span class="eyebrow">DUPLICATE CLEANUP</span><h2>중복 지역 페이지 정리</h2><p class="lead">지점 50개가 본문 90%가 똑같은 페이지를 가지고 있다면, 검색엔진이 \"50개 모두 같은 페이지\"로 판단해 어느 것도 1위가 되지 않습니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="F&B FRANCHISE",
                icon="🧹",
                h3="지점 50개가 같은 본문 템플릿을 쓰는 사이트 — 차별화·통합 정리",
                problem="외식 프랜차이즈 사이트로 지점 페이지가 50개 넘게 있지만 본문 90% 이상이 본사 템플릿 그대로. 주소·전화·지점명만 다른 사실상 동일한 페이지였습니다. 일부 지점은 색인조차 되지 않았습니다.",
                diagnosis="구글이 중복 콘텐츠로 판단해 일부 지점 페이지를 색인에서 제외하거나, 색인은 했지만 검색에서 노출하지 않는 상태. 서치콘솔에서 \"중복, 사용자가 선택한 표준 URL 없음\" 메시지가 다수 발생했습니다.",
                improvements=["지점별 차별화 콘텐츠 작성 (지역 특성, 인근 상권, 매장 인테리어 특징, 지점 매니저 인사말, 지역 한정 메뉴 등)", "잘못 설정된 canonical 정비 (일부 지점이 본사 페이지를 canonical로 가리키고 있던 케이스 수정)", "본문이 너무 비슷한 일부 작은 지점은 통합 페이지로 묶고 301 리다이렉트", "색인 거부 페이지는 본문 보강 후 서치콘솔 색인 재요청"],
                results=["색인된 지점 페이지 수 회복", "지역 키워드에서 노출 시작", "작업 기간 약 4개월"],
                caveats="무리한 지점 통합은 지역 시그널 자체를 잃습니다. 지역 검색 가치가 있는 지점은 본문 차별화로, 가치가 적은 지점만 통합하는 게 안전합니다.",
                tools=["Screaming Frog", "GSC 색인 적용 범위 리포트", "Siteliner 중복 콘텐츠 진단", "canonical 매핑 시트"],
                verification="중복 정리 후 6주 동안 GSC '색인 적용 범위'에서 '중복, 사용자가 선택한 표준 URL 없음' 페이지 수가 단계적으로 줄어드는지 모니터링했습니다. 통합·301 처리 페이지는 리다이렉트 체인 길이도 함께 점검했습니다.",
                comment="프랜차이즈 사이트에서 가장 흔한 실수는 \"본사 페이지로 canonical 한 줄 박아두면 끝난다\"는 가정입니다. 그렇게 하면 그 지점은 검색에서 영원히 안 보입니다.",
                insight="지점별 차별화 콘텐츠 중 가장 빠르게 색인 회복을 만든 단락은 '지점 매니저 인사말' + '지역 한정 메뉴/서비스'였습니다. 다른 지점과 본문이 명확히 달라지는 신호가 강력합니다.",
                checklist=["지점 페이지끼리 본문 유사도가 80% 이상인 곳이 있는지", "canonical이 본사 페이지를 가리키는 지점이 있는지", "통합·301 처리한 페이지가 의도대로 동작하는지"],
                related_service=("지역 SEO 서비스", "/services/local-seo/"),
                related_insight=("Helpful Content System 셀프 점검", "/insights/google-seo/helpful-content-self-check/")
            ) +
            '</div></div></section>'

            # Case 4 — 내부링크 설계
            '<section class="section section-soft" id="local-internal-link"><div class="container">'
            '<div class="case-section-head"><span class="case-num">04</span><span class="eyebrow">INTERNAL LINKING</span><h2>내부링크 설계</h2><p class="lead">지점 페이지가 만들어졌어도 본사·블로그에서 본문 컨텍스트 링크가 없으면 검색엔진이 \"중요하지 않은 페이지\"로 판단합니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="MULTI-STORE",
                icon="🔗",
                h3="지점 페이지가 본사·블로그에서 분리된 사이트 — 권위 흐름 재설계",
                problem="다지점 매장 사이트로 지점 페이지가 만들어져 있긴 했지만, 본사 페이지·블로그 글에서 지점으로 가는 본문 내 컨텍스트 링크가 거의 없었습니다. 메뉴와 푸터의 \"매장 찾기\" 버튼 외에는 사실상 고립된 페이지였습니다.",
                diagnosis="자동 \"전체 매장 보기\" 페이지가 있긴 했지만 그 페이지에서 개별 지점으로 가는 링크 외에는 사이트 내 어디서도 \"○○동 매장 보기\" 같은 컨텍스트 링크가 없었습니다. 권위 신호가 흐르지 않아 색인 우선순위도 낮았습니다.",
                improvements=["지역별 허브 페이지 신설 (시·도 단위 또는 권역 단위) → 그 안에서 인근 지점 그룹화", "본사·서비스 페이지 본문에서 주요 지점으로 자연스러운 컨텍스트 링크 (\"강남 지점에서 자세히 보기\" 같은 표현)", "블로그 글에서 관련 지점으로 링크 (\"○○동 가이드\" 글 → 해당 지점 페이지)", "앵커텍스트는 정확한 지역명 + 서비스로 통일"],
                results=["주요 지점 페이지의 색인 속도 개선", "지점 페이지로 권위 신호가 흐르기 시작", "작업 기간 약 3개월"],
                caveats="모든 페이지에서 모든 지점으로 링크하면 노이즈로 평가됩니다. 컨텍스트가 자연스러운 위치에만, 1~3개씩 배치하는 게 효과적입니다.",
                tools=["Ahrefs Site Audit", "Screaming Frog 내부링크 리포트", "GSC 링크 리포트", "내부링크 매트릭스 시트"],
                verification="허브 페이지·서비스 페이지에서 지점으로 가는 컨텍스트 링크를 추가한 후, 4주마다 Screaming Frog로 지점 페이지의 InLink 수가 증가하는지 확인했습니다. GSC 링크 리포트의 '많이 연결된 페이지'에 주요 지점이 진입하는지도 함께 봤습니다.",
                comment="\"매장 찾기 페이지가 있으니 내부링크는 충분하다\"는 인식을 자주 봅니다. 자동 디렉토리식 매장 찾기 페이지는 검색엔진에 권위 흐름을 거의 보내지 못합니다.",
                insight="블로그 글에서 지점으로 보내는 컨텍스트 링크가 의외로 강력했습니다. \"○○동 ○○ 가이드\" 같은 정보형 글이 자연스럽게 지점 페이지를 인용하는 구조가 가장 안정적입니다.",
                checklist=["지점 페이지의 InLink 수가 페이지당 5개 이상인지", "본사·서비스 본문에 주요 지점 링크가 컨텍스트로 들어가는지", "앵커텍스트가 '여기 클릭'이 아닌 '지역명 + 서비스'인지"],
                related_service=("지역 SEO 서비스", "/services/local-seo/"),
                related_insight=("다지점 사업장 GBP 운영 가이드", "/insights/local-seo/multi-location-gbp/")
            ) +
            '</div></div></section>'

            # Case 5 — 지도/로컬 검색 대응
            '<section class="section" id="map-local-pack"><div class="container">'
            '<div class="case-section-head"><span class="case-num">05</span><span class="eyebrow">MAP & LOCAL PACK</span><h2>지도/로컬 검색 대응</h2><p class="lead">모바일에서 지역 검색을 하면 \"지도 결과\"와 \"로컬 팩\"이 최상단입니다. 자체 사이트만 신경 쓰면 노출의 절반을 놓칩니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="MEDICAL",
                icon="🗺️",
                h3="구글맵·네이버 플레이스에서 빠진 사이트 — NAP·GBP·플레이스 풀 정비",
                problem="자체 사이트는 일부 지역 키워드에서 잡혔지만 구글맵 로컬 팩(상단 지도 결과 3곳)과 네이버 플레이스 상위에서 빠져 있었습니다. 모바일 트래픽 대부분은 지도 결과를 먼저 클릭하므로 자체 사이트 트래픽만으로는 한계가 명확했습니다.",
                diagnosis="구글 비즈니스 프로필(GBP)이 기본 정보만 설정된 상태. 카테고리·서비스·사진·게시물·리뷰 응대가 거의 운영되지 않았습니다. 네이버 플레이스도 마찬가지. NAP(상호·주소·전화)가 사이트·GBP·네이버 플레이스·외부 디렉토리에서 미세하게 달라 일관성 문제가 있었습니다.",
                improvements=["GBP 풀 셋업 — 카테고리·부카테고리·서비스 항목·30장+ 사진·주간 게시물·리뷰 응답 SLA", "네이버 플레이스 메뉴·서비스·영업시간·휴무일·블로그 연동 정비", "NAP 통일 — 사이트·GBP·플레이스·디렉토리 전수 점검 후 일관 갱신", "지역 디렉토리 등록 (구글맵·다음 지도·카카오맵·업종별 디렉토리)", "자체 사이트에 LocalBusiness 스키마 적용"],
                results=["일부 지역 키워드에서 구글 로컬 팩 노출 시작", "네이버 플레이스 상위 노출과 예약·전화 문의 증가", "작업 기간 약 5개월"],
                caveats="리뷰 어뷰징(지인 리뷰 대량 작성·금품 거래)은 즉시 패널티 사유입니다. 영수증 인증 기반의 자연 리뷰만 유도해야 합니다.",
                tools=["Google Business Profile 관리자", "네이버 플레이스 관리자", "NAP 일관성 점검 시트", "Schema Markup Validator"],
                verification="GBP·플레이스 정비 후 매주 GBP 인사이트(검색 노출수·통화·길찾기)와 네이버 플레이스 통계를 비교해 추이를 확인했습니다. 자체 사이트에는 LocalBusiness 스키마를 적용해 Schema Validator로 무오류를 점검했습니다.",
                comment="\"GBP는 한 번 만들어두면 끝\"이라는 인식이 가장 위험합니다. 게시물·사진·리뷰 응답이 멈춘 GBP는 알고리즘이 활동성 낮은 비즈니스로 판정합니다.",
                insight="자체 사이트 SEO보다 GBP·플레이스 정비가 더 빨리 매출로 이어진 케이스가 많았습니다. 지역·로컬 비즈니스라면 사이트 SEO와 동시 진행이 필수입니다.",
                checklist=["NAP가 사이트·GBP·플레이스·디렉토리에서 완전히 일치하는지", "GBP·플레이스에 주간 게시물·사진이 정기 갱신되는지", "리뷰 응답 SLA가 24~48시간 내인지"],
                related_service=("지역 SEO 서비스", "/services/local-seo/"),
                related_insight=("다지점 사업장 GBP 운영 가이드", "/insights/local-seo/multi-location-gbp/")
            ) +
            '</div></div></section>'

            # Case 6 — 지역별 제목·디스크립션 개선
            '<section class="section section-soft" id="regional-meta"><div class="container">'
            '<div class="case-section-head"><span class="case-num">06</span><span class="eyebrow">REGIONAL META</span><h2>지역별 제목·디스크립션 개선</h2><p class="lead">지점 메타가 모두 \"브랜드명 - 공식 사이트\" 패턴이면 지역 검색에서 클릭률이 회복되지 않습니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="MULTI-STORE",
                icon="🏷️",
                h3="지점 메타가 모두 똑같은 사이트 — 지역별 메타 재설계",
                problem="지점 페이지 30개가 모두 \"○○ 브랜드 - 공식 사이트\" 형식의 동일한 title을 사용. description도 \"최고의 서비스를 제공합니다\" 같은 일반 카피였습니다. 검색 결과에 노출되어도 클릭 후크가 없어 CTR이 매우 낮았습니다.",
                diagnosis="title이 지역 정보 없이 브랜드명만 포함. description은 페이지마다 동일해서 검색 결과에서 다른 지점과 구분이 안 됨. 사용자가 \"○○동 ○○\"로 검색해도 우리 결과에 지역명이 안 보여 클릭률 차이가 컸습니다.",
                improvements=["지점별 title 패턴 도입: \"○○동 ○○ — 영업시간·주차·예약 | 브랜드명\" 형식", "지점별 description 작성: 지역 특성 + 핵심 서비스 + CTA 1줄 (지점 매니저가 직접 작성한 톤)", "변수 기반 자동 생성 + 사람의 미세 조정 병행 (지역명만 바뀌면 안 됨, 본문 내용 일부 반영)", "시즌·이벤트별로 일부 지점 메타 분기 갱신"],
                results=["지점 페이지 평균 CTR 회복", "지역 검색에서 같은 노출수 대비 클릭 증가", "작업 기간 약 6주"],
                caveats="자동 생성된 메타가 너무 동일한 패턴이면 구글이 본문에서 자동 추출한 디스크립션으로 대체하는 경우가 있습니다. 패턴이라도 변형이 필요합니다.",
                tools=["GSC 검색 실적 (쿼리·페이지별 CTR)", "title/description 길이 측정기", "Screaming Frog 메타 추출", "A/B 메타 시트"],
                verification="메타 재작성 후 4주·8주 시점에 GSC '검색 실적'에서 페이지별 CTR이 회복되는지, 같은 노출 수 대비 클릭 수가 증가하는지를 추적했습니다. 일부 지점은 자동 추출로 대체된 케이스가 있어 본문도 같이 손봤습니다.",
                comment="\"브랜드명 - 공식 사이트\" 패턴이 가장 안 좋습니다. 검색자는 \"○○동\"으로 검색했는데 결과에 지역명이 안 보이면 1초 안에 다른 결과를 클릭합니다.",
                insight="title의 첫 8~10자가 가장 중요했습니다. 지역명을 맨 앞에 두고 그 뒤에 서비스·차별점·브랜드를 배치한 패턴이 CTR 회복에 가장 안정적이었습니다.",
                checklist=["지점 페이지 title이 지점마다 다른지", "description이 사람이 작성한 1~2 문장인지", "title이 50~60자, description이 130~160자 안에 들어가는지"],
                related_service=("지역 SEO 서비스", "/services/local-seo/"),
                related_insight=("신규 매장 네이버 플레이스 첫 30일", "/insights/local-seo/new-store-naver-place/")
            ) +
            '</div></div></section>'

            # CTA
            '<section class="section section-cta"><div class="container cta-grid">'
            '<div><h2>우리 지점·매장은 어디에 해당할까요?</h2><p>현재 지역 검색 상태를 진단해 어느 시나리오에 해당하는지, 어떤 우선순위로 작업해야 하는지 24시간 내 분석 리포트를 보내드립니다.</p></div>'
            '<div class="cta-actions"><a href="https://t.me/googleseolab" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-lg">무료 지역 SEO 진단 받기 →</a><a href="/services/local-seo/" class="btn btn-outline btn-lg btn-light">지역 SEO 서비스 보기</a></div>'
            '</div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"지역 SEO 사례","url":"https://onesearchpro.org/case-studies/local-seo/","description":"지역 키워드·랜딩페이지·중복 정리·내부링크·지도·메타 6대 시나리오 지역 SEO 작업 기록","isPartOf":{"@type":"WebSite","name":"OneSearchPro"}}</script>',
        "active": "cases",
    },

    "/case-studies/content/": {
        "title": "콘텐츠 개선 사례 | 검색 의도·H태그·E-E-A-T·내부링크 | OneSearchPro",
        "desc": "검색 의도 불일치, H태그 구조, 키워드 과잉, 얇은 콘텐츠, FAQ 추가, E-E-A-T 신호, 내부 링크까지 — 콘텐츠 개선 7대 시나리오 실무 작업 기록.",
        "keywords": "콘텐츠 SEO 사례, 검색 의도 불일치, H태그 구조, 키워드 스터핑, 얇은 콘텐츠, FAQ 스키마, E-E-A-T",
        "h1": "콘텐츠 개선 사례",
        "eyebrow": "CONTENT IMPROVEMENT CASES",
        "lead": "Google은 도움이 되는 콘텐츠가 독창적인 정보, 충분한 설명, 뻔하지 않은 분석을 제공하는지 스스로 평가하라고 안내합니다. 따라서 콘텐츠 SEO 사례에서는 \"몇 글자 작성\"보다 무엇을 보강했고 왜 좋아졌는지를 보여주는 게 중요합니다.",
        "body": (
            # 7대 시나리오 인덱스
            '<section class="section case-index"><div class="container">'
            '<div class="section-head left"><span class="eyebrow">QUICK INDEX</span><h2>이 페이지에서 다루는 7가지 콘텐츠 개선 시나리오</h2><p>어느 상황에 해당하는지 먼저 골라 보고, 사례 카드로 이동하세요.</p></div>'
            '<div class="case-index-grid">'
            '<a href="#search-intent" class="case-index-item"><span class="case-index-num">01</span><div><b>검색 의도 불일치</b><span>잘 쓴 페이지인데 노출되지 않는 사이트의 SERP 분석</span></div></a>'
            '<a href="#heading-structure" class="case-index-item"><span class="case-index-num">02</span><div><b>H태그 구조 개선</b><span>H1·H2·H3 계층이 무너진 사이트의 헤딩 재구성</span></div></a>'
            '<a href="#keyword-stuffing" class="case-index-item"><span class="case-index-num">03</span><div><b>키워드 과잉 반복 수정</b><span>본문에 타겟 키워드가 30번 박힌 페이지 자연화</span></div></a>'
            '<a href="#thin-content" class="case-index-item"><span class="case-index-num">04</span><div><b>얇은 콘텐츠 보강</b><span>본문 300자 미만 페이지의 정보 완전성 회복</span></div></a>'
            '<a href="#faq-addition" class="case-index-item"><span class="case-index-num">05</span><div><b>FAQ 추가</b><span>사용자 질문이 답변되지 않은 페이지의 FAQ 섹션 신설</span></div></a>'
            '<a href="#eeat-signals" class="case-index-item"><span class="case-index-num">06</span><div><b>E-E-A-T 요소 보강</b><span>익명·일반론 글의 저자·경험·출처 신호 추가</span></div></a>'
            '<a href="#content-internal-link" class="case-index-item"><span class="case-index-num">07</span><div><b>내부링크 삽입</b><span>본문에 컨텍스트 링크 없는 글의 권위 흐름 형성</span></div></a>'
            '</div></div></section>'

            # Case 1 — 검색 의도 불일치
            '<section class="section" id="search-intent"><div class="container">'
            '<div class="case-section-head"><span class="case-num">01</span><span class="eyebrow">SEARCH INTENT MISMATCH</span><h2>검색 의도 불일치</h2><p class="lead">콘텐츠는 잘 썼는데 노출이 안 되는 경우, 대부분 \"무엇을 썼는가\" 가 아니라 \"이 키워드의 SERP에 맞는 형식인가\" 가 문제입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="MEDIA",
                icon="🎯",
                h3="잘 쓴 페이지인데 노출 안 되는 사이트 — SERP 분석 기반 재정렬",
                problem="키워드 리서치를 통해 \"트래픽 잠재력이 있다\" 고 판단해 작성한 글들이, 막상 검색 결과에서 거의 노출되지 않았습니다. 본문 품질·길이는 충분했지만 검색에 잡히지 않는 패턴이 누적되었습니다.",
                diagnosis="타겟 키워드의 실제 SERP는 \"비교 표·추천 리스트·후기\" 같은 상업형/탐색형 콘텐츠가 상위였는데, 작성된 페이지는 \"○○란 무엇인가\" 같은 정보형 일반 정의 글이었습니다. 검색 의도와 페이지 유형이 어긋난 상태였습니다.",
                improvements=["타겟 키워드별로 실제 SERP 상위 10개 결과 유형 분석 (블로그/상품/비교/동영상 분포)", "페이지 유형을 검색 의도에 맞게 재정렬 (정의 글 → 비교/추천 가이드 / 일반 정보 → 사례·후기 글)", "메타·H1·인트로의 표현을 검색자 표현으로 재작성 (\"○○ 추천\", \"○○ 비교\" 등)", "한 키워드가 의도가 혼재된 경우 의도별로 페이지 분리"],
                results=["검색 의도 일치 페이지의 노출·CTR 회복", "기존에 못 잡던 일부 키워드 1페이지 진입", "작업 기간 약 3개월"],
                caveats="의도를 바꾸면 기존에 노출되던 일부 키워드는 손실될 수 있습니다. 의도 변경 전 영향 키워드 시뮬레이션이 필요합니다.",
                tools=["GSC 검색 실적", "Ahrefs SERP 비교", "SERP 의도 분류 시트", "SurferSEO SERP Analyzer"],
                verification="의도 재정렬 후 6주·12주 시점에 GSC에서 타겟 키워드의 노출·평균 게재순위·CTR 변화를 비교했습니다. 의도가 바뀐 페이지는 기존 노출 키워드의 손실 여부도 함께 점검했습니다.",
                comment="\"잘 쓴 글\"이라는 평가는 검색엔진 기준이 아니라 사람 기준입니다. SERP 상위 10개가 비교·리스트형이면 우리 페이지도 그 형식이어야 노출 자체가 시작됩니다.",
                insight="의도를 \"정의 → 비교\"로 바꾼 케이스에서 가장 큰 변화가 있었습니다. 인트로 한 문단과 첫 H2만 바꿔도 노출 회복이 시작된 사례가 다수입니다.",
                checklist=["타겟 키워드의 실제 SERP 상위 10개 형식이 우리 페이지와 같은지", "메타·H1·인트로의 표현이 검색자 표현인지", "한 키워드에 의도가 혼재되면 페이지가 분리되어 있는지"],
                related_service=("콘텐츠 SEO 서비스", "/services/content-seo/"),
                related_insight=("Helpful Content System 셀프 점검", "/insights/google-seo/helpful-content-self-check/")
            ) +
            '</div></div></section>'

            # Case 2 — H태그 구조 개선
            '<section class="section section-soft" id="heading-structure"><div class="container">'
            '<div class="case-section-head"><span class="case-num">02</span><span class="eyebrow">HEADING STRUCTURE</span><h2>H태그 구조 개선</h2><p class="lead">H1이 여러 개거나 없거나, H2 없이 H3부터 시작되는 페이지는 검색엔진이 정보 계층을 파악하기 어렵습니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="B2B",
                icon="📐",
                h3="H1·H2·H3 계층이 무너진 사이트 — 헤딩 재구성",
                problem="검수해보니 한 페이지에 H1이 2~3개 있거나, H1 없이 H2부터 시작하거나, H2 건너뛰고 H3·H4가 등장하는 페이지가 다수. 일부 페이지는 디자인 목적의 큰 글자(<code>&lt;div class=\"big\"&gt;</code>)를 사용하고 실제 의미적 헤딩(<code>&lt;h1&gt;</code>)은 페이지에 없는 케이스도 있었습니다.",
                diagnosis="페이지의 정보 계층을 검색엔진이 명확히 파악할 단서가 부족. 일부 페이지는 H1이 페이지 주제가 아닌 사이트 로고 텍스트인 경우도 있었습니다.",
                improvements=["페이지당 H1 1개 원칙 적용 (페이지 주제를 정확히 명시)", "H2는 본문 섹션 단위로 4~7개, H3는 H2 하위만 사용", "헤딩 텍스트를 검색 의도가 드러나는 자연 문장으로 재작성 (키워드만 박지 않음)", "디자인 헤딩과 의미적 헤딩 분리 — 큰 글자는 CSS로, 의미적 계층은 HTML로"],
                results=["페이지 구조 명확화로 색인 효율 회복", "검색 결과 스니펫에 페이지 구조가 더 잘 반영됨", "작업 기간 약 6주"],
                caveats="기존 헤딩 변경은 디자인 시스템과 함께 검토해야 합니다. H 태그 의미를 무시하고 디자인용으로 쓰던 케이스라면 CSS 전면 점검 필요.",
                tools=["Screaming Frog 헤딩 추출", "Wave WebAIM 접근성 점검", "HTML5 Outliner", "CSS 헤딩 클래스 매핑 시트"],
                verification="헤딩 재구성 후 Screaming Frog로 페이지별 H1 개수·H 태그 시퀀스 무결성을 점검했습니다. 접근성 점검은 WebAIM Wave로 헤딩 순서 경고가 사라졌는지도 확인했습니다.",
                comment="\"디자인용 큰 글자\"를 H 태그로 쓴 케이스가 가장 자주 보입니다. 디자인은 CSS, 의미 구조는 HTML — 이 원칙만 지키면 대부분 해결됩니다.",
                insight="H1을 페이지 주제 문장으로 바꾸자 검색 결과 스니펫의 강조 표시가 더 정확해진 케이스가 많았습니다. 헤딩은 사람·검색엔진 모두에게 페이지 지도 역할을 합니다.",
                checklist=["페이지당 H1이 정확히 1개인지", "H2 없이 H3·H4가 등장하는 페이지가 있는지", "H 태그가 디자인용으로 쓰이지는 않는지"],
                related_service=("기술 SEO 진단", "/services/technical-seo/"),
                related_insight=("쇼핑몰 제품 페이지 6단락 구조", "/insights/content-seo/product-page-content-structure/")
            ) +
            '</div></div></section>'

            # Case 3 — 키워드 과잉 반복
            '<section class="section" id="keyword-stuffing"><div class="container">'
            '<div class="case-section-head"><span class="case-num">03</span><span class="eyebrow">KEYWORD STUFFING</span><h2>키워드 과잉 반복 수정</h2><p class="lead">옛 SEO 관행(\"키워드 밀도 2~3% 유지\")의 잔재로 본문에 타겟 키워드를 30번씩 박은 페이지가 적지 않습니다. 현재 알고리즘은 자연스러움을 평가합니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="LEGACY SITE",
                icon="🔁",
                h3="본문에 타겟 키워드가 30번 박힌 페이지 — 자연 분포 회복",
                problem="과거 외주 SEO 작업의 결과로 일부 페이지의 본문에 타겟 키워드가 30~50번 등장. 첫 100자에 같은 키워드가 5번씩 박혀있고 사람이 읽기 어색한 패턴이었습니다. 일부 페이지는 노출 자체가 떨어지는 상태였습니다.",
                diagnosis="현재 구글 알고리즘은 키워드 밀도를 직접 평가하지 않고 자연스러움·검색 의도 매칭을 봅니다. 키워드 스터핑은 신호가 강해지지 않을 뿐 아니라 일정 임계 이상이면 품질 점수 하락으로 이어질 수 있습니다.",
                improvements=["강제 반복된 키워드를 동의어·대명사·관련 표현으로 자연 분포 회복", "첫 100자의 키워드 스터핑 제거 후 검색자 표현·문맥으로 재작성", "타이틀·H1·H2에는 키워드를 1번씩만 자연스럽게 배치", "토픽 신호는 동의어·관련어·문맥으로 보강 (키워드 횟수가 아니라 토픽 깊이)"],
                results=["본문 가독성·체류시간 회복", "일부 페이지의 순위 회복 추세", "작업 기간 약 8주"],
                caveats="키워드를 \"한 번도 안 쓰는\" 수준까지 줄이면 토픽 신호가 약해질 수 있습니다. 자연스러운 분포 회복이 목표이지 제거가 아닙니다.",
                tools=["키워드 빈도 카운터(자체 스크립트)", "Hemingway Editor 가독성 점검", "Ahrefs Content Gap", "GA4 체류시간 리포트"],
                verification="키워드 자연 분포 작업 후 8주·16주 시점에 GSC 게재순위 변화와 GA4 페이지별 평균 체류 시간을 비교했습니다. 본문 가독성은 Hemingway 점수로도 측정해 가독성과 순위 회복이 함께 가는지 확인했습니다.",
                comment="\"키워드는 많이 박을수록 좋다\"는 인식은 2010년대 초중반 SEO 잔재입니다. 현재 알고리즘은 자연스러운 문맥과 토픽 깊이를 봅니다.",
                insight="키워드 횟수를 줄이고 그 자리에 동의어·관련어·사용자 표현을 배치하자 오히려 더 많은 롱테일 키워드에서 노출이 시작되었습니다.",
                checklist=["첫 100자에 같은 키워드가 3번 이상 등장하는지", "본문 키워드 밀도가 3%를 넘는 페이지가 있는지", "헤딩에 키워드가 자연스러운 문장으로 들어가는지"],
                related_service=("콘텐츠 SEO 서비스", "/services/content-seo/"),
                related_insight=("Helpful Content System 셀프 점검", "/insights/google-seo/helpful-content-self-check/")
            ) +
            '</div></div></section>'

            # Case 4 — 얇은 콘텐츠 보강
            '<section class="section section-soft" id="thin-content"><div class="container">'
            '<div class="case-section-head"><span class="case-num">04</span><span class="eyebrow">THIN CONTENT</span><h2>얇은 콘텐츠 보강</h2><p class="lead">본문이 300자도 안 되는 페이지는 단순히 글자를 늘리는 게 답이 아닙니다. \"사용자가 진짜 알고 싶은 정보가 빠졌는가\"를 봐야 합니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="ECOMMERCE",
                icon="📄",
                h3="본문 300자 미만 페이지 — 정보 깊이 보강",
                problem="제품 카테고리·태그·기본 정보 페이지의 본문이 매우 짧음. 일부 제품 페이지는 사진과 가격·옵션만 있고 텍스트 본문이 사실상 비어있는 상태. 검색엔진이 \"이 페이지는 색인 가치가 적다\"고 판단해 일부는 색인조차 되지 않았습니다.",
                diagnosis="Helpful Content System에서 가장 쉽게 잡히는 패턴. 다만 단순 글자 수 증가로 해결되지 않습니다. 사용자가 페이지에 와서 답을 얻고 싶은 정보 자체가 빠져있는 게 핵심.",
                improvements=["페이지별로 \"사용자가 와서 답을 얻고 싶은 5~7가지 질문\" 리서치 (서치콘솔 쿼리·People Also Ask·실제 CS 문의 기반)", "누락된 정보 추가 — 사용법·사양·비교 기준·결정 가이드·FAQ", "검색 의도와 매칭 안 되는 페이지는 통합·삭제 검토 (글자 수 늘리기로 해결되지 않는 경우)", "단순 글자 수보다 \"검색자가 원하는 정보의 완전성\" 기준 적용"],
                results=["색인 가치 평가 회복으로 일부 페이지 노출 시작", "체류 시간·재방문 회복", "작업 기간 약 3개월"],
                caveats="페이지의 \"존재 이유\" 자체가 모호한 경우는 글자 수 늘려도 효과 없습니다. 페이지 자체를 통합·삭제하는 게 정답일 때도 있습니다.",
                tools=["GSC 검색 실적·쿼리 리포트", "People Also Ask 추출 도구", "AlsoAsked", "CS 문의 로그 분석"],
                verification="얇은 콘텐츠 보강 후 8주·16주 시점에 GSC '색인 적용 범위'에서 '크롤링됨 - 현재 색인되지 않음' 페이지 수가 줄어드는지, 보강 페이지의 노출·CTR 변화도 함께 확인했습니다.",
                comment="\"본문 1000자 채워라\"는 가이드는 가장 흔한 오해입니다. 사용자가 원하는 정보 7가지가 빠져있으면 글자 수를 늘려도 신호가 약해지지 않습니다.",
                insight="가장 효과가 큰 보강 항목은 'FAQ'와 '비교 표'였습니다. 두 가지 모두 검색자가 페이지에서 답을 즉시 얻을 수 있게 해주는 구조입니다.",
                checklist=["페이지가 답해야 할 사용자 질문 5~7개가 본문에 들어 있는지", "단순 글자 수 채우기가 아니라 정보 깊이가 증가했는지", "통합·삭제가 더 나은 페이지가 아닌지"],
                related_service=("콘텐츠 SEO 서비스", "/services/content-seo/"),
                related_insight=("쇼핑몰 제품 페이지 6단락 구조", "/insights/content-seo/product-page-content-structure/")
            ) +
            '</div></div></section>'

            # Case 5 — FAQ 추가
            '<section class="section" id="faq-addition"><div class="container">'
            '<div class="case-section-head"><span class="case-num">05</span><span class="eyebrow">FAQ ENHANCEMENT</span><h2>FAQ 추가</h2><p class="lead">사용자가 검색 후 페이지에 들어와도 궁금한 점이 답변되지 않으면 즉시 뒤로가기로 이탈합니다. 이탈 신호는 누적됩니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="SAAS · SERVICE",
                icon="❓",
                h3="사용자 질문이 본문에 답변되지 않은 페이지 — FAQ 섹션 신설",
                problem="서비스·제품 페이지가 \"우리 입장의 설명\" 으로만 작성되어 있고, 사용자가 실제로 궁금해할 질문(가격 구조, 환불 정책, 호환성, 사용법 등)에 대한 답변이 본문에 없었습니다. People Also Ask 영역에 노출되지 않아 부가 트래픽 손실도 컸습니다.",
                diagnosis="페이지가 \"브랜드가 말하고 싶은 내용\" 중심으로 구성됨. 사용자 질문 관점 부재. FAQPage 스키마도 미적용으로 검색 결과의 리치 스니펫 노출 손실까지 있었습니다.",
                improvements=["실제 CS 문의·서치콘솔 People Also Ask·관련 검색어로 FAQ 5~10개 추출", "페이지 하단에 FAQ 섹션 신설 (질문 형태 그대로, 사용자 표현 사용)", "FAQPage 스키마 마크업 적용", "답변은 짧고 구체적으로 (스니펫에 그대로 표시될 수 있는 길이)"],
                results=["일부 페이지의 People Also Ask 영역 노출 시작", "체류 시간·재방문 회복", "작업 기간 약 6주"],
                caveats="가짜 FAQ(만들어낸 질문)는 즉시 들킵니다. 실제 받은 질문만 사용. 답변에 \"보장\"·\"확실\" 같은 표현은 정책 위반 위험이 있습니다.",
                tools=["GSC People Also Ask 추출", "AlsoAsked", "Schema Markup Validator", "Rich Results Test"],
                verification="FAQPage 스키마 적용 후 Schema Validator·Rich Results Test로 무오류를 확인하고, 8주 동안 GSC '검색 외관'에서 FAQ 리치 결과 노출 수가 증가하는지 추적했습니다.",
                comment="실제 CS에 가장 자주 들어온 질문 5개만 본문에 자연스럽게 답해도 People Also Ask 영역 노출이 시작됩니다. 인위적으로 만든 질문은 효과가 거의 없습니다.",
                insight="FAQ 답변 길이를 짧고 구체적으로(40~80자) 작성한 페이지가 리치 스니펫 노출률이 가장 높았습니다. 답변이 길면 스니펫이 안 잡힙니다.",
                checklist=["FAQ가 실제 CS 문의·검색어 기반인지", "FAQPage 스키마가 적용되고 무오류인지", "답변에 '보장·확실·100%' 같은 표현이 없는지"],
                related_service=("콘텐츠 SEO 서비스", "/services/content-seo/"),
                related_insight=("의료 블로그 첫 100편 운영", "/insights/content-seo/medical-blog-first-100/")
            ) +
            '</div></div></section>'

            # Case 6 — E-E-A-T 요소 보강
            '<section class="section section-soft" id="eeat-signals"><div class="container">'
            '<div class="case-section-head"><span class="case-num">06</span><span class="eyebrow">E-E-A-T SIGNALS</span><h2>E-E-A-T 요소 보강</h2><p class="lead">\"관리자\" 명의의 익명 글, 일반 정보의 재정리만 있는 콘텐츠는 권위·신뢰 신호가 약합니다. 특히 YMYL 인접 영역에서는 치명적입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="B2B · CONSULTING",
                icon="🛡️",
                h3="익명·일반론 콘텐츠 — 저자·경험·출처 신호 추가",
                problem="블로그 글이 모두 \"관리자\" 명의로 발행. 본문은 일반 정보를 재정리한 수준이라 \"누가 어떤 경험과 전문성으로 작성했는지\" 신호가 부재. 전문 키워드에서 경쟁사 대비 노출이 약했습니다.",
                diagnosis="E-E-A-T(Experience·Expertise·Authoritativeness·Trustworthiness) 4가지 신호 모두 부족. 특히 Experience(직접 경험) 신호 부재가 컸습니다.",
                improvements=["저자 페이지 신설 + Person 스키마 적용 (경력·자격·발표 이력 명시)", "본문에 저자의 실무 경험·관찰 자연스럽게 녹임 — \"실무에서 자주 본 패턴은…\", \"○○ 도구를 5년 운영하면서…\"", "외부 1차 자료·공식 문서·권위 매체 인용 (출처 명시)", "발행일·수정일 가시적 표시 + 정기 갱신 사이클 운영", "외부 매체 기고로 외부 권위 신호 누적"],
                results=["전문 키워드에서 노출·체류시간 개선 추세", "코어 업데이트 영향이 점차 안정화", "작업 기간 약 6개월"],
                caveats="E-E-A-T 신호는 빠르게 만들어지지 않습니다. 6개월 이상의 누적 작업과 진정성 있는 활동이 필요하며, 가짜 저자·가짜 자격은 역효과입니다.",
                tools=["Schema.org Person 마크업", "Ahrefs 외부 권위 점검", "GSC 검색 실적(전문 키워드 그룹)", "저자 페이지 관리 시트"],
                verification="저자 페이지 신설·Person 스키마 적용 후 12주 동안 전문 키워드 그룹의 평균 게재순위 변화를 추적했습니다. 코어 업데이트 시점의 변동성도 비교 기준으로 사용했습니다.",
                comment="\"관리자\" 명의 글이 가장 위험합니다. 특히 의료·금융·법률 인접 영역에서는 저자 정보 부재만으로도 노출 자체가 멈춥니다.",
                insight="저자가 외부 매체에 기고한 이력이 누적되자 사이트 전체의 권위 신호가 동반 상승하는 패턴이 관찰되었습니다. E-E-A-T는 사이트 안에서만 만들어지지 않습니다.",
                checklist=["블로그 글에 실명 저자와 저자 페이지 링크가 있는지", "Person 스키마가 적용되었는지", "본문에 직접 경험·관찰 신호가 들어 있는지"],
                related_service=("콘텐츠 SEO 서비스", "/services/content-seo/"),
                related_insight=("Helpful Content System 셀프 점검", "/insights/google-seo/helpful-content-self-check/")
            ) +
            '</div></div></section>'

            # Case 7 — 내부 링크 삽입
            '<section class="section" id="content-internal-link"><div class="container">'
            '<div class="case-section-head"><span class="case-num">07</span><span class="eyebrow">INTERNAL LINKING</span><h2>내부링크 삽입</h2><p class="lead">콘텐츠가 좋아도 본문에서 다른 글로 가는 컨텍스트 링크가 없으면 검색엔진이 사이트 전체 가치를 인식하지 못합니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="MEDIA · BLOG",
                icon="🔗",
                h3="본문에 컨텍스트 링크가 없는 글 — 권위 흐름 형성",
                problem="블로그 글이 100편 넘게 누적되었지만, 본문 한가운데에 다른 글로 가는 컨텍스트 링크는 거의 없었습니다. 사이드바·자동 \"관련 글\" 위젯만 있는 상태로, 한 글 읽고 사용자가 이탈하는 패턴이었습니다.",
                diagnosis="사이드바·자동 추천 위젯의 링크는 검색엔진이 약하게 평가합니다. 본문 안에서 \"○○에 대해 더 알려면 [○○ 가이드 보기]\" 같이 자연스럽게 박힌 텍스트 링크가 권위 신호를 전달하는데, 그게 사실상 없었습니다.",
                improvements=["트래픽 상위 30개 글에 본문 컨텍스트 링크 평균 3~5개 추가 (관련 글·서비스 페이지)", "앵커텍스트를 정확한 타겟 키워드로 통일 (\"여기 클릭\" 금지)", "필러 글 → 클러스터 글 흐름 설계", "오래된 글에는 \"이 주제의 최신 정리\" 링크 추가로 갱신성 신호"],
                results=["사이트 전체 권위 흐름 형성, 평균 페이지뷰·체류시간 회복", "신규 글의 색인 속도도 함께 개선", "작업 기간 약 2개월"],
                caveats="자동 \"관련 글\" 위젯과 본문 컨텍스트 링크는 다릅니다. 본문 컨텍스트가 어색한 위치에 강제 링크를 박으면 역효과이고, 자연스러운 위치에만 배치하는 게 핵심입니다.",
                tools=["Ahrefs Internal Backlinks", "Screaming Frog 내부링크 리포트", "GA4 사용자 흐름 리포트", "내부링크 매핑 시트"],
                verification="컨텍스트 링크 추가 후 8주 동안 GA4의 페이지당 평균 페이지뷰·세션 깊이 변화와 GSC '많이 연결된 페이지' 리스트의 변동을 비교했습니다. 신규 글 색인 속도도 함께 추적했습니다.",
                comment="\"사이드바·자동 관련글이 있으니 충분하다\"는 가정이 가장 흔합니다. 본문 안에 박힌 텍스트 링크가 검색엔진 평가에서 훨씬 더 강하게 작동합니다.",
                insight="필러 글 → 클러스터 글 흐름을 만들고 나서 가장 큰 변화는 신규 글의 색인 속도였습니다. 발행 후 24~48시간 안에 색인되는 비율이 눈에 띄게 늘었습니다.",
                checklist=["본문 한가운데에 컨텍스트 링크가 평균 3~5개 있는지", "앵커텍스트가 정확한 타겟 키워드인지", "필러·클러스터 구조가 설계되어 있는지"],
                related_service=("콘텐츠 SEO 서비스", "/services/content-seo/"),
                related_insight=("쇼핑몰 제품 페이지 6단락 구조", "/insights/content-seo/product-page-content-structure/")
            ) +
            '</div></div></section>'

            # CTA
            '<section class="section section-cta"><div class="container cta-grid">'
            '<div><h2>우리 사이트의 콘텐츠는 어느 시나리오일까요?</h2><p>현재 콘텐츠 상태를 7가지 시나리오에 대조해 어디가 가장 시급한지, 어떤 우선순위로 개선해야 하는지 24시간 내 분석 리포트를 보내드립니다.</p></div>'
            '<div class="cta-actions"><a href="https://t.me/googleseolab" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-lg">무료 콘텐츠 SEO 진단 받기 →</a><a href="/services/content-seo/" class="btn btn-outline btn-lg btn-light">콘텐츠 SEO 서비스 보기</a></div>'
            '</div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"콘텐츠 개선 사례","url":"https://onesearchpro.org/case-studies/content/","description":"검색 의도·H태그·키워드 분포·콘텐츠 깊이·FAQ·E-E-A-T·내부 링크 7대 시나리오 콘텐츠 개선 작업 기록","isPartOf":{"@type":"WebSite","name":"OneSearchPro"}}</script>',
        "active": "cases",
    },

    "/case-studies/web-design/": {
        "title": "SEO 웹사이트 제작 사례 | 메뉴·URL·속도·전환 8대 시나리오 | OneSearchPro",
        "desc": "메뉴 구조, URL 구조, 모바일 반응형, 페이지 속도, 서비스 페이지 구성, 메타 정보, 내부 링크, 문의 전환 구조까지 — 디자인 포트폴리오가 아닌 SEO 구조로 제작한 사이트 8대 시나리오 작업 기록.",
        "keywords": "SEO 웹사이트 제작 사례, 메뉴 구조, URL 구조, 모바일 반응형, Core Web Vitals, 서비스 페이지, 내부 링크, 문의 전환",
        "h1": "웹사이트 제작 사례",
        "eyebrow": "WEB DESIGN CASES",
        "lead": "OneSearchPro의 웹사이트 제작은 단순 디자인 포트폴리오가 아닙니다. 처음부터 검색엔진이 이해할 수 있는 구조·URL·속도·전환 동선을 \"SEO 자산\"으로 설계합니다. 다음은 사이트 제작·리뉴얼 시 자주 다루는 8가지 시나리오의 실제 작업 기록입니다.",
        "body": (
            # 8대 시나리오 인덱스
            '<section class="section case-index"><div class="container">'
            '<div class="section-head left"><span class="eyebrow">QUICK INDEX</span><h2>이 페이지에서 다루는 8가지 SEO 웹사이트 제작 시나리오</h2><p>제작·리뉴얼 시 SEO 관점에서 반드시 점검하는 8가지 영역입니다. 해당 항목으로 바로 이동하세요.</p></div>'
            '<div class="case-index-grid">'
            '<a href="#nav-architecture" class="case-index-item"><span class="case-index-num">01</span><div><b>메뉴 구조</b><span>핵심 페이지에 3클릭 안에 도달 못 하는 사이트</span></div></a>'
            '<a href="#url-architecture" class="case-index-item"><span class="case-index-num">02</span><div><b>URL 구조</b><span>/index.php?id=123 같은 비의미적 URL 정리</span></div></a>'
            '<a href="#mobile-responsive" class="case-index-item"><span class="case-index-num">03</span><div><b>모바일 반응형</b><span>모바일에서 본문·링크가 빠진 사이트의 콘텐츠 패리티</span></div></a>'
            '<a href="#page-speed" class="case-index-item"><span class="case-index-num">04</span><div><b>페이지 속도</b><span>Core Web Vitals 모바일 50점대 사이트 90+ 만들기</span></div></a>'
            '<a href="#service-page-design" class="case-index-item"><span class="case-index-num">05</span><div><b>서비스 페이지 구성</b><span>이미지 위주 빈약한 서비스 페이지 6단락 재설계</span></div></a>'
            '<a href="#meta-info" class="case-index-item"><span class="case-index-num">06</span><div><b>메타 정보</b><span>자동 추출 메타로 CTR 손실 → 페이지별 수동 작성</span></div></a>'
            '<a href="#design-internal-link" class="case-index-item"><span class="case-index-num">07</span><div><b>내부 링크</b><span>고립 페이지가 많은 사이트의 권위 흐름 설계</span></div></a>'
            '<a href="#conversion-structure" class="case-index-item"><span class="case-index-num">08</span><div><b>문의 전환 구조</b><span>트래픽은 오는데 문의가 없는 사이트의 CTA 동선</span></div></a>'
            '</div></div></section>'

            # Case 1 — 메뉴 구조
            '<section class="section" id="nav-architecture"><div class="container">'
            '<div class="case-section-head"><span class="case-num">01</span><span class="eyebrow">NAVIGATION ARCHITECTURE</span><h2>메뉴 구조</h2><p class="lead">사용자가 핵심 페이지에 3클릭 안에 도달하지 못하면 검색엔진 크롤러도 동일합니다. 메뉴는 첫 번째 SEO 구조입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="B2B",
                icon="🧭",
                h3="메뉴가 깊거나 평평한 사이트 — SEO 친화 정보 구조 설계",
                problem="기존 사이트의 메뉴가 4단 깊이까지 들어가야 핵심 서비스 페이지에 도달하는 구조였습니다. 또 다른 케이스에서는 메뉴에 30개 링크가 평평하게 늘어서서 정보 계층이 안 보이는 패턴이 있었습니다.",
                diagnosis="크롤러는 사용자와 비슷하게 사이트를 탐색합니다. 메뉴 깊이가 4단 이상이면 깊은 페이지는 색인 우선순위가 떨어집니다. 반대로 평평한 메뉴는 카테고리 그룹 신호가 약합니다.",
                improvements=["1차 메뉴 5~7개 + 드롭다운 2단으로 제한", "사용자 결정 흐름 기반 메뉴 재배치 (서비스→사례→인사이트→회사→문의)", "메뉴 항목명에 정확한 키워드 포함 (\"서비스\" 단독보다 \"SEO 컨설팅\" 등 구체)", "모바일 햄버거 메뉴에서도 동일 계층 유지"],
                results=["크롤링 효율 회복으로 깊은 페이지 색인 속도 개선", "사용자 동선 단축으로 페이지뷰 증가", "메뉴 재설계 작업 기간 약 3~4주"],
                caveats="메뉴 변경은 기존 사용자 동선에 영향을 줍니다. 변경 전 사용자 행동 데이터를 보고, 변경 후 이탈률 모니터링이 필요합니다.",
                tools=["Screaming Frog 사이트 크롤", "GA4 사용자 동선 리포트", "MS Clarity 클릭 히트맵", "메뉴 트리 매핑 시트"],
                verification="메뉴 재설계 후 4주 동안 GA4 페이지 평균 깊이, GSC 깊은 페이지 색인 적용 상태, Clarity 메뉴 클릭률을 비교했습니다. 이탈률 변화도 별도 추적했습니다.",
                comment="메뉴 깊이 4단 사이트가 가장 자주 보입니다. 사용자도 3클릭 이상 들어가지 않습니다 — 검색엔진도 마찬가지입니다.",
                insight="메뉴 항목명을 \"서비스\"에서 \"SEO 컨설팅·기술 SEO·콘텐츠 SEO\" 같이 구체화하자, 메뉴 자체가 키워드 시그널로도 작동하기 시작했습니다.",
                checklist=["핵심 페이지에 3클릭 안에 도달 가능한지", "1차 메뉴가 5~7개인지", "메뉴 항목명에 정확한 키워드가 있는지"],
                related_service=("SEO 웹사이트 제작", "/services/web-design/"),
                related_insight=("쇼핑몰 제품 페이지 6단락 구조", "/insights/content-seo/product-page-content-structure/")
            ) +
            '</div></div></section>'

            # Case 2 — URL 구조
            '<section class="section section-soft" id="url-architecture"><div class="container">'
            '<div class="case-section-head"><span class="case-num">02</span><span class="eyebrow">URL ARCHITECTURE</span><h2>URL 구조</h2><p class="lead">URL은 검색엔진과 사용자 모두에게 \"이 페이지가 무엇인지\"의 첫 신호입니다. /index.php?id=123 같은 패턴은 즉시 손해입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="LEGACY CMS",
                icon="🔗",
                h3="비의미적 URL 패턴 사이트 — 의미적 URL 재설계와 마이그레이션",
                problem="기존 사이트가 PHP 기반으로 /page.php?cat=4&id=128 같은 파라미터 URL 사용. 카테고리·계층 정보가 URL에 전혀 반영되지 않았고, 같은 페이지가 여러 파라미터 조합으로 접근 가능해 중복 URL이 다수 발생했습니다.",
                diagnosis="의미 없는 URL은 검색엔진과 사용자 모두에게 신호가 약합니다. 또한 파라미터 URL은 트래킹·캠페인 변수에 따라 무한히 늘어나 크롤링 예산을 낭비합니다.",
                improvements=["URL 패턴을 /[category]/[subcategory]/[slug]/ 형식으로 통일", "영문 슬러그 사용 (한글 URL은 인코딩 문제 발생 가능)", "카테고리·서비스 계층을 URL에 반영", "파라미터 URL은 canonical 또는 noindex로 정리", "기존 URL과 새 URL 1:1 301 매핑 시트 작성"],
                results=["URL 자체가 키워드 신호로 작동", "중복 URL 정리로 크롤링 예산 회복", "색인된 핵심 페이지의 검색 노출 회복"],
                caveats="URL 변경 시 반드시 모든 기존 URL의 1:1 301 매핑 필수. 누락되면 트래픽 손실이 수개월 이어집니다.",
                tools=["Screaming Frog", "GSC URL 검사", "301 매핑 시트", "Ahrefs Site Audit"],
                verification="URL 마이그레이션 후 4주·8주 시점에 GSC '색인 적용 범위'의 오류·제외 페이지 변화, 평균 게재순위, 404 발생 추이를 함께 추적했습니다. 매핑 누락 케이스가 발견되면 즉시 301 추가했습니다.",
                comment="\"리뉴얼하면서 URL 좀 바꿨다\"는 말이 가장 위험합니다. 1:1 301 매핑 시트 없이 진행한 리뉴얼은 거의 예외 없이 트래픽이 절반으로 떨어집니다.",
                insight="파라미터 URL을 의미적 URL로 바꾸자 동일 페이지의 평균 게재순위가 자연 상승한 케이스가 있었습니다. URL 자체가 약하지만 분명한 시그널입니다.",
                checklist=["URL이 카테고리·계층을 반영하는지", "파라미터 URL이 canonical로 정리됐는지", "기존 URL → 새 URL 1:1 301 매핑 시트가 있는지"],
                related_service=("SEO 웹사이트 제작", "/services/web-design/"),
                related_insight=("301 리다이렉트 자주 빠뜨리는 12가지", "/insights/visibility/301-migration-mistakes/")
            ) +
            '</div></div></section>'

            # Case 3 — 모바일 반응형
            '<section class="section" id="mobile-responsive"><div class="container">'
            '<div class="case-section-head"><span class="case-num">03</span><span class="eyebrow">MOBILE FIRST</span><h2>모바일 반응형</h2><p class="lead">구글은 모바일 우선 색인입니다. 모바일에서 안 보이는 콘텐츠는 사실상 색인되지 않습니다. \"반응형\"이라도 콘텐츠 패리티는 별도 점검이 필요합니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="ECOMMERCE",
                icon="📱",
                h3="모바일 콘텐츠가 빠진 사이트 — 모바일 우선 색인 대응 제작",
                problem="PC 기준으로 잘 만들어진 사이트지만 모바일에서는 사이드바·일부 본문·내부 링크가 <code>display:none</code> 처리되어 보이지 않는 상태. 모바일 viewport 메타 누락 페이지도 있었고, 터치 타겟 크기·가독성 기준도 미준수했습니다.",
                diagnosis="모바일 우선 색인은 \"모바일에서 보이는 게 색인 기준\"이 됩니다. 데스크탑에만 있는 본문·이미지·내부 링크는 사실상 색인되지 않는 셈입니다. 콘텐츠 패리티(데스크탑/모바일 일치) 실패 케이스였습니다.",
                improvements=["모바일에서 <code>display:none</code> 처리된 본문·링크 점검 후 복원", "<code>viewport</code> 메타 적용, 본문 폰트 16px 이상, 탭 영역 48×48px+", "모바일 친화성 테스트 통과", "구조화 데이터·내부 링크가 모바일에서도 동일하게 출력되는지 점검", "모바일 LCP·INP·CLS 별도 측정·최적화"],
                results=["모바일 키워드 노출 회복", "모바일 트래픽이 데스크탑 수준으로 회복", "작업 기간 약 4주"],
                caveats="별도 모바일 도메인(m.example.com)은 관리 부담만 큽니다. 반응형 단일 사이트가 정답입니다.",
                tools=["Chrome DevTools Device Toolbar", "PageSpeed Insights Mobile", "GSC 모바일 사용 편의성", "Lighthouse"],
                verification="모바일 콘텐츠 패리티 작업 후 GSC '모바일 사용 편의성' 오류 페이지 수, 모바일 노출·CTR, Field Data의 모바일 LCP·INP·CLS를 4주 단위로 비교했습니다.",
                comment="\"반응형이니까 모바일도 자동으로 잘 보일 것\"이라는 가정이 가장 흔합니다. 실제로는 display:none으로 숨긴 본문·내부 링크가 색인에서 빠집니다.",
                insight="모바일에서 본문을 복원하자 모바일 키워드 노출이 데스크탑 수준에 도달하는 데 6주면 충분했습니다. 색인 자체가 빠르게 갱신됩니다.",
                checklist=["모바일에서 display:none으로 숨긴 본문·링크가 없는지", "viewport 메타가 있고 폰트가 16px 이상인지", "터치 타겟이 48×48px 이상인지"],
                related_service=("기술 SEO 진단", "/services/technical-seo/"),
                related_insight=("모바일 우선 색인 점검 가이드", "/insights/technical-seo/mobile-first-indexing/")
            ) +
            '</div></div></section>'

            # Case 4 — 페이지 속도
            '<section class="section section-soft" id="page-speed"><div class="container">'
            '<div class="case-section-head"><span class="case-num">04</span><span class="eyebrow">PAGE SPEED</span><h2>페이지 속도</h2><p class="lead">PageSpeed 점수보다 중요한 건 사용자 환경에서 측정된 Field Data입니다. 구글이 랭킹에 쓰는 건 실제 사용자 데이터입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="WORDPRESS",
                icon="⚡",
                h3="Core Web Vitals 모바일 50점대 사이트 — 90+ 만들기 작업",
                problem="PageSpeed Insights 모바일 점수가 30~50점대로 정체. LCP 4초 이상, CLS 0.25 초과, INP 200ms 이상으로 Core Web Vitals 기준치 초과. 모바일 검색 노출에 부정적 영향이 있는 상태였습니다.",
                diagnosis="Hero 이미지가 압축 안 된 4MB PNG, 폰트가 차단 렌더링, 무거운 플러그인·CSS/JS, 호스팅 TTFB 1초 초과 등이 복합 원인이었습니다.",
                improvements=["Hero 이미지 WebP 변환 + 모바일용 별도 srcset, fetchpriority high", "한글 폰트 swap·preload·subset 적용", "사용 안 하는 CSS/JS 제거 또는 lazy loading", "캐싱 플러그인 + Cloudflare CDN 도입으로 TTFB 단축", "Core Web Vitals Field Data를 서치콘솔에서 지속 추적"],
                results=["모바일 PageSpeed 점수 90+ 진입", "LCP 1.5~2초대로 단축", "Field Data 기준 \"Good\" 비율 증가"],
                caveats="PageSpeed Lab 점수와 Field Data가 다를 수 있습니다. 구글은 Field Data를 랭킹 신호로 사용하므로 실측 기반 모니터링이 필수입니다.",
                tools=["PageSpeed Insights", "Lighthouse CI", "Cloudflare 대시보드", "GSC Core Web Vitals 리포트"],
                verification="속도 최적화 후 12주 동안 GSC '주요 사이트 정보(Core Web Vitals)' 리포트의 'Good' 비율이 증가하는지, Field Data 기준 LCP·INP·CLS 변화를 추적했습니다.",
                comment="\"Lab 점수 90점\"이 목표가 아니라 실제 사용자 환경의 Field Data가 'Good'인 게 목표입니다. Lab은 깨끗한 환경에서 측정되므로 항상 더 좋게 나옵니다.",
                insight="Hero 이미지 1장만 WebP + fetchpriority high 적용해도 LCP가 1초 이상 단축된 케이스가 있었습니다. 최우선 작업은 LCP 이미지입니다.",
                checklist=["Field Data 기준 모바일 LCP가 2.5초 이내인지", "INP가 200ms 이내인지", "CLS가 0.1 이내인지"],
                related_service=("기술 SEO 진단", "/services/technical-seo/"),
                related_insight=("워드프레스 LCP 개선 작업 순서", "/insights/technical-seo/wordpress-lcp-fix/")
            ) +
            '</div></div></section>'

            # Case 5 — 서비스 페이지 구성
            '<section class="section" id="service-page-design"><div class="container">'
            '<div class="case-section-head"><span class="case-num">05</span><span class="eyebrow">SERVICE PAGE</span><h2>서비스 페이지 구성</h2><p class="lead">서비스 페이지는 검색 의도(거래형) 매칭 + 전환 동선이 핵심입니다. 본문이 없으면 둘 다 실패합니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="B2B · SAAS",
                icon="💼",
                h3="이미지 위주 빈약한 서비스 페이지 — 전환 + SEO 통합 6단락 재구성",
                problem="서비스 페이지가 이미지 위주로 구성되고 본문이 거의 없었습니다. 사용자가 어떤 서비스인지, 가격·차별점·결과를 알기 어려웠고, 검색에서도 거래형 키워드(\"서비스명 + 가격\", \"비교\")에서 노출되지 않았습니다.",
                diagnosis="서비스 페이지는 \"정보 + 전환\" 두 역할을 동시에 해야 하는데, 본문 부재로 검색엔진 신호(SEO)와 사용자 결정(전환) 둘 다 잡지 못하는 상태였습니다.",
                improvements=["서비스별 6단락 구조: ① 대상 고객, ② 해결할 문제, ③ 해결 방식, ④ 차별점·증거, ⑤ 프로세스, ⑥ FAQ", "Service / Offer 스키마 적용", "기간·결과물·범위 명시 (\"보장\" 표현 없이 \"기준\"·\"목표\"·\"평균\" 표현 사용)", "관련 사례·블로그 글로 본문 내 컨텍스트 링크", "페이지 하단 명확한 CTA + 신뢰 신호 (실적·후기·법적 정보)"],
                results=["거래형 키워드에서 서비스 페이지가 직접 노출", "문의 전환율 회복 추세", "재구성 기간 약 6주"],
                caveats="가격 비공개 정책이면 가격 대신 \"프로젝트 단위 견적\"으로 안내하되, 범위·기간은 반드시 명시해야 신뢰가 형성됩니다.",
                tools=["GSC 거래형 키워드 모니터", "Schema Markup Validator", "GA4 전환 이벤트", "MS Clarity 스크롤·클릭 히트맵"],
                verification="서비스 페이지 재구성 후 GA4 전환 이벤트, GSC '검색 외관' 의 Service/Offer 리치 결과 노출, Clarity 스크롤 깊이를 8주 단위로 비교했습니다.",
                comment="이미지만 잔뜩 박힌 서비스 페이지는 결국 영업 자료를 PDF로 받아본 사람만 결정합니다. 본문이 있어야 검색에서 발견되고, 발견된 사람이 결정합니다.",
                insight="6단락 중 가장 전환에 기여한 단락은 '차별점·증거'와 'FAQ'였습니다. 결정 직전 사용자에게 가장 필요한 정보가 그 두 단락에 들어 있기 때문입니다.",
                checklist=["서비스 페이지에 6단락 구조가 있는지", "Service/Offer 스키마가 적용됐는지", "'보장·확실' 표현 없이 '기준·평균'으로 명시되는지"],
                related_service=("SEO 웹사이트 제작", "/services/web-design/"),
                related_insight=("쇼핑몰 제품 페이지 6단락 구조", "/insights/content-seo/product-page-content-structure/")
            ) +
            '</div></div></section>'

            # Case 6 — 메타 정보
            '<section class="section section-soft" id="meta-info"><div class="container">'
            '<div class="case-section-head"><span class="case-num">06</span><span class="eyebrow">META INFO</span><h2>메타 정보</h2><p class="lead">메타는 SERP의 입구입니다. 자동 추출에 맡기면 사용자가 클릭할 후크가 없습니다. 페이지별 수동 작성이 필수입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="MULTI-PAGE",
                icon="🏷️",
                h3="자동 생성된 메타가 클릭률을 낮추는 사이트 — 페이지별 수동 작성",
                problem="title이 모든 페이지에 \"회사명 - 페이지명\" 패턴으로 자동 생성. description은 입력 안 된 상태라 본문 첫 문장이 자동 추출되어 \"안녕하세요, ○○ 회사입니다\" 같은 의미 없는 텍스트가 검색 결과에 노출되었습니다.",
                diagnosis="메타는 SERP에서 사용자가 우리 페이지를 클릭할지 결정하는 핵심 후크입니다. 자동 추출은 통제 불가능하고, 클릭 후크가 없어 같은 노출수에서도 클릭이 빠집니다.",
                improvements=["페이지별 title 50~60자 (1차 키워드 + 클릭 후크 + 브랜드)", "description 120~155자 (가치·차별점·CTA 한 줄)", "OG title·description 별도 작성 (SNS 공유 카피와 SERP 카피 분리)", "구조화 데이터로 리치 결과 유도 (FAQPage, Review, Product 등 페이지 유형별)"],
                results=["평균 CTR 회복", "같은 노출수에서 클릭 증가", "메타 작성·검수 작업 기간 약 3~4주 (페이지 수에 비례)"],
                caveats="자동 생성 도구 활용 시에도 페이지마다 검수 필수. 동일 패턴이면 구글이 자동 추출로 대체하기도 합니다.",
                tools=["GSC 검색 실적(CTR)", "Screaming Frog 메타 추출", "title/description 길이 측정기", "Rich Results Test"],
                verification="페이지별 메타 작성 후 4주·8주 시점에 GSC '검색 실적'에서 페이지별 CTR 변화를 비교했습니다. 자동 추출로 대체된 페이지는 별도 시트로 관리해 본문도 함께 손봤습니다.",
                comment="\"메타는 자동으로 두면 된다\"는 가정이 가장 빈번한 손실 원인입니다. 자동 추출은 통제 불가능하고 클릭 후크가 없습니다.",
                insight="title의 클릭 후크 한 단어(예: '체크리스트', '가이드', '비교')만 추가해도 CTR이 회복된 사례가 많았습니다. 모든 페이지에 후크 1개씩은 필요합니다.",
                checklist=["페이지마다 title·description이 수동 작성됐는지", "title 50~60자, description 120~155자 내인지", "OG title·description이 별도 작성됐는지"],
                related_service=("SEO 컨설팅", "/services/seo/"),
                related_insight=("Helpful Content System 셀프 점검", "/insights/google-seo/helpful-content-self-check/")
            ) +
            '</div></div></section>'

            # Case 7 — 내부 링크
            '<section class="section" id="design-internal-link"><div class="container">'
            '<div class="case-section-head"><span class="case-num">07</span><span class="eyebrow">INTERNAL LINKING</span><h2>내부 링크</h2><p class="lead">페이지가 많아도 본문에서 서로 연결되지 않으면 검색엔진이 사이트 전체 가치를 인식하지 못합니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="LARGE SITE",
                icon="🕸️",
                h3="고립 페이지가 많은 사이트 — 권위 흐름 설계",
                problem="페이지가 100개 넘게 있지만 본문 안에서 다른 페이지로 가는 컨텍스트 링크가 거의 없었습니다. 사이드바·자동 \"관련 글\" 위젯에만 의존했고, 일부 페이지는 사이트맵·메뉴 외에는 어디서도 링크되지 않는 고립 페이지(orphan) 상태였습니다.",
                diagnosis="고립 페이지는 검색엔진이 \"중요하지 않은 페이지\"로 판단해 색인 우선순위가 매우 낮습니다. 또한 본문 컨텍스트 링크 부재로 사이트 전체 권위 신호가 흐르지 않았습니다.",
                improvements=["본문 내 컨텍스트 링크 평균 3~5개씩 추가 (관련 글·서비스·사례)", "카테고리 허브 → 개별 글 → 서비스 페이지 흐름 설계", "고립 페이지 식별 후 본문 내 자연스러운 위치에 연결", "앵커텍스트는 정확한 타겟 키워드로 통일 (\"여기 클릭\" 금지)", "필러 글과 클러스터 글을 명확히 구분해 권위 집중"],
                results=["사이트 전체 권위 흐름 형성", "신규 페이지의 색인 속도 개선", "평균 페이지뷰 증가"],
                caveats="자동 \"관련 글\" 위젯에 의존하지 마세요. 본문 컨텍스트가 자연스러운 위치에 수동 배치가 검색엔진 신호로 더 강합니다.",
                tools=["Screaming Frog 내부링크 리포트", "Ahrefs Internal Backlinks", "GSC 링크 리포트", "고립 페이지 식별 시트"],
                verification="고립 페이지에 컨텍스트 링크 추가 후 8주 동안 페이지별 InLink 수 증가, GSC '많이 연결된 페이지' 변동, 신규 페이지 색인 속도를 함께 점검했습니다.",
                comment="\"메뉴와 푸터에서 링크하면 충분하다\"는 가정이 가장 흔합니다. 본문 안에서 자연스러운 위치에 박힌 컨텍스트 링크가 훨씬 강한 신호를 보냅니다.",
                insight="필러 글이 클러스터 글로 자연스럽게 연결되는 구조를 만들고 나서, 클러스터 글의 색인 속도가 발행 후 24~48시간으로 단축된 케이스가 있었습니다.",
                checklist=["InLink 0인 고립 페이지가 있는지", "본문 안 컨텍스트 링크가 페이지당 평균 3~5개인지", "앵커텍스트가 정확한 타겟 키워드인지"],
                related_service=("SEO 웹사이트 제작", "/services/web-design/"),
                related_insight=("쇼핑몰 제품 페이지 6단락 구조", "/insights/content-seo/product-page-content-structure/")
            ) +
            '</div></div></section>'

            # Case 8 — 문의 전환 구조
            '<section class="section section-soft" id="conversion-structure"><div class="container">'
            '<div class="case-section-head"><span class="case-num">08</span><span class="eyebrow">CONVERSION STRUCTURE</span><h2>문의 전환 구조</h2><p class="lead">SEO로 트래픽이 회복돼도 문의·전환으로 이어지지 않으면 비즈니스 가치는 절반입니다. 사이트 제작 단계에서 전환 동선이 함께 설계되어야 합니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="LEAD GEN",
                icon="💬",
                h3="트래픽은 오는데 문의가 없는 사이트 — CTA 동선 재설계",
                problem="SEO 작업 후 검색 유입은 회복됐는데 문의·신청 수가 거의 변하지 않는 상태. 페이지에 도착해도 다음 행동(CTA)이 명확하지 않거나, 폼이 복잡해서 결정 마비가 발생하는 패턴이었습니다.",
                diagnosis="페이지마다 \"다음 행동\"이 명확하지 않거나 푸터에만 있는 케이스. 폼 항목이 너무 많아서 입력 부담이 크고, 신뢰 신호(실적·후기·법적 정보)가 부족해 마지막 결정이 막히는 구조였습니다.",
                improvements=["모든 핵심 페이지에 명확한 CTA 배치 (상단·중간·하단 3구간)", "폼 항목 최소화 (이름·이메일·문의 내용 3개로 시작)", "복수 채널 제공 (폼 외에 텔레그램·이메일 등)", "신뢰 신호 강화 (실적·후기·인증·법적 정보·사업자등록번호)", "마이크로 컨버전 추가 (무료 진단·체크리스트 다운로드 등 진입 장벽 낮은 행동)"],
                results=["같은 트래픽에서 문의 수 회복 추세", "재구성 작업 기간 약 3~4주"],
                caveats="CTA가 너무 공격적이거나 팝업이 과하면 이탈률이 증가합니다. 신뢰 신호와 CTA의 균형이 핵심입니다.",
                tools=["GA4 전환 이벤트", "MS Clarity 클릭·스크롤 히트맵", "Hotjar 폼 분석", "CRO 가설 트래킹 시트"],
                verification="CTA 동선 재설계 후 4주·8주 시점에 GA4 전환율, Clarity의 CTA 영역 클릭률, 폼 입력 중단 단계 데이터를 비교했습니다. 마이크로 컨버전(자료 다운로드)도 별도 KPI로 추적했습니다.",
                comment="\"트래픽이 늘면 문의는 자연스럽게 따라온다\"는 가정은 위험합니다. 페이지에 도착한 사용자가 다음 행동을 찾지 못하면 트래픽이 100배여도 문의는 그대로입니다.",
                insight="가장 빠르게 전환을 회복한 변경은 'CTA를 상단·중간·하단 3구간 배치'였습니다. 한 곳에만 CTA가 있으면 스크롤 깊이별로 결정 타이밍을 놓칩니다.",
                checklist=["페이지 상단·중간·하단에 CTA가 있는지", "폼 항목이 3~5개로 최소화됐는지", "신뢰 신호(실적·후기·법적 정보)가 페이지에 노출되는지"],
                related_service=("SEO 웹사이트 제작", "/services/web-design/"),
                related_insight=("쇼핑몰 제품 페이지 6단락 구조", "/insights/content-seo/product-page-content-structure/")
            ) +
            '</div></div></section>'

            # CTA
            '<section class="section section-cta"><div class="container cta-grid">'
            '<div><h2>지금 사이트는 어느 시나리오에 해당할까요?</h2><p>현재 사이트의 메뉴·URL·속도·전환 구조를 8가지 기준으로 진단해 우선순위를 알려드립니다. 신규 제작·리뉴얼 견적도 함께 회신드립니다.</p></div>'
            '<div class="cta-actions"><a href="https://t.me/googleseolab" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-lg">무료 사이트 진단 받기 →</a><a href="/services/web-design/" class="btn btn-outline btn-lg btn-light">SEO 웹사이트 제작 서비스</a></div>'
            '</div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"SEO 웹사이트 제작 사례","url":"https://onesearchpro.org/case-studies/web-design/","description":"메뉴·URL·속도·메타·내부 링크·전환까지 SEO 구조로 만든 사이트 8대 시나리오 작업 기록","isPartOf":{"@type":"WebSite","name":"OneSearchPro"}}</script>',
        "active": "cases",
    },

    "/case-studies/visibility/": {
        "title": "검색 노출 문제 해결 사례 | 색인·서치콘솔·샌드박스·중복·이전 | OneSearchPro",
        "desc": "구글 색인 안 됨, 서치콘솔 오류, 검색 결과 미노출, 사이트맵 무반응, 신규 도메인 샌드박스, 중복 페이지, 도메인 이전 트래픽 하락 — '왜 구글에 안 뜨지?' 의 7가지 시나리오 실제 해결 기록.",
        "keywords": "검색 노출 사례, 구글 색인 안됨, 서치콘솔 오류, 사이트맵 색인, 샌드박스, 중복 페이지, 도메인 이전 트래픽 하락",
        "h1": "검색 노출 문제 해결 사례",
        "eyebrow": "VISIBILITY FIX CASES",
        "lead": "\"왜 구글에 안 뜨지?\" — 콘텐츠는 만들고, 사이트도 잘 운영하는데 검색에 안 잡힐 때 가장 답답합니다. 이 페이지는 그 정확한 상황 7가지를 다룹니다. 각 시나리오는 \"작업 전 문제 → 진단 결과 → 개선한 항목 → 적용 후 변화 → 주의할 점\" 5단계로 정리했습니다.",
        "body": (
            # 7대 시나리오 인덱스
            '<section class="section case-index"><div class="container">'
            '<div class="section-head left"><span class="eyebrow">QUICK INDEX</span><h2>이 페이지에서 다루는 7가지 검색 노출 시나리오</h2><p>지금 사이트가 겪고 있는 상황을 골라서 바로 해당 사례로 이동하세요.</p></div>'
            '<div class="case-index-grid">'
            '<a href="#not-indexed" class="case-index-item"><span class="case-index-num">01</span><div><b>구글 색인 안 됨</b><span>"site:도메인" 검색해도 결과가 없는 사이트</span></div></a>'
            '<a href="#search-console-error" class="case-index-item"><span class="case-index-num">02</span><div><b>서치콘솔 오류</b><span>빨간 오류·경고가 다수 떠 있는데 어디부터 손댈지</span></div></a>'
            '<a href="#no-search-visibility" class="case-index-item"><span class="case-index-num">03</span><div><b>검색 결과 미노출</b><span>색인은 됐는데 어떤 키워드로도 안 나오는 사이트</span></div></a>'
            '<a href="#sitemap-no-response" class="case-index-item"><span class="case-index-num">04</span><div><b>사이트맵 제출 후 반응 없음</b><span>sitemap.xml 냈는데 색인이 진행 안 되는 사이트</span></div></a>'
            '<a href="#sandbox" class="case-index-item"><span class="case-index-num">05</span><div><b>신규 사이트 샌드박스 의심</b><span>신규 도메인이 3~6개월간 거의 무반응인 경우</span></div></a>'
            '<a href="#duplicate-pages" class="case-index-item"><span class="case-index-num">06</span><div><b>중복 페이지 문제</b><span>같은 내용이 여러 URL로 색인된 사이트의 정리</span></div></a>'
            '<a href="#domain-migration" class="case-index-item"><span class="case-index-num">07</span><div><b>도메인 이전 후 트래픽 하락</b><span>리뉴얼·도메인 변경 후 트래픽이 절반으로</span></div></a>'
            '</div></div></section>'

            # Case 1 — 구글 색인 안 됨
            '<section class="section" id="not-indexed"><div class="container">'
            '<div class="case-section-head"><span class="case-num">01</span><span class="eyebrow">NOT INDEXED</span><h2>구글 색인 안 됨</h2><p class="lead">\"site:도메인.com\" 검색해도 결과가 없거나 메인페이지만 색인되는 경우. 가장 기본 단계인 색인부터 막혀있는 상태입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="INDEXING",
                icon="🚫",
                h3="사이트가 구글에 아예 안 나오는 사이트 — 색인 단계별 진단",
                problem="\"site:도메인\" 검색해도 결과가 거의 없거나 메인페이지만 색인된 상태. 구글에 회사명·서비스명을 쳐도 검색 결과에 사이트가 나오지 않았습니다.",
                diagnosis="색인 실패는 보통 다음 중 하나로 좁혀집니다 — robots.txt 차단 규칙, 메타 robots에 잘못 박힌 noindex, canonical이 다른 URL을 가리키는 오설정, 호스팅·CDN의 봇 차단, 서버 응답 코드 오류(5xx, 잘못된 4xx).",
                improvements=["robots.txt 점검 — 불필요한 Disallow 제거, 핵심 경로 차단 해제", "모든 페이지의 메타 robots 확인 — noindex가 잘못 박힌 페이지 식별", "canonical이 자기 자신을 정확히 가리키는지 점검", "서치콘솔에 sitemap 제출 + URL 검사 도구로 색인 요청", "서버 응답 코드 점검 (정상 페이지는 200, 의도된 차단은 명확히)"],
                results=["주요 페이지 대부분 색인 정상화", "회사명·서비스명 검색에서 사이트 노출 회복", "작업 기간 약 4주"],
                caveats="색인됐다고 검색 상위 노출까지 보장되는 건 아닙니다. 색인은 \"검색에 잡힐 자격\"을 얻는 단계이고, 실제 노출은 콘텐츠·외부 신호 작업이 추가로 필요합니다.",
                tools=["GSC URL 검사", "robots.txt 테스터", "Screaming Frog", "서버 로그 분석"],
                verification="색인 차단 원인 제거 후 핵심 페이지를 GSC URL 검사로 색인 요청하고, 4주 동안 색인 적용 범위 리포트에서 '색인 생성됨' 페이지 수가 증가하는지 추적했습니다.",
                comment="\"사이트가 구글에 안 뜬다\"는 상담의 8할은 robots.txt 또는 메타 noindex 1줄이 원인입니다. 가장 먼저 점검할 곳이 가장 자주 누락됩니다.",
                insight="개발 환경에서 noindex로 막아둔 채로 라이브에 배포된 사이트가 의외로 많습니다. 라이브 배포 직후 noindex 점검은 체크리스트에 고정 항목으로 두는 게 안전합니다.",
                checklist=["robots.txt가 핵심 경로를 차단하지 않는지", "메타 robots에 noindex가 잘못 박힌 페이지가 있는지", "canonical이 자기 자신을 정확히 가리키는지"],
                related_service=("기술 SEO 진단", "/services/technical-seo/"),
                related_insight=("'발견됨 - 색인되지 않음' 7가지 원인", "/insights/technical-seo/discovered-not-indexed/")
            ) +
            '</div></div></section>'

            # Case 2 — 서치콘솔 오류
            '<section class="section section-soft" id="search-console-error"><div class="container">'
            '<div class="case-section-head"><span class="case-num">02</span><span class="eyebrow">SEARCH CONSOLE ERROR</span><h2>서치콘솔 오류</h2><p class="lead">빨간 오류·경고가 화면 가득 떠 있는데 무엇부터 손대야 할지 모르겠는 경우. 모든 오류를 한 번에 잡으려 하면 시간만 낭비됩니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="DIAGNOSIS",
                icon="⚠️",
                h3="서치콘솔에 빨간 오류·경고가 계속 뜨는 사이트 — 분류 후 우선순위",
                problem="서치콘솔 \"페이지 색인 생성\" 리포트에 빨간 오류와 노란 경고가 수십~수백 개. \"리디렉션 오류\", \"발견됨 - 색인되지 않음\", \"noindex 태그에 의해 제외됨\", \"4xx (요청을 처리할 수 없음)\" 등 다양한 메시지가 섞여있었습니다.",
                diagnosis="서치콘솔 오류는 종류별로 영향이 다릅니다. 일부는 의도된 동작(예: 관리자 페이지의 noindex, 검색용 차단)이고 일부는 진짜 문제(404, 5xx, 색인 실패). 모든 오류를 0으로 만들 필요는 없습니다.",
                improvements=["오류를 3분류 — ① 진짜 문제 (5xx 서버 오류, 의도하지 않은 4xx, 색인 실패), ② 의도된 동작 (관리자 noindex, 카테고리 필터 차단), ③ 무시 가능 (오래된 외부 링크의 404 등)", "우선순위 1: 5xx 서버 오류 (즉시), 핵심 페이지의 4xx (1주 내), 핵심 페이지 색인 누락 (2주 내)", "우선순위 2: 중복 콘텐츠, canonical 미일치, 모바일 사용성", "우선순위 3: 비핵심 페이지의 \"발견됨/색인 안 됨\""],
                results=["오류 페이지 수 정상 수준으로 회복", "핵심 페이지 색인 비율 회복", "작업 기간 약 6주"],
                caveats="\"오류 0\"이 목표가 아닙니다. 의도된 동작은 그대로 두고, 진짜 문제만 우선순위로 해결하는 게 효율적입니다.",
                tools=["GSC 페이지 색인 생성 리포트", "Screaming Frog 응답 코드 점검", "서버 로그 분석", "오류 분류 시트"],
                verification="오류를 3분류한 뒤 우선순위 1·2 항목을 6주 동안 단계적으로 해결하면서 GSC '페이지 색인 생성'에서 오류 페이지 수가 감소하는 추이를 매주 모니터링했습니다.",
                comment="\"빨간 오류 0개 만들기\"는 잘못된 목표입니다. 관리자 페이지의 noindex 같은 의도된 차단까지 잡으려 들면 정말 중요한 문제를 놓칩니다.",
                insight="실제로 문제가 되는 오류는 보통 전체의 10~20%였습니다. 분류 시트 한 장만 만들어도 작업 효율이 크게 개선됩니다.",
                checklist=["오류가 ① 진짜 문제 ② 의도된 동작 ③ 무시 가능 3분류로 정리됐는지", "5xx 서버 오류가 즉시 해결됐는지", "핵심 페이지의 4xx·색인 실패가 우선순위 상단에 있는지"],
                related_service=("기술 SEO 진단", "/services/technical-seo/"),
                related_insight=("'크롤링됨 - 색인되지 않음' 대응법", "/insights/visibility/crawled-not-indexed/")
            ) +
            '</div></div></section>'

            # Case 3 — 검색 결과 미노출
            '<section class="section" id="no-search-visibility"><div class="container">'
            '<div class="case-section-head"><span class="case-num">03</span><span class="eyebrow">NO SEARCH VISIBILITY</span><h2>검색 결과 미노출</h2><p class="lead">색인은 분명히 됐는데 어떤 키워드로 검색해도 우리 사이트가 결과에 보이지 않는 경우. 색인과 노출은 다른 단계의 신호입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="VISIBILITY",
                icon="🔍",
                h3="색인은 됐는데 검색 결과에 안 보이는 사이트 — 노출 단서 진단",
                problem="서치콘솔에서는 페이지가 \"색인됨\" 상태로 표시되는데, 정작 어떤 키워드로 구글에 검색해도 우리 사이트가 결과에 나오지 않았습니다. 단순 색인과 실제 노출은 다른 문제입니다.",
                diagnosis="색인 ≠ 노출. 색인은 \"검색 후보 풀에 들어간 것\"이고, 노출은 \"실제 검색 결과 페이지에 표시되는 것\"입니다. 페이지가 색인됐어도 검색엔진이 \"이 페이지를 어떤 키워드에 노출할까\" 판단할 신호가 부족하거나, 품질·신뢰 임계 이하면 노출에서 제외됩니다.",
                improvements=["서치콘솔 \"성능\" 리포트에서 페이지가 어떤 쿼리에라도 노출됐는지 확인 (노출 0이면 신호 부재)", "노출 0인 페이지는 본문·메타·내부 링크·H 태그·구조화 데이터 신호 보강", "매우 경쟁 심한 키워드는 자연스럽게 노출 형성에 3~6개월 소요됨을 인지", "E-E-A-T 신호 점검 (저자·갱신성·출처·실적)", "롱테일 키워드부터 진입 시도 (경쟁 낮은 키워드로 신호 누적)"],
                results=["페이지가 어떤 키워드에서든 노출 시작 → 점진 확장", "롱테일 키워드 우선 진입 후 메인 키워드로 확장", "작업 기간 약 3~5개월"],
                caveats="신규 도메인은 색인됐어도 노출까지 4~8주 걸리는 게 흔합니다. 노출 0이라고 즉시 \"문제\"는 아닙니다.",
                tools=["GSC 검색 실적", "Ahrefs Keyword Explorer", "롱테일 키워드 시트", "Schema Validator"],
                verification="롱테일 키워드 우선 작업 후 12주 동안 GSC '검색 실적' 의 노출 키워드 수, 평균 게재순위 변화, 첫 노출 발생까지의 시간을 추적했습니다.",
                comment="\"색인은 됐다\"는 말은 시작점이지 끝점이 아닙니다. 노출은 별도의 신호 임계점을 넘어야 발생합니다.",
                insight="롱테일 키워드(검색량은 작지만 의도가 뚜렷한 키워드)에서 먼저 노출이 잡히고, 그 신호가 메인 키워드로 점진 확장되는 패턴이 가장 안정적이었습니다.",
                checklist=["페이지가 어떤 키워드에서든 노출 1회 이상 발생했는지", "본문·메타·H 태그·내부 링크가 키워드 신호를 보내는지", "E-E-A-T 신호가 누적되고 있는지"],
                related_service=("SEO 컨설팅", "/services/seo/"),
                related_insight=("Helpful Content System 셀프 점검", "/insights/google-seo/helpful-content-self-check/")
            ) +
            '</div></div></section>'

            # Case 4 — 사이트맵 제출 후 반응 없음
            '<section class="section section-soft" id="sitemap-no-response"><div class="container">'
            '<div class="case-section-head"><span class="case-num">04</span><span class="eyebrow">SITEMAP NOT PICKED UP</span><h2>사이트맵 제출 후 반응 없음</h2><p class="lead">서치콘솔에 sitemap.xml을 제출했는데 색인 페이지 수가 늘지 않고 \"제출됨 - 색인되지 않음\" 으로 정체된 경우.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="SITEMAP",
                icon="🗺️",
                h3="sitemap.xml 제출 후 반응 없는 사이트 — sitemap·크롤링 진단",
                problem="서치콘솔에 sitemap.xml을 제출하고 2~3주가 지났는데 색인 페이지 수가 증가하지 않음. \"제출됨 - 색인되지 않음\" 상태로 정체되어 있었습니다.",
                diagnosis="sitemap이 제대로 처리되지 않는 원인은 보통 4가지 — ① sitemap XML 형식 오류(인코딩·XML 구문), ② sitemap 내 URL이 robots.txt에 차단됨, ③ 사이트 권위가 낮아 크롤링 예산이 작음, ④ sitemap 내 URL 다수가 중복·자동 생성 노이즈.",
                improvements=["sitemap XML 형식 검증 (XML Sitemap Validator 같은 도구로)", "sitemap 내 URL이 robots.txt에 차단되지 않는지 모든 URL 점검", "자동 생성 sitemap을 \"수동 큐레이션\"으로 전환 — 노이즈 URL 제거, 정말 색인 시키고 싶은 URL만 포함", "큰 사이트는 sitemap을 카테고리별로 분리 + sitemap 인덱스 사용", "서치콘솔 URL 검사 → 핵심 페이지 색인 요청으로 수동 트리거"],
                results=["sitemap 처리 속도 개선", "색인된 URL 수 점진 증가", "작업 기간 약 4~6주"],
                caveats="sitemap이 모든 페이지의 색인을 보장하지 않습니다. sitemap은 \"이 URL들을 우선 봐달라\"는 요청 신호일 뿐, 색인 결정은 구글이 합니다.",
                tools=["XML Sitemap Validator", "GSC 사이트맵 리포트", "Screaming Frog Sitemap 생성", "수동 큐레이션 시트"],
                verification="sitemap 형식·URL 차단·중복 점검 후 재제출하고 6주 동안 GSC 사이트맵 리포트의 '검색됨' vs '색인 생성됨' URL 수 추이를 비교했습니다.",
                comment="자동 sitemap 플러그인이 만든 sitemap에는 의외로 노이즈 URL이 많이 섞여 들어갑니다. 사이트 규모에 맞춰 수동 큐레이션이 필요합니다.",
                insight="sitemap 내 URL을 정말 색인하고 싶은 URL로만 줄였더니, sitemap 제출 후 7~10일 안에 색인 적용 속도가 눈에 띄게 빨라졌습니다.",
                checklist=["sitemap이 XML 형식 검증을 통과하는지", "sitemap 내 URL이 robots.txt에 차단되지 않는지", "sitemap에 노이즈·중복 URL이 섞이지 않았는지"],
                related_service=("기술 SEO 진단", "/services/technical-seo/"),
                related_insight=("'발견됨 - 색인되지 않음' 7가지 원인", "/insights/technical-seo/discovered-not-indexed/")
            ) +
            '</div></div></section>'

            # Case 5 — 신규 사이트 샌드박스
            '<section class="section" id="sandbox"><div class="container">'
            '<div class="case-section-head"><span class="case-num">05</span><span class="eyebrow">NEW DOMAIN SANDBOX</span><h2>신규 사이트 샌드박스 의심</h2><p class="lead">신규 도메인 사이트가 런칭 후 3~6개월이 지나도 검색 트래픽이 매우 적은 경우. 흔히 \"구글 샌드박스\" 로 의심하지만 실체는 \"도메인 신뢰 누적 시간\" 입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="NEW DOMAIN",
                icon="🏝️",
                h3="신규 도메인이 몇 개월간 거의 무반응인 사이트 — 권위 누적 가속",
                problem="신규 도메인으로 사이트를 런칭한 후 3~6개월이 지나도 검색 트래픽이 매우 적었습니다. 색인은 되지만 어떤 키워드로도 거의 잡히지 않아 \"구글 샌드박스\" 현상으로 의심되는 패턴이었습니다.",
                diagnosis="구글이 공식적으로 \"샌드박스\"를 인정하진 않지만, 신규 도메인의 신뢰 형성에 시간이 걸리는 건 명확합니다. 도메인 권위·외부 신호·콘텐츠 누적이 임계점에 도달해야 검색이 활성화됩니다. 단기간 백링크 대량 발주 같은 무리한 신호는 오히려 의심 신호로 작용합니다.",
                improvements=["첫 6개월은 콘텐츠 발행·내부 구조에 집중 (외부 신호 무리하게 추구 X)", "주 1~2편 정기 콘텐츠로 \"활성 사이트\" 신호 누적", "안전한 외부 신호 확보 (보도자료·디지털 PR 기반의 자연 언급)", "코어 키워드보다 롱테일 키워드 우선 진입 (경쟁 낮은 키워드부터)", "인내 — 도메인 권위 누적은 절대 시간 필요"],
                results=["6~9개월차부터 키워드 노출 점진 회복", "롱테일 키워드부터 진입 시작", "안정 노출까지 9~12개월"],
                caveats="신규 도메인에 단기간 백링크 대량 발주는 의심 신호로 작용합니다. 자연 누적이 정답이며, 무리한 가속은 오히려 회복 시간을 늘립니다.",
                tools=["GSC 검색 실적(주간 추적)", "Ahrefs Domain Rating", "콘텐츠 발행 캘린더", "Whois 도메인 이력 점검"],
                verification="첫 6개월은 콘텐츠 발행 캘린더에 맞춰 진행하고, 7개월차부터 GSC 노출·평균 게재순위·DR 변화를 월간 단위로 비교했습니다. 외부 신호도 자연 누적 페이스를 점검했습니다.",
                comment="\"3개월 안에 검색 1등\" 같은 약속은 위험 신호입니다. 신규 도메인은 시간을 단축할 수 없고, 무리한 가속은 패널티 위험만 키웁니다.",
                insight="첫 6개월간 주 1~2편의 정기 콘텐츠 발행이 '활성 사이트' 신호로 누적되어, 7개월차부터 노출 회복 속도가 가팔라지는 패턴이 일관되게 관찰되었습니다.",
                checklist=["주 1~2편 정기 콘텐츠 발행 캘린더가 있는지", "단기간 백링크 대량 발주를 피하고 있는지", "롱테일 키워드 우선 전략이 적용됐는지"],
                related_service=("SEO 컨설팅", "/services/seo/"),
                related_insight=("구글 SEO 첫 달 우선 작업 5가지", "/insights/google-seo/first-month-priorities/")
            ) +
            '</div></div></section>'

            # Case 6 — 중복 페이지 문제
            '<section class="section section-soft" id="duplicate-pages"><div class="container">'
            '<div class="case-section-head"><span class="case-num">06</span><span class="eyebrow">DUPLICATE CONTENT</span><h2>중복 페이지 문제</h2><p class="lead">같은 내용이 여러 URL로 색인된 사이트는 어느 페이지도 1위가 되지 못합니다. 옵션·필터·정렬·페이지네이션이 중복 URL의 주범입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="DUPLICATE",
                icon="🧩",
                h3="같은 내용이 여러 URL로 색인된 사이트 — canonical·통합 정리",
                problem="제품·콘텐츠 페이지가 옵션·필터·정렬·페이지네이션에 따라 수많은 중복 URL로 색인. 본문은 거의 같은데 URL만 다른 페이지가 수천 개. 서치콘솔에 \"중복, 사용자가 선택한 표준 URL 없음\" 메시지가 다수 발생한 상태였습니다.",
                diagnosis="중복 콘텐츠는 구글이 \"어느 페이지가 메인인지\" 판단하지 못해 노출 우선순위가 하락합니다. 또한 크롤링 예산을 낭비해서 정말 색인되어야 할 핵심 페이지의 색인까지 지연됩니다.",
                improvements=["중복 페이지 식별 (서치콘솔 + site: 검색 + 본문 첫 50자 따옴표 검색)", "옵션·필터·정렬 URL은 메인 페이지를 canonical로 지정", "페이지네이션은 rel=next/prev 대신 canonical 메인 + noindex 조합", "본문 90% 이상 같은 페이지는 통합 후 301", "sitemap에서 중복 URL 모두 제거, 핵심 URL만 포함"],
                results=["크롤링 통계상 핵심 페이지 방문 증가", "중복 색인 페이지 점진 감소", "핵심 페이지 노출 회복", "작업 기간 약 3개월"],
                caveats="대규모 중복 정리는 단기 트래픽 변동이 발생할 수 있습니다. 작업 전 영향 분석과 분기 단위 추적이 필요합니다.",
                tools=["GSC 색인 적용 범위", "Screaming Frog 중복 콘텐츠 점검", "Siteliner", "canonical 매핑 시트"],
                verification="중복 정리 후 GSC '색인 적용 범위'의 '중복, 사용자가 선택한 표준 URL 없음' 페이지 수 감소, '크롤링 통계'의 핵심 페이지 방문 빈도, 핵심 URL의 평균 게재순위를 12주 동안 추적했습니다.",
                comment="옵션·필터·페이지네이션 URL은 가장 흔한 중복 발생원입니다. canonical 한 줄로 막을 수 있는 케이스가 의외로 많이 방치됩니다.",
                insight="중복 URL을 정리하자 크롤링 통계상 핵심 페이지 방문 빈도가 자연스럽게 늘었습니다. 크롤링 예산 회복이 색인·노출 회복으로 연결되는 패턴이 명확했습니다.",
                checklist=["옵션·필터·정렬 URL이 canonical로 정리됐는지", "본문 90% 이상 같은 페이지가 통합·301되었는지", "sitemap에 중복 URL이 섞여 들어가지 않는지"],
                related_service=("기술 SEO 진단", "/services/technical-seo/"),
                related_insight=("'크롤링됨 - 색인되지 않음' 대응법", "/insights/visibility/crawled-not-indexed/")
            ) +
            '</div></div></section>'

            # Case 7 — 도메인 이전 트래픽 하락
            '<section class="section" id="domain-migration"><div class="container">'
            '<div class="case-section-head"><span class="case-num">07</span><span class="eyebrow">DOMAIN MIGRATION</span><h2>기존 도메인 이전 후 트래픽 하락</h2><p class="lead">도메인을 바꿨거나 URL 구조를 리뉴얼한 후 트래픽이 절반 이상 빠진 경우. 90% 케이스는 301 매핑 누락이 원인입니다.</p></div>'
            '<div class="grid services case-grid">' +
            case_card(
                badge="MIGRATION",
                icon="📦",
                h3="도메인·URL 변경 후 트래픽이 절반으로 — 마이그레이션 복구",
                problem="기존 사이트의 도메인을 변경하거나 URL 구조를 리뉴얼한 후 검색 트래픽이 50% 이상 감소. 회복 기미 없이 몇 주가 지난 상태로 상담이 시작되었습니다.",
                diagnosis="마이그레이션 후 트래픽 손실의 90%는 301 리다이렉트 매핑 누락에서 발생합니다. 옛 URL이 새 URL로 정확히 연결되지 않으면 외부 백링크·기존 색인 신호가 모두 끊깁니다. 또한 도메인 변경 시 서치콘솔의 \"주소 변경 도구\"를 사용하지 않은 경우도 흔합니다.",
                improvements=["기존 URL ↔ 새 URL 1:1 매핑 시트 작성, 누락 점검", "모든 옛 URL에 301 리다이렉트 적용 (http/https/www/non-www/대소문자/슬래시 변형 포함)", "서치콘솔 \"주소 변경 도구\"로 도메인 이전 명시 (도메인 자체가 바뀐 경우)", "새 도메인의 sitemap 제출 + 핵심 URL 색인 재요청", "외부 백링크가 가리키는 옛 URL이 살아있는지(301 작동) 점검", "외부 백링크 일부는 새 URL로 업데이트 요청"],
                results=["트래픽 점진 회복 (보통 4~12주)", "핵심 키워드 순위 대부분 유지", "작업 기간 약 6~10주"],
                caveats="마이그레이션 트래픽 손실은 즉시 회복되지 않습니다. 사전 계획이 핵심이고 사후 복구는 시간이 오래 걸립니다. 도메인 이전을 계획 중이라면 출시 전 SEO 컨설팅이 비용 대비 가장 효율적입니다.",
                tools=["GSC 주소 변경 도구", "Screaming Frog 301 점검", "1:1 URL 매핑 시트", "Ahrefs Backlinks(외부 백링크)"],
                verification="301 매핑 적용 후 4주·8주·12주 시점에 GSC '검색 실적' 의 클릭·노출, '페이지 색인 생성'의 404 추이, 외부 백링크가 가리키는 옛 URL이 정상 301되는지 점검했습니다.",
                comment="\"옛 URL은 자연스럽게 사라진다\"는 가정이 가장 위험합니다. 1:1 301 없이 진행한 마이그레이션은 백링크·기존 색인 신호를 모두 잃습니다.",
                insight="외부 백링크 상위 30개에 대해 새 URL로 업데이트를 직접 요청한 것이 회복 속도를 가장 크게 단축시킨 작업이었습니다. 301만으로는 권위 신호의 일부가 새고 있습니다.",
                checklist=["옛 URL ↔ 새 URL 1:1 매핑 시트가 완성됐는지", "서치콘솔 '주소 변경 도구'가 적용됐는지", "주요 외부 백링크가 새 URL로 업데이트 요청됐는지"],
                related_service=("기술 SEO 진단", "/services/technical-seo/"),
                related_insight=("301 리다이렉트 자주 빠뜨리는 12가지", "/insights/visibility/301-migration-mistakes/")
            ) +
            '</div></div></section>'

            # CTA (전환 강조)
            '<section class="section section-cta"><div class="container cta-grid">'
            '<div><h2>지금 \"왜 안 뜨지?\" 라고 느끼신다면</h2><p>위 7가지 시나리오 중 하나에 거의 확실히 해당합니다. 어떤 상황인지, 어디서부터 손대야 하는지 24시간 내 분석 리포트를 텔레그램으로 회신드립니다. 진단 자체는 무료이고 계약 의무는 없습니다.</p></div>'
            '<div class="cta-actions"><a href="https://t.me/googleseolab" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-lg">지금 무료 진단 받기 →</a><a href="/services/technical-seo/" class="btn btn-outline btn-lg btn-light">기술 SEO 진단 서비스</a></div>'
            '</div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"검색 노출 문제 해결 사례","url":"https://onesearchpro.org/case-studies/visibility/","description":"구글 색인·서치콘솔·사이트맵·샌드박스·중복·도메인 이전 7대 시나리오 검색 노출 문제 해결 작업 기록","isPartOf":{"@type":"WebSite","name":"OneSearchPro"}}</script>',
        "active": "cases",
    },

    # ========== Insights subpages ==========
    "/insights/google-seo/": {
        "title": "구글 SEO 가이드 | E-E-A-T·알고리즘 | OneSearchPro",
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
        "title": "기술 SEO 가이드 | 색인·CWV | OneSearchPro",
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
        "title": "콘텐츠 SEO 가이드 | 키워드·토픽 권위 | OneSearchPro",
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
        "title": "지역 SEO 가이드 | GBP·네이버 플레이스 | OneSearchPro",
        "desc": "지역 SEO 실무 가이드. 구글 비즈니스 프로필 최적화, 네이버 플레이스 운영, 지역 랜딩페이지 설계, NAP 일관성 등 지역 기반 검색 유입 가이드 모음.",
        "keywords": "지역 SEO 가이드, 구글 비즈니스 프로필, 네이버 플레이스, 지역 랜딩페이지, NAP 일관성, 로컬 SEO",
        "h1": "지역 SEO",
        "eyebrow": "LOCAL SEO GUIDES",
        "lead": "구글 비즈니스 프로필·네이버 플레이스·지역 랜딩페이지·NAP 일관성을 다루는 지역 SEO 실무 가이드입니다.",
        "body": (
            '<section class="section"><div class="container"><div class="grid services">' +
            insight_article_card(
                "네이버 플레이스 부정 리뷰 대응 — 자주 하는 실수 5가지",
                "부정 리뷰는 제거 대상이 아니라 응답 대상. 사장님들이 자주 빠지는 5가지 실수와 신뢰를 유지하는 4단계 응답 프로세스.",
                "/insights/local-seo/negative-review-response-mistakes/",
                8
            ) +
            insight_article_card(
                "신규 매장 네이버 플레이스 등록 첫 4주 운영 가이드",
                "리뷰 없는 신규 매장이 빠지는 함정과, 정보·블로그·리뷰 우선순위로 짠 월별 운영 매뉴얼.",
                "/insights/local-seo/new-store-naver-place/",
                7
            ) +
            insight_article_card(
                "다지점 매장 GBP 본사·지점 분리 원칙",
                "본사 정보를 모든 지점에 복붙하면 안 되는 이유. 위치·카테고리·사진·리뷰 응대 4가지 분리 원칙.",
                "/insights/local-seo/multi-location-gbp/",
                7
            ) +
            insight_card("\"지역명 + 서비스\" 키워드용 지역 랜딩페이지 설계법", "다지점 비즈니스에서 지역 키워드를 잡기 위한 페이지 구조와 콘텐츠 작성 가이드.") +
            insight_card("NAP 일관성과 로컬 인용(citation)이 왜 중요한가", "디렉토리·SNS·자체 사이트의 상호·주소·전화 정보 통일 가이드.") +
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"지역 SEO","url":"https://onesearchpro.org/insights/local-seo/","isPartOf":{"@type":"Blog","name":"SEO 인사이트"}}</script>',
        "active": "insights",
    },

    "/insights/backlink-pr/": {
        "title": "백링크·디지털 PR 가이드 | OneSearchPro",
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
        "title": "SNS 마케팅 가이드 | 인스타·유튜브 | OneSearchPro",
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
        "title": "검색 노출 문제 해결 가이드 | OneSearchPro",
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

    "/about/team/": {
        "title": "팀 · 저자 소개 | OneSearchPro 운영자와 SEO 전문가",
        "desc": "OneSearchPro를 운영하고 SEO 인사이트를 직접 집필하는 책임 저자와 팀을 소개합니다. 누가 어떤 경험으로 콘텐츠를 만드는지(E-E-A-T) 투명하게 공개합니다.",
        "keywords": "OneSearchPro 팀, 강백호, SEO 컨설턴트, SEO 전문가, 저자 소개, About Author, E-E-A-T",
        "h1": "팀 · 저자 소개",
        "eyebrow": "OUR TEAM & AUTHORS",
        "lead": "콘텐츠의 신뢰는 결국 \"누가 썼는가\"에서 시작됩니다. OneSearchPro의 SEO 인사이트와 컨설팅을 책임지는 팀을 공개합니다. 글에 적용된 경험·관점이 어디서 나왔는지 직접 확인하실 수 있도록 했습니다.",
        "body": (
            '<section class="section"><div class="container">'
            '<div class="section-head left"><span class="eyebrow">LEAD AUTHOR</span><h2>책임 저자 — 강백호</h2><p>OneSearchPro(YH기획) 운영자이자 SEO 인사이트 글 대부분을 직접 집필하는 책임 저자입니다.</p></div>'
            '<div class="legal-doc">'
            '<h3>경력 요약</h3>'
            '<ul>'
            '<li>SEO·디지털 마케팅 실무 10년+ — 리테일·F&amp;B·뷰티·핀테크·교육·의료 등 다양한 산업의 SEO 프로젝트 수행</li>'
            '<li>OneSearchPro(YH기획) 대표 · SEO 컨설팅 총괄</li>'
            '<li>구글 검색 가이드라인·네이버 검색 정책을 동시 대응하는 한국형 SEO 워크플로우 구축</li>'
            '<li>1,200건+ 화이트햇 백링크 빌딩, 페널티 사례 0건 유지</li>'
            '</ul>'
            '<h3>주로 다루는 주제</h3>'
            '<ul>'
            '<li>구글 코어 업데이트·Helpful Content System 실무 대응</li>'
            '<li>기술 SEO (색인, Core Web Vitals, 구조화 데이터, sitemap·robots 설계)</li>'
            '<li>콘텐츠 SEO (검색 의도, 토픽 클러스터, 의료·금융 등 YMYL 콘텐츠 가이드)</li>'
            '<li>지역 SEO (네이버 플레이스·구글 비즈니스 프로필 운영)</li>'
            '<li>디지털 PR·백링크 진단·disavow 판단</li>'
            '</ul>'
            '<h3>집필 원칙</h3>'
            '<p>OneSearchPro의 모든 인사이트 글은 다음 기준을 지킵니다.</p>'
            '<ul>'
            '<li><b>실무 경험 기반</b> — 검증되지 않은 인터넷 정보의 단순 재정리는 발행하지 않습니다.</li>'
            '<li><b>한국 시장 맥락 반영</b> — 네이버 C-랭크·DIA, 의료광고심의, 한국 광고 정책 등 현지 특성을 반영합니다.</li>'
            '<li><b>관찰형 표현</b> — \"보장\", \"100%\", \"반드시 1위\" 같은 단정·과장 표현 대신 \"자주 보이는 패턴\", \"실무 관찰상\" 같은 정직한 표현을 씁니다.</li>'
            '<li><b>출처 명시</b> — 구글 공식 가이드라인·서치콘솔 도움말·1차 자료를 우선 인용합니다.</li>'
            '<li><b>AI 보조 시 인간 검수</b> — 초안 작성에 AI를 보조 도구로 사용하더라도 모든 글은 책임 저자가 사실관계·논리·문장을 직접 검수한 뒤 발행합니다.</li>'
            '</ul>'
            '<h3>외부 프로필 · 콘텐츠</h3>'
            '<ul>'
            '<li>LinkedIn: <a href="https://www.linkedin.com/in/%EB%B0%B1%ED%98%B8-%EA%B0%95-a84273261/" target="_blank" rel="noopener noreferrer me">강백호 · OneSearchPro</a></li>'
            '<li>Medium: <a href="https://medium.com/@88smartbro88" target="_blank" rel="noopener noreferrer me">@88smartbro88</a></li>'
            '<li>X (Twitter): <a href="https://x.com/gugeulmake84173" target="_blank" rel="noopener noreferrer me">@gugeulmake84173</a></li>'
            '<li>Telegram (문의): <a href="https://t.me/googleseolab" target="_blank" rel="noopener noreferrer me">@googleseolab</a></li>'
            '</ul>'
            '<h3>연락처</h3>'
            '<p>저자에게 직접 글·사실관계에 대한 의견을 보내시려면 <a href="mailto:contact@onesearchpro.com">contact@onesearchpro.com</a> 으로 메일을 보내주세요. 모든 인사이트 글의 사실 오류 신고는 24시간 내 검토 후 수정·반영합니다.</p>'
            '</div></div></section>'
            + section("EDITORIAL", "콘텐츠 검수 프로세스",
                "모든 인사이트 글은 발행 전 다음 4단계 검수를 거칩니다.",
                [
                    {"icon":"📝","h":"1. 초안 작성","p":"책임 저자가 주제를 선정하고 실무 경험과 1차 자료를 토대로 초안을 작성합니다.","li":["주제는 발행 캘린더로 사전 계획","경쟁 SERP·검색 의도 사전 분석"]},
                    {"icon":"🔍","h":"2. 사실관계 검토","p":"구글·네이버 공식 가이드라인, 도구 공식 문서 등 1차 자료와 대조해 사실 오류를 점검합니다.","li":["공식 문서 인용 추적","수치·날짜 재확인"]},
                    {"icon":"⚖️","h":"3. 표현·정책 검수","p":"단정·과장 표현, 검증 불가능한 수치, 광고법 위반 가능 표현을 정비합니다.","li":["\\\"보장·100%·반드시\\\" 표현 제거","의료·금융 등 YMYL 규제 확인"]},
                    {"icon":"🚀","h":"4. 발행 후 관찰","p":"발행 후 댓글·문의·실측 트래픽 데이터를 토대로 사실 오류·노후화 항목을 분기 단위로 업데이트합니다.","li":["분기별 글 리프레시","독자 피드백 반영"]},
                ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"ProfilePage","mainEntity":{"@type":"Person","name":"강백호","alternateName":"Hobaek Kang","url":"https://onesearchpro.org/about/team/","jobTitle":"SEO 컨설턴트 · OneSearchPro 대표","worksFor":{"@type":"Organization","name":"OneSearchPro","legalName":"YH기획","url":"https://onesearchpro.org/"},"knowsAbout":["Search Engine Optimization","Technical SEO","Content SEO","Local SEO","Digital PR","구글 SEO","네이버 SEO","Helpful Content System","Core Web Vitals"],"sameAs":["https://www.linkedin.com/in/%EB%B0%B1%ED%98%B8-%EA%B0%95-a84273261/","https://medium.com/@88smartbro88","https://x.com/gugeulmake84173","https://t.me/googleseolab"]}}</script>',
        "active": "about",
    },

    # ===================== BLOG ARTICLES =====================
    # Google SEO category
    "/insights/google-seo/post-core-update-mistakes/": {
        "title": "코어 업데이트 직후 SEO 주의사항 5가지 | OneSearchPro",
        "desc": "코어 업데이트 발표 후 트래픽이 흔들릴 때 가장 위험한 건 패닉 작업입니다. 첫 2주간 손대지 말아야 할 5가지와 그 이유, 그리고 대신 무엇을 해야 하는지 정리합니다.",
        "keywords": "구글 코어 업데이트, core update, 트래픽 급락, SEO 패닉, 코어 업데이트 대응",
        "h1": "코어 업데이트 직후 SEO 주의사항 5가지",
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
                 "<p>이 순서를 지키면 \"무엇이 효과 있었는지\"를 측정할 수 있습니다. 측정이 가능한 것만이 다음 업데이트에도 통용되는 노하우가 됩니다.</p>"
                 "<p><b>1차 자료 참고:</b> 코어 업데이트의 \"무엇을 평가하고 무엇을 하지 말 것인가\"는 구글 검색 센터의 "
                 "<a href=\"https://developers.google.com/search/updates/core-updates\" target=\"_blank\" rel=\"noopener noreferrer\">Core updates 공식 가이드</a>에 정리되어 있습니다. 특히 \"recovery는 일반적으로 다음 코어 업데이트까지 기다려야 한다\"는 부분이 패닉 작업 자제의 근거로 활용됩니다.</p>"),
            ],
            key_takeaways=[
                "코어 업데이트는 7~14일 단계적 롤아웃이라 첫 며칠의 변동이 최종 결과가 아닙니다.",
                "패닉 작업은 진단 변수만 늘리고 측정 기준선을 무너뜨립니다.",
                "Disavow·콘텐츠 대량 수정·디자인 리뉴얼·새 도구 도입은 안정 이후로 미루세요.",
                "대신 \"4주 관찰\"이 진짜 원인을 찾는 가장 빠른 길입니다.",
            ],
            related=[
                ("Helpful Content System 셀프 점검 7가지", "/insights/google-seo/helpful-content-self-check/", "구글 SEO"),
                ("트래픽이 갑자기 떨어졌을 때 4주 진단 매뉴얼", "/insights/visibility/", "검색 노출"),
                ("SEO 컨설팅 서비스", "/services/seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/google-seo/post-core-update-mistakes/",
            title="코어 업데이트 직후 SEO 주의사항 5가지",
            desc="코어 업데이트 직후 패닉 작업이 위험한 이유와 4주 관찰 매뉴얼.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/google-seo/helpful-content-self-check/": {
        "title": "Helpful Content System 셀프 점검 7가지 | OneSearchPro",
        "desc": "구글의 Helpful Content System은 사이트 전체 평가에 영향을 줍니다. 한국 사이트가 셀프 평가에서 자주 떨어지는 7가지 질문과 통과 기준을 정리합니다.",
        "keywords": "Helpful Content System, HCS, 도움이 되는 콘텐츠, 구글 셀프 평가, 콘텐츠 품질 평가",
        "h1": "Helpful Content System 셀프 점검 7가지",
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
                 "<p>위 4가지를 정비하는 것만으로도 HCS 평가에 의미 있는 변화가 나타납니다.</p>"
                 "<p><b>1차 자료 참고:</b> 본문 셀프 평가 질문의 원문은 구글 검색 센터의 "
                 "<a href=\"https://developers.google.com/search/docs/fundamentals/creating-helpful-content\" target=\"_blank\" rel=\"noopener noreferrer\">\"Creating helpful, reliable, people-first content\"</a> 가이드에 정리되어 있습니다. 영문이지만 단락별로 \"누구를 위해\", \"무엇을 보여주는가\"를 자가 점검할 수 있도록 만들어진 표준 질문지입니다.</p>"),
            ],
            key_takeaways=[
                "HCS는 페이지가 아닌 사이트 전체 평가입니다. 가지치기가 새 글 발행보다 효과적일 때가 많습니다.",
                "\"1차 목적이 사람인가\"는 키워드를 빼고 본문이 읽히는지로 검증할 수 있습니다.",
                "저자 페이지의 자격 나열보다, 본문 안에 경험이 드러나는지가 더 중요합니다.",
                "옛 글 정리·저자 정보·출처 인용·키워드 스터핑 제거가 가장 효과적인 시작점입니다.",
            ],
            related=[
                ("코어 업데이트 직후 SEO 주의사항 5가지", "/insights/google-seo/post-core-update-mistakes/", "구글 SEO"),
                ("쇼핑몰 제품 페이지 본문 6단락 구조", "/insights/content-seo/product-page-content-structure/", "콘텐츠 SEO"),
                ("콘텐츠 SEO 서비스", "/services/content-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/google-seo/helpful-content-self-check/",
            title="Helpful Content System 셀프 점검 7가지",
            desc="구글 HCS의 셀프 평가 질문 중 한국 사이트가 가장 자주 떨어지는 패턴 분석.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/google-seo/first-month-priorities/": {
        "title": "신규 사이트 첫 1개월 SEO 우선순위 5가지 | OneSearchPro",
        "desc": "신규 도메인이 첫 한 달에 해야 할 SEO 작업을 우선순위 순으로 정리. 측정 기반·색인 확보·핵심 페이지 최적화·Core Web Vitals 기준선·첫 콘텐츠 발행까지의 실무 순서.",
        "keywords": "신규 사이트 SEO, 신규 도메인 SEO, 첫달 SEO, SEO 우선순위, 서치콘솔 셋업, SEO 처음 시작",
        "h1": "신규 사이트 첫 1개월 SEO 우선순위 5가지",
        "eyebrow": "GOOGLE SEO · ARTICLE",
        "lead": "신규 도메인의 첫 한 달은 \"무엇을 하느냐\"보다 \"어떤 순서로 하느냐\"가 6개월 결과를 좌우합니다. 욕심내서 한 번에 다 하면 변수가 섞여 측정이 불가능해집니다. 우선순위 5단계로 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            reading_time=8,
            intro="신규 사이트는 구글에게 \"아직 모르는 사이트\"입니다. 첫 한 달은 \"신뢰할 만한가\"가 판단되는 기간이고, 어떤 신호를 주느냐가 이후를 좌우합니다. 백링크 작업이나 광고 집행 같은 일은 그 다음 단계에서 의미가 생깁니다. 첫 한 달은 다음 5단계를 순서대로만 진행하세요.",
            sections=[
                ("왜 신규 사이트는 \"우선순위\"가 결정적인가",
                 "<p>많은 신규 사이트가 첫 달부터 백링크 발주, 광고 집행, 디자인 리뉴얼을 동시에 시도합니다. 의도는 좋지만 결과적으로는 변수가 너무 많이 섞입니다. 한 달 뒤 트래픽이 늘어났든 줄어들었든, 어떤 작업이 효과적이었는지 분리할 수 없게 됩니다.</p>"
                 "<p>이 시기의 진짜 목표는 \"측정 가능한 기반\"과 \"색인된 사이트\"를 만드는 것입니다. 이 두 가지가 갖춰지면 그 다음 작업의 효과를 숫자로 확인할 수 있고, 의사결정 속도가 몇 배 빨라집니다.</p>"),
                ("1순위 — 서치콘솔·GA4·태그 매니저·네이버 서치어드바이저 셋업",
                 "<p>가장 먼저 해야 할 작업이고, 가장 자주 미루는 작업입니다. 다음 4가지를 1주차 안에 설치합니다.</p>"
                 "<ul>"
                 "<li><b>Google Search Console</b> — 소유권 확인, sitemap 제출, URL 검사 가능 상태로</li>"
                 "<li><b>Google Analytics 4</b> — 이벤트 트래킹 기본 설정 (페이지뷰·스크롤·외부 링크)</li>"
                 "<li><b>Google Tag Manager</b> — 이후 추가될 도구 셋업의 허브 역할</li>"
                 "<li><b>네이버 서치어드바이저</b> — 한국 검색 대응 필수</li>"
                 "</ul>"
                 "<p>이 4가지가 갖춰지지 않으면 그 다음 모든 작업의 효과를 측정할 수 없습니다. 실무에서 보면 신규 사이트의 절반은 이걸 \"나중에\" 미루다가 한 달 데이터를 통째로 잃습니다.</p>"),
                ("2순위 — 색인 가능한 페이지 점검과 sitemap 제출",
                 "<p>사이트가 만들어졌다고 자동으로 구글에 색인되는 게 아닙니다. 다음을 점검합니다.</p>"
                 "<ul>"
                 "<li><code>robots.txt</code>가 핵심 페이지를 차단하지 않는지</li>"
                 "<li>메타 robots에 <code>noindex</code>가 잘못 걸린 페이지 없는지</li>"
                 "<li><code>canonical</code>이 자기 자신을 정확히 가리키는지</li>"
                 "<li><code>sitemap.xml</code>이 색인 대상 페이지 전부를 포함하는지</li>"
                 "<li>서치콘솔에서 sitemap 제출 → 며칠 후 \"커버리지\" 리포트로 색인 상태 확인</li>"
                 "</ul>"
                 "<p>색인 안 된 페이지는 어떤 작업을 해도 검색에 노출되지 않습니다. 1~2주차 안에 끝내야 할 작업입니다.</p>"),
                ("3순위 — 핵심 페이지 5개의 메타·H1·내부 링크 우선 최적화",
                 "<p>전체 사이트를 한 번에 다 최적화할 필요는 없습니다. 비즈니스에 가장 중요한 페이지 5개만 골라서 다음을 점검합니다.</p>"
                 "<ul>"
                 "<li><b>title 태그</b>: 50~60자, 1차 키워드 포함, 브랜드명 뒤에</li>"
                 "<li><b>meta description</b>: 120~160자, 클릭 유도 카피 + CTA 한 줄</li>"
                 "<li><b>H1</b>: 페이지당 1개, 1차 키워드가 자연스럽게</li>"
                 "<li><b>메인페이지에서 이 5개로 가는 본문 내 텍스트 링크</b></li>"
                 "<li>5개 페이지 사이의 상호 내부 링크</li>"
                 "</ul>"
                 "<p>이 5개 페이지가 검색 결과에서 우리 사이트를 대표하게 됩니다. 첫 달 안에 완성도 90%까지 끌어올리는 게 목표입니다.</p>"),
                ("4순위 — Core Web Vitals 기준선 측정과 큰 문제만 해결",
                 "<p>첫 한 달부터 Core Web Vitals 100점을 노릴 필요는 없습니다. 다음만 처리하세요.</p>"
                 "<ul>"
                 "<li>PageSpeed Insights로 핵심 페이지 5개 측정</li>"
                 "<li>LCP가 4초 넘는 페이지가 있으면 Hero 이미지 압축·WebP 변환 (효과 가장 큼)</li>"
                 "<li>CLS가 0.25 넘으면 이미지·광고 자리에 명시적 width/height 지정</li>"
                 "<li>INP·TBT는 이 단계에서 깊게 안 봐도 됨 — 트래픽 생긴 후 실측 데이터로 판단</li>"
                 "</ul>"
                 "<p>\"치명적 문제만 해결해 기준선 확보\"가 이 단계의 목표입니다. 세부 최적화는 트래픽이 생긴 후 우선순위를 다시 잡습니다.</p>"),
                ("5순위 — 첫 콘텐츠 발행 (토픽 권위의 시드)",
                 "<p>이전 4단계가 \"색인되고 측정 가능한 상태\"를 만들었다면, 5단계는 \"검색엔진이 평가할 콘텐츠\"를 처음으로 제공합니다.</p>"
                 "<ul>"
                 "<li>핵심 비즈니스 키워드와 직접 관련된 글 2~3편 발행</li>"
                 "<li>각 글 1,500자 이상, 본인 경험·관점·구체 사례 포함</li>"
                 "<li>메인페이지에서 이 글들로 내부 링크</li>"
                 "<li>BlogPosting 스키마 마크업 적용</li>"
                 "</ul>"
                 "<p>첫 콘텐츠는 양보다 \"이 사이트가 무엇을 다루는 곳인지\"를 검색엔진에 신호로 전달하는 게 목적입니다. 한 달 안에 무리하게 많이 쓸 필요 없습니다.</p>"),
                ("이 단계에서 절대 하지 말아야 할 4가지",
                 "<ol>"
                 "<li><b>첫 달 백링크 대량 발주</b> — 신규 도메인이 갑자기 외부 링크를 많이 받으면 의심 신호로 작용. 백링크는 콘텐츠 누적 후 시작.</li>"
                 "<li><b>디자인 리뉴얼·URL 구조 변경</b> — 색인이 안정되기 전에 변동을 주면 회복 시간만 늘어남.</li>"
                 "<li><b>광고 위주의 트래픽 만들기</b> — 광고를 끄면 트래픽이 0으로 돌아옵니다. SEO 기반이 먼저.</li>"
                 "<li><b>익숙하지 않은 자동화 도구 도입</b> — 첫 한 달은 수동 점검 위주로 진행. 변수를 단순하게 유지.</li>"
                 "</ol>"
                 "<p>다음 한 달의 결과는 첫 한 달의 \"기반 다지기\"가 얼마나 깨끗했느냐에 좌우됩니다. 욕심을 줄이고 순서를 지키는 게 가장 빠른 길입니다.</p>"),
            ],
            key_takeaways=[
                "첫 한 달의 핵심은 \"측정 기반 + 색인 확보\"이고, 콘텐츠와 외부 신호는 그 다음입니다.",
                "서치콘솔·GA4·sitemap이 1주차에 갖춰져야 이후 모든 작업의 효과를 측정할 수 있습니다.",
                "핵심 페이지 5개만 우선 최적화하세요. 전체 사이트는 점진적으로.",
                "백링크 대량 발주·디자인 리뉴얼·과한 자동화는 첫 한 달에는 피해야 합니다.",
            ],
            related=[
                ("코어 업데이트 직후 SEO 주의사항 5가지", "/insights/google-seo/post-core-update-mistakes/", "구글 SEO"),
                ("서치콘솔 \"발견됨 - 현재 색인되지 않음\" 7가지 원인과 진단 순서", "/insights/technical-seo/discovered-not-indexed/", "기술 SEO"),
                ("SEO 컨설팅 서비스", "/services/seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/google-seo/first-month-priorities/",
            title="신규 사이트 첫 1개월 SEO 우선순위 5가지",
            desc="신규 도메인이 첫 한 달에 해야 할 SEO 작업의 우선순위 5단계.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    # Technical SEO category
    "/insights/technical-seo/discovered-not-indexed/": {
        "title": "'발견됨 - 색인되지 않음' 원인 7가지 | OneSearchPro",
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
                 "<p>이 순서대로 점검하면 90% 케이스는 위 3단계에서 원인이 잡힙니다.</p>"
                 "<p><b>1차 자료 참고:</b> 서치콘솔 페이지 색인 상태 보고서의 각 상태(\"발견됨\", \"크롤링됨\", \"색인됨\" 등) 정의와 권장 조치는 구글 공식 도움말의 "
                 "<a href=\"https://support.google.com/webmasters/answer/7440203\" target=\"_blank\" rel=\"noopener noreferrer\">\"페이지 색인 생성 보고서\"</a>에 정리되어 있습니다. 본문의 진단 순서는 이 문서의 상태별 권장 작업을 한국 사이트에서 자주 빠지는 단계 위주로 재정렬한 것입니다.</p>"),
            ],
            key_takeaways=[
                "\"발견됨\"과 \"크롤링됨\"은 다른 단계의 문제라 진단 순서가 다릅니다.",
                "가장 흔한 원인은 내부 링크 부재와 sitemap 노이즈입니다.",
                "JS 렌더링 의존 사이트는 \"발견됨\"에 오래 머무는 경향이 있습니다.",
                "sitemap은 자동 생성보다 큐레이션이 효과적입니다.",
            ],
            related=[
                ("워드프레스 LCP 개선 작업 순서", "/insights/technical-seo/wordpress-lcp-fix/", "기술 SEO"),
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

    "/insights/technical-seo/mobile-first-indexing/": {
        "title": "모바일 우선 색인 점검 가이드 | OneSearchPro",
        "desc": "구글 모바일 우선 색인(Mobile-First Indexing)이 데스크탑 색인과 어떻게 다른지, 반응형 사이트도 점검해야 할 6가지 항목과 흔히 빠뜨리는 함정을 정리합니다.",
        "keywords": "모바일 우선 색인, Mobile-First Indexing, 반응형 SEO, 모바일 SEO, viewport, 콘텐츠 패리티",
        "h1": "모바일 우선 색인 점검 가이드",
        "eyebrow": "TECHNICAL SEO · ARTICLE",
        "lead": "이름은 \"모바일 우선\"이지만 사실상 \"모바일이 전부\"입니다. 데스크탑에만 있고 모바일에 없는 콘텐츠는 색인되지 않습니다. 반응형 사이트도 안심할 수 없는 6가지 점검 항목을 정리합니다.",
        "body": blog_post(
            date="2025-05-14",
            date_modified="2026-05-17",
            reading_time=8,
            intro="구글은 2023년 10월부터 모든 사이트를 모바일 우선 색인으로 평가하고 있습니다. 핵심 의미는 단순합니다 — 구글봇이 사이트를 가져갈 때 데스크탑 버전이 아닌 모바일 버전을 봅니다. 모바일에서 안 보이는 본문·이미지·내부 링크는 사실상 없는 것으로 처리됩니다.",
            sections=[
                ("모바일 우선 색인이 정확히 무엇인가",
                 "<p>가장 흔한 오해 두 가지부터 정리합니다.</p>"
                 "<p><b>오해 1 — \"반응형 사이트라 상관없다\":</b> 반응형이라도 모바일에서 일부 콘텐츠를 <code>display:none</code>으로 숨기거나, 이미지가 다르거나, 일부 내부 링크가 빠지면 그 부분은 색인 손실로 이어집니다. 반응형은 \"같은 코드\"라는 의미일 뿐, \"같은 콘텐츠가 보인다\"는 보장은 아닙니다.</p>"
                 "<p><b>오해 2 — \"별도 모바일 사이트(m.example.com)가 더 안전\":</b> 답이 아닙니다. 관리 부담만 늘고, 데스크탑·모바일 콘텐츠 일치(parity) 점검이 더 까다로워집니다. 구글도 반응형을 공식 권장합니다.</p>"),
                ("데스크탑 색인과의 결정적 차이 3가지",
                 "<ol>"
                 "<li><b>콘텐츠 패리티가 절대적</b> — 데스크탑에만 있는 본문·이미지·링크·메타는 사실상 색인되지 않습니다. \"모바일에서 보이는 것\"이 \"전부\"입니다.</li>"
                 "<li><b>구조화 데이터도 모바일 기준</b> — JSON-LD 마크업이 데스크탑에만 있고 모바일에 빠져있으면 적용되지 않습니다.</li>"
                 "<li><b>모바일 UX가 직접 영향</b> — 탭 영역, 가독성, 가로 스크롤 같은 모바일 UX 신호가 랭킹에 영향을 줍니다.</li>"
                 "</ol>"),
                ("점검 1·2 — viewport 메타와 콘텐츠 패리티",
                 "<p><b>점검 1: viewport 메타 태그</b></p>"
                 "<p>모든 페이지에 다음 태그가 있어야 합니다.</p>"
                 "<p><code>&lt;meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"&gt;</code></p>"
                 "<p>이게 없으면 모바일 친화성 평가에서 즉시 탈락합니다. 빠뜨리는 경우가 의외로 많고, 특히 외주 제작 사이트에서 자주 보입니다.</p>"
                 "<p><b>점검 2: 콘텐츠 패리티</b></p>"
                 "<p>데스크탑/모바일에서 본문·이미지·내부 링크·메타가 동일한지 점검. 자주 빠지는 패턴:</p>"
                 "<ul>"
                 "<li>아코디언이나 탭 안에 숨겨진 본문 (구글은 펼친 상태로 평가하지만 일부 누락 위험)</li>"
                 "<li>사이드바·푸터 콘텐츠가 모바일에서 사라짐</li>"
                 "<li>데스크탑 메뉴에만 있던 카테고리·서브페이지 내부 링크</li>"
                 "<li>호버 시 표시되는 툴팁 본문 (모바일에서는 안 보임)</li>"
                 "</ul>"),
                ("점검 3·4 — 구조화 데이터·모바일 UX",
                 "<p><b>점검 3: 구조화 데이터 일치</b></p>"
                 "<p>Schema.org JSON-LD가 모바일·데스크탑 양쪽에 동일하게 출력되는지 확인합니다. CMS·플러그인을 쓰는 경우 일부 스키마가 데스크탑에만 출력되는 경우가 있습니다.</p>"
                 "<p>점검 방법: Chrome DevTools → Device Mode → 모바일 화면으로 전환 → 페이지 소스에서 JSON-LD 검색.</p>"
                 "<p><b>점검 4: 모바일 UX 기본</b></p>"
                 "<ul>"
                 "<li>탭 영역 최소 48×48px (버튼·링크 사이 간격 포함)</li>"
                 "<li>폰트 16px 이상 (확대해도 가독성 유지)</li>"
                 "<li>가로 스크롤 없음 (overflow 점검)</li>"
                 "<li>Mobile-Friendly Test(search.google.com/test/mobile-friendly) 통과</li>"
                 "</ul>"),
                ("점검 5·6 — 모바일 속도와 미디어",
                 "<p><b>점검 5: 모바일 속도</b></p>"
                 "<p>PageSpeed Insights는 기본적으로 모바일 점수가 기준입니다. LCP·INP·CLS 모두 모바일 점수가 데스크탑보다 낮은 경향이 있으므로, 모바일에 우선 최적화해야 합니다.</p>"
                 "<ul>"
                 "<li>Hero 이미지는 모바일용 별도 srcset 권장 (작은 해상도 버전)</li>"
                 "<li>모바일에서는 WebP·AVIF 압축 효과가 더 큽니다</li>"
                 "<li>3G 환경 시뮬레이션으로 측정 (실제 사용자 일부 환경 반영)</li>"
                 "</ul>"
                 "<p><b>점검 6: 이미지·동영상</b></p>"
                 "<ul>"
                 "<li>모바일에 표시 안 되는 이미지는 색인되지 않음 (alt 텍스트도 무의미)</li>"
                 "<li>lazy loading은 OK, 단 above-the-fold(첫 화면) 이미지는 즉시 로드</li>"
                 "<li>모바일에서 자동 재생되는 동영상은 정책상 음소거 + 사용자 인터랙션 후 가능</li>"
                 "</ul>"),
                ("자주 빠뜨리는 함정 — 데스크탑/모바일 분리 사이트",
                 "<p>별도 도메인(m.example.com) 운영 사이트는 점검 항목이 두 배가 됩니다.</p>"
                 "<ul>"
                 "<li>양쪽 canonical이 정확히 서로를 가리켜야 함</li>"
                 "<li><code>alternate</code> 태그로 데스크탑-모바일 연결</li>"
                 "<li>두 사이트 간 콘텐츠가 동일하게 유지되는지 (시간이 지나면 어긋나는 경우가 많음)</li>"
                 "<li>모바일 사이트 robots.txt가 차단되지 않는지</li>"
                 "<li>두 사이트의 구조화 데이터, sitemap 모두 점검</li>"
                 "</ul>"),
                ("측정 — 서치콘솔과 외부 도구",
                 "<p>점검 도구 4가지를 함께 사용합니다.</p>"
                 "<ul>"
                 "<li><b>서치콘솔 → URL 검사</b>: 각 URL의 \"모바일 사용성\" 확인</li>"
                 "<li><b>Mobile-Friendly Test</b>: 모바일 친화성 합격/불합격 + 구체적 이슈</li>"
                 "<li><b>PageSpeed Insights (Mobile 탭)</b>: Field Data가 실제 사용자 데이터, 랭킹 기준</li>"
                 "<li><b>서치콘솔 \"Core Web Vitals\" 모바일 리포트</b>: 사이트 전체 모바일 성능 추적</li>"
                 "</ul>"),
                ("주의할 점 — 콘텐츠가 먼저, 디자인은 나중",
                 "<p>모바일 우선 색인 점검에서 가장 자주 놓치는 우선순위가 \"디자인보다 콘텐츠\"입니다. 모바일 화면이 예쁘게 보이는 것보다 \"같은 콘텐츠가 데스크탑/모바일에서 동일하게 보이는가\"가 압도적으로 중요합니다.</p>"
                 "<p>또한 변경 직후 일시적 트래픽 하락이 있을 수 있습니다. 데스크탑 콘텐츠 의존도가 높았던 사이트일수록 영향이 큽니다. 1~2주 관찰 후 안정화 여부를 봅니다.</p>"),
            ],
            key_takeaways=[
                "모바일 우선 색인은 \"모바일에서 보이는 게 색인 기준\"이 된다는 의미입니다.",
                "반응형이라도 콘텐츠 패리티(데스크탑/모바일 내용 일치)는 별도 점검이 필요합니다.",
                "구조화 데이터·내부 링크가 모바일에서 빠지면 그 신호도 빠집니다.",
                "별도 모바일 도메인은 관리 부담만 큽니다. 반응형이 정답입니다.",
            ],
            related=[
                ("워드프레스 LCP 개선 작업 순서", "/insights/technical-seo/wordpress-lcp-fix/", "기술 SEO"),
                ("서치콘솔 \"발견됨 - 현재 색인되지 않음\" 7가지 원인과 진단 순서", "/insights/technical-seo/discovered-not-indexed/", "기술 SEO"),
                ("기술 SEO 진단 서비스", "/services/technical-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/technical-seo/mobile-first-indexing/",
            title="모바일 우선 색인 점검 가이드",
            desc="모바일 우선 색인의 데스크탑 색인 차이점과 점검 6가지.",
            date_published="2025-05-14",
            date_modified="2026-05-17"
        ),
        "active": "insights",
    },

    "/insights/technical-seo/wordpress-lcp-fix/": {
        "title": "워드프레스 LCP 개선 작업 순서 | OneSearchPro",
        "desc": "워드프레스 사이트의 LCP(Largest Contentful Paint)가 느려지는 가장 흔한 4가지 원인과 효과 큰 순서로 정리한 작업 매뉴얼. 실측 기반.",
        "keywords": "워드프레스 LCP, Core Web Vitals, LCP 개선, 페이지 속도, 워드프레스 최적화",
        "h1": "워드프레스 LCP 개선 작업 순서",
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
                ("사이트 리뉴얼 301 매핑 실수 12가지", "/insights/visibility/301-migration-mistakes/", "검색 노출"),
                ("기술 SEO 진단 서비스", "/services/technical-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/technical-seo/wordpress-lcp-fix/",
            title="워드프레스 LCP 개선 작업 순서",
            desc="워드프레스 LCP 개선의 4가지 핵심 작업과 빈도순 매뉴얼.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    # Content SEO category
    "/insights/content-seo/medical-blog-first-100/": {
        "title": "병원·치과 블로그 첫 100자 작성법 | OneSearchPro",
        "desc": "병원·치과 블로그가 검색 노출이 약한 이유는 첫 100자에 있습니다. 환자가 실제로 검색하는 표현으로 시작하는 패턴과 의료광고심의 충돌을 피하는 작성법.",
        "keywords": "병원 블로그 SEO, 치과 블로그, 의료 콘텐츠, 환자 검색어, 의료광고심의",
        "h1": "병원·치과 블로그 첫 100자 작성법",
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
                ("쇼핑몰 제품 페이지 본문 6단락 구조", "/insights/content-seo/product-page-content-structure/", "콘텐츠 SEO"),
                ("Helpful Content System 셀프 점검 7가지", "/insights/google-seo/helpful-content-self-check/", "구글 SEO"),
                ("콘텐츠 SEO 서비스", "/services/content-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/content-seo/medical-blog-first-100/",
            title="병원·치과 블로그 첫 100자 작성법",
            desc="병원 블로그 첫 100자 작성법과 의료광고심의 회피 패턴.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/content-seo/product-page-content-structure/": {
        "title": "쇼핑몰 제품 페이지 본문 6단락 구조 | OneSearchPro",
        "desc": "쇼핑몰 제품 페이지가 이미지 중심으로만 만들어져 검색 노출이 안 될 때, 본문을 채우는 6단락 구조와 스키마 마크업 가이드.",
        "keywords": "쇼핑몰 제품 페이지 SEO, 제품 상세 페이지, 제품 본문, Product 스키마, 쇼핑몰 콘텐츠",
        "h1": "쇼핑몰 제품 페이지 본문 6단락 구조",
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
                ("병원·치과 블로그 첫 100자 작성법", "/insights/content-seo/medical-blog-first-100/", "콘텐츠 SEO"),
                ("Helpful Content System 셀프 점검 7가지", "/insights/google-seo/helpful-content-self-check/", "구글 SEO"),
                ("콘텐츠 SEO 서비스", "/services/content-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/content-seo/product-page-content-structure/",
            title="쇼핑몰 제품 페이지 본문 6단락 구조",
            desc="쇼핑몰 제품 페이지에 본문을 채우는 6단락 구조와 스키마 가이드.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    # Local SEO category
    "/insights/local-seo/new-store-naver-place/": {
        "title": "신규 매장 네이버 플레이스 3개월 운영 | OneSearchPro",
        "desc": "신규 매장이 네이버 플레이스에서 \"리뷰 0\" 상태로 시작할 때, 첫 3개월을 어떻게 운영해야 노출이 자연스럽게 자라는지 정리합니다.",
        "keywords": "네이버 플레이스, 신규 매장 SEO, 영수증 리뷰, 플레이스 노출, 로컬 SEO",
        "h1": "신규 매장 네이버 플레이스 3개월 운영",
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
                ("다지점 매장 GBP 본사·지점 분리 원칙", "/insights/local-seo/multi-location-gbp/", "지역 SEO"),
                ("지역 SEO 사례", "/case-studies/local-seo/", "성공사례"),
                ("지역 SEO 서비스", "/services/local-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/local-seo/new-store-naver-place/",
            title="신규 매장 네이버 플레이스 3개월 운영",
            desc="신규 매장 네이버 플레이스 운영 첫 3개월의 우선순위 매뉴얼.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/local-seo/multi-location-gbp/": {
        "title": "다지점 매장 GBP 본사·지점 분리 원칙 | OneSearchPro",
        "desc": "지점 여러 개를 운영하는 매장이 구글 비즈니스 프로필을 통합 관리할 때, 본사·지점 정보를 어떻게 분리해야 지역 키워드 노출이 분산되지 않는지 정리합니다.",
        "keywords": "구글 비즈니스 프로필, GBP, 다지점 매장, 프랜차이즈 SEO, NAP 일관성",
        "h1": "다지점 매장 GBP 본사·지점 분리 원칙",
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
                ("신규 매장 네이버 플레이스 3개월 운영", "/insights/local-seo/new-store-naver-place/", "지역 SEO"),
                ("지역 SEO 사례", "/case-studies/local-seo/", "성공사례"),
                ("지역 SEO 서비스", "/services/local-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/local-seo/multi-location-gbp/",
            title="다지점 매장 GBP 본사·지점 분리 원칙",
            desc="다지점 매장의 GBP 운영 원칙과 본사·지점 정보 분리 가이드.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    # Backlink & Digital PR category
    "/insights/backlink-pr/disavow-decision/": {
        "title": "위험한 백링크 Disavow 결정 기준 | OneSearchPro",
        "desc": "이전 대행사가 만든 백링크 중 위험한 것을 식별하고 Disavow 여부를 결정하는 기준. 즉시 처리·보류·유지 3단계 분류와 단계적 제출 전략.",
        "keywords": "Disavow, 백링크 진단, 위험한 백링크, 백링크 정리, 페널티 회복",
        "h1": "위험한 백링크 Disavow 결정 기준",
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
                 "<p>두 경우를 구분하지 않고 같은 전략으로 가면 손해가 큽니다.</p>"
                 "<p><b>1차 자료 참고:</b> Disavow 도구의 사용 시점·파일 형식·제출 절차는 구글 공식 도움말 "
                 "<a href=\"https://support.google.com/webmasters/answer/2648487\" target=\"_blank\" rel=\"noopener noreferrer\">\"Disavow links to your site\"</a>에 정리되어 있습니다. 본 글의 \"보류 vs 즉시 처리\" 기준은 구글이 권장하는 \"수동 조치를 받았거나, 받을 가능성이 매우 높다고 판단될 때만 사용\" 원칙에 기반한 실무 해석입니다.</p>"),
            ],
            key_takeaways=[
                "도구 점수는 1차 필터일 뿐, 위험 판단은 사이트 직접 확인 후 사람이 해야 합니다.",
                "즉시 Disavow는 명백한 스팸(스팸 디렉토리·자동 생성·도박/성인 인접 등)만.",
                "보류 대상은 3~6개월 관찰 후 결정. 무차별 처리는 살아있는 신호까지 차단합니다.",
                "Disavow는 단계적으로(1차→4주 관찰→2차) 제출해야 효과 측정이 가능합니다.",
            ],
            related=[
                ("한국 언론사 보도자료 백링크 구분법", "/insights/backlink-pr/korean-press-release/", "백링크 · 디지털 PR"),
                ("서치콘솔 \"크롤링됨 - 현재 색인되지 않음\" — 다른 상태와의 차이와 대응법", "/insights/visibility/crawled-not-indexed/", "검색 노출"),
                ("디지털 PR · 백링크 진단 서비스", "/services/digital-pr/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/backlink-pr/disavow-decision/",
            title="위험한 백링크 Disavow 결정 기준",
            desc="위험한 백링크의 3단계 분류와 단계적 Disavow 제출 전략.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/backlink-pr/korean-press-release/": {
        "title": "한국 언론사 보도자료 백링크 구분법 | OneSearchPro",
        "desc": "한국 언론사에 보도자료를 뿌렸을 때 백링크가 따라오는 매체와 안 오는 매체의 차이. 본문 링크 vs 텍스트 언급, 발행 패턴, 측정 방법.",
        "keywords": "보도자료 SEO, 언론사 백링크, 디지털 PR, 보도자료 배포, 한국 언론 SEO",
        "h1": "한국 언론사 보도자료 백링크 구분법",
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
                ("위험한 백링크 Disavow 결정 기준", "/insights/backlink-pr/disavow-decision/", "백링크 · 디지털 PR"),
                ("Helpful Content System 셀프 점검 7가지", "/insights/google-seo/helpful-content-self-check/", "구글 SEO"),
                ("디지털 PR · 백링크 진단 서비스", "/services/digital-pr/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/backlink-pr/korean-press-release/",
            title="한국 언론사 보도자료 백링크 구분법",
            desc="한국 언론 보도자료의 백링크 보존 패턴과 매체별 SEO 가치.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    # SNS Marketing category
    "/insights/sns/youtube-shorts-description/": {
        "title": "유튜브 쇼츠 설명란 트래픽 유도법 | OneSearchPro",
        "desc": "유튜브 쇼츠 설명란을 어떻게 써야 본 영상이나 외부 사이트로 트래픽이 흐르는지. 첫 줄·본문·해시태그 구조와 측정 방법.",
        "keywords": "유튜브 쇼츠 SEO, 쇼츠 설명란, 유튜브 마케팅, 쇼츠 클릭률, 외부 링크 유도",
        "h1": "유튜브 쇼츠 설명란 트래픽 유도법",
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
                ("인스타그램 프로필 링크 SEO 비교", "/insights/sns/instagram-link-in-bio/", "SNS 마케팅"),
                ("쇼핑몰 제품 페이지 본문 6단락 구조", "/insights/content-seo/product-page-content-structure/", "콘텐츠 SEO"),
                ("SNS 마케팅 서비스", "/services/social-media/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/sns/youtube-shorts-description/",
            title="유튜브 쇼츠 설명란 트래픽 유도법",
            desc="유튜브 쇼츠 설명란의 첫 줄·본문·해시태그 구조와 클릭률 측정.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/sns/instagram-link-in-bio/": {
        "title": "인스타그램 프로필 링크 SEO 비교 | OneSearchPro",
        "desc": "인스타그램 프로필에 링크인바이오 서비스(Linktree 등)와 자체 랜딩 페이지 중 어느 것을 써야 하나. SEO·UX·트래킹 관점에서 비교.",
        "keywords": "인스타그램 프로필 링크, 링크인바이오, Linktree, 인스타 SEO, SNS 유입",
        "h1": "인스타그램 프로필 링크 SEO 비교",
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
                ("유튜브 쇼츠 설명란 트래픽 유도법", "/insights/sns/youtube-shorts-description/", "SNS 마케팅"),
                ("쇼핑몰 제품 페이지 본문 6단락 구조", "/insights/content-seo/product-page-content-structure/", "콘텐츠 SEO"),
                ("SNS 마케팅 서비스", "/services/social-media/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/sns/instagram-link-in-bio/",
            title="인스타그램 프로필 링크 SEO 비교",
            desc="인스타 프로필 링크 두 선택지의 SEO·UX·측정 관점 비교.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    # Visibility category
    "/insights/visibility/301-migration-mistakes/": {
        "title": "사이트 리뉴얼 301 매핑 실수 12가지 | OneSearchPro",
        "desc": "사이트 리뉴얼 후 트래픽이 절반으로 떨어지는 가장 흔한 원인은 301 리다이렉트 매핑 누락입니다. 자주 빠뜨리는 12가지 항목과 출시 후 모니터링 방법.",
        "keywords": "사이트 리뉴얼, 301 리다이렉트, URL 마이그레이션, 트래픽 손실, 리뉴얼 SEO",
        "h1": "사이트 리뉴얼 301 매핑 실수 12가지",
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
                ("워드프레스 LCP 개선 작업 순서", "/insights/technical-seo/wordpress-lcp-fix/", "기술 SEO"),
                ("SEO 웹사이트 제작 서비스", "/services/web-design/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/visibility/301-migration-mistakes/",
            title="사이트 리뉴얼 301 매핑 실수 12가지",
            desc="사이트 리뉴얼 시 301 매핑에서 자주 누락되는 12가지 항목과 모니터링.",
            date_published="2025-05-14"
        ),
        "active": "insights",
    },

    "/insights/visibility/crawled-not-indexed/": {
        "title": "'크롤링됨 - 색인되지 않음' 대응법 | OneSearchPro",
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
                ("Helpful Content System 셀프 점검 7가지", "/insights/google-seo/helpful-content-self-check/", "구글 SEO"),
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
    "/insights/content-seo/search-intent-4-types-keyword-classification-page-strategy/": {
        "title": "검색 의도 4가지 유형과 키워드 분류 | OneSearchPro",
        "desc": "정보형·탐색형·거래형·상업형 4가지 검색 의도를 구분하고 키워드별 페이지를 설계하는 실무 가이드. 네이버·구글 SERP 분석 절차와 혼합 의도 처리법까지 정리합니다.",
        "keywords": "검색 의도, 키워드 분류, 콘텐츠 SEO, 정보형 키워드, 거래형 키워드, SERP 분석, 네이버 SEO",
        "h1": "검색 의도 4가지 유형 — 키워드별로 어떻게 분류하고 페이지를 만드나",
        "eyebrow": "콘텐츠 SEO · ARTICLE",
        "lead": "같은 키워드라도 사용자가 원하는 결과는 다릅니다. 검색 의도를 정확히 파악해야 페이지가 상위에 잡힙니다.",
        "body": blog_post(
            date="2026-05-14",
            date_modified="2026-05-17",
            reading_time=8,
            intro="검색 의도를 잘못 매핑한 페이지는 기술 SEO가 완벽해도 상위 노출이 어렵습니다. 같은 키워드라도 사용자 의도는 다르고, 검색엔진은 그 차이를 SERP 구성으로 명확히 보여줍니다. 이 글에서는 정보형·탐색형·거래형·상업형 4가지 의도를 구분하는 기준과, 키워드별로 어떤 페이지를 만들어야 하는지 실무 관점에서 정리합니다.",
            sections=[
                ("1. 검색 의도(Search Intent)가 SEO에서 중요한 이유",
                 """<p>검색 엔진은 사용자가 입력한 키워드 뒤에 숨은 <strong>진짜 목적</strong>을 추정합니다. 네이버의 통합검색 영역 배치, 구글의 Featured Snippet·People Also Ask·Shopping 탭 같은 SERP 기능은 모두 이 의도 추정의 결과로 만들어집니다. 사용자가 무엇을 원하는지 추정해 \"가장 적절한 결과 형식\"을 위에 올리는 거죠.</p><p>예를 들어 \"에어컨 청소\"라는 동일한 키워드도 사용자에 따라 의도가 다릅니다. 직접 청소법을 알고 싶은 사람(정보형)도 있고, 업체를 찾아 예약하려는 사람(거래형)도 있습니다. 한 페이지가 두 의도를 동시에 만족시키기는 어렵습니다.</p><p>실무에서 의도 매칭 실패는 다음 신호로 자주 드러납니다 — 노출은 되는데 클릭률이 낮거나, 클릭은 받지만 체류 시간이 매우 짧거나, 검색 트래픽의 행동이 직접 트래픽과 다르게 어긋남. 이런 신호가 보이면 콘텐츠 보강 전에 \"의도 매칭부터\" 점검해야 합니다.</p>"""),
                ("2. 정보형(Informational) 검색 의도와 콘텐츠 전략",
                 """<p>정보형 검색은 <strong>지식 습득·문제 해결 방법</strong>을 목적으로 합니다. \"SEO란\", \"김치찌개 끓이는 법\", \"퇴직금 계산 방법\" 같은 키워드가 대표적입니다. 네이버에서는 VIEW·지식iN·블로그 영역이, 구글에서는 Featured Snippet·People Also Ask 영역이 주로 노출됩니다.</p><ul><li><strong>키워드 패턴:</strong> ~이란, ~방법, ~하는 법, why, how to, what is</li><li><strong>최적 콘텐츠 형식:</strong> 가이드 블로그, 튜토리얼, FAQ, 비교 분석 글</li><li><strong>CTA 전략:</strong> 직접 판매보다 뉴스레터 구독·자료 다운로드·후속 단계 안내</li></ul><p><strong>자주 보이는 실수:</strong> 정보형 키워드에 제품 상세 페이지를 매핑하는 경우. 사용자는 정보를 원했는데 판매 페이지가 노출되면 뒤로가기까지 시간이 매우 짧습니다. 정보형 키워드는 정보를 제공하는 페이지로 받고, 그 안에서 다음 단계로 자연스럽게 안내하는 2단계 구조가 효과적입니다.</p>"""),
                ("3. 탐색형(Navigational) 검색 의도 — 브랜드·특정 페이지 찾기",
                 """<p>탐색형 검색은 <strong>특정 웹사이트·브랜드·페이지로 직접 이동</strong>하려는 의도입니다. \"유튜브 로그인\", \"쿠팡 고객센터\", \"브랜드명 + 서비스명\"처럼 브랜드명이나 고유명사가 포함됩니다. 네이버 통합검색 최상단에 사이트 링크가, 구글에서는 Knowledge Panel·사이트 링크가 노출됩니다.</p><ul><li><strong>키워드 패턴:</strong> 브랜드명, 브랜드명+로그인/가격/후기, 특정 서비스명</li><li><strong>최적 대응:</strong> 공식 홈페이지 메타 최적화, Organization 스키마, 네이버 플레이스·브랜드 검색 등록</li><li><strong>자사 브랜드 키워드:</strong> 이미 인지도가 있는 상태이므로 공식 페이지의 자연 검색 상위 유지가 핵심</li><li><strong>경쟁사 브랜드 키워드:</strong> 콘텐츠 SEO보다 비교 콘텐츠(\"A와 B의 차이\")로 우회 진입이 현실적</li></ul><p><strong>주의:</strong> 네이버 파워링크에서 타사 상표권 키워드 입찰은 상표권 신고로 광고 중단으로 이어질 수 있습니다. 자사 브랜드 검색에 자기 광고를 띄우는 것도 비용 효율 측면에서 일반적으로 비추천이며, 자연 검색 결과가 상위면 충분합니다.</p>"""),
                ("4. 거래형(Transactional) 검색 의도 — 구매·전환 직전",
                 """<p>거래형 검색은 <strong>즉시 구매·가입·예약</strong> 행동을 목적으로 합니다. \"운동화 구매\", \"호텔 예약\", \"온라인 강의 등록\" 같은 키워드가 해당합니다. 네이버 쇼핑·스마트스토어, 구글 Shopping 탭이 주요 노출 영역입니다.</p><ul><li><strong>키워드 패턴:</strong> 구매, 예약, 신청, 할인, buy, order, book now</li><li><strong>최적 페이지:</strong> 제품 상세(PDP), 서비스 랜딩, 프로모션 페이지</li><li><strong>전환 핵심 요소:</strong> 명확한 CTA 버튼, 신뢰 신호(리뷰·인증·배송 정보), 간편 결제 옵션</li></ul><p><strong>자주 보이는 실수:</strong> 거래형 키워드에 긴 가이드 형식 글을 매핑하는 경우. 사용자는 빨리 구매하고 싶은데 \"○○ 완벽 가이드 5,000자\"가 첫 화면에 나오면 결정이 지연됩니다. 거래형 의도에서는 <strong>결정 장벽을 낮추는 페이지 구조</strong>가 긴 설명보다 효과적입니다.</p>"""),
                ("5. 상업형(Commercial Investigation) 검색 의도 — 구매 전 비교",
                 """<p>상업형 검색은 거래 직전 <strong>제품 비교·후기 확인·대안 탐색</strong> 단계입니다. \"노트북 추천\", \"A vs B 비교\", \"○○ 후기\" 같은 키워드로, 정보형과 거래형의 중간 성격을 띱니다. 네이버 VIEW 탭 상위에 \"추천·후기·비교\" 콘텐츠가 배치됩니다.</p><ul><li><strong>키워드 패턴:</strong> 추천, 비교, 후기, best, top, review, vs</li><li><strong>최적 콘텐츠:</strong> 비교 가이드, 제품 라운드업, 사용 후기 집계, 의사결정 체크리스트</li><li><strong>전환 연결:</strong> 콘텐츠 내 제품 링크, 하단에 상담 신청·무료 체험 CTA 배치</li></ul><p><strong>AI 요약 시대의 차별화:</strong> 구글 SGE(Search Generative Experience)와 네이버 하이퍼클로바X 적용 이후 비교 콘텐츠의 클릭 환경이 변하고 있습니다. AI가 요약할 수 없는 차별점 — 본인이 직접 사용해본 경험, 자체 테스트 결과, 사용자 인터뷰 — 이 포함되어야 클릭 가치가 유지됩니다. \"누가 인터넷 정보를 재정리한 글\"은 점점 가치가 떨어집니다.</p>"""),
                ("6. 키워드를 4가지 의도로 분류하는 실전 프로세스",
                 """<p>검색 의도를 판단할 때는 <strong>키워드 자체보다 실제 검색 결과</strong>를 우선 분석해야 합니다. 같은 키워드라도 시장·시즌·사용자층에 따라 의도가 달라지기 때문입니다.</p><ol><li><strong>SERP 분석:</strong> 네이버·구글에서 키워드 직접 검색 → 상위 10개 결과 유형(블로그/쇼핑/동영상/공식 페이지) 확인</li><li><strong>탭·영역 확인:</strong> 네이버 VIEW/쇼핑/플레이스 어느 탭이 상단인지, 구글 Featured Snippet/Shopping/Local Pack 노출 여부 점검</li><li><strong>키워드 수식어로 1차 분류:</strong> \"방법\", \"추천\", \"구매\" 같은 접미사로 가설을 세우고 SERP로 검증</li><li><strong>도구로 정량 점검:</strong> 네이버 검색광고 키워드 도구·구글 키워드 플래너에서 경쟁도·CPC 확인. CPC가 높을수록 상업형·거래형 가능성 증가</li><li><strong>스프레드시트로 분류:</strong> 키워드 목록에 \"의도\" 열 추가, 정보/탐색/거래/상업 태그 부여 → 페이지 유형 매핑</li></ol><p><code>예시: \"에어프라이어\" → 네이버 쇼핑 탭 최상단 → 거래형 / \"에어프라이어 요리법\" → VIEW 탭 우세 → 정보형</code></p><p><strong>혼합 의도 주의:</strong> 한 키워드가 여러 의도를 동시에 가질 수 있습니다. \"다이어트\"는 정보형(방법 안내)과 상업형(보조제 비교)이 혼재합니다. 포괄적 콘텐츠로 다루거나 의도별로 별도 페이지를 준비해야 합니다.</p>"""),
                ("7. 검색 의도별 페이지 제작 체크리스트와 흔한 실수",
                 """<p>의도를 분류한 뒤에는 각 유형에 맞는 페이지 구조·콘텐츠 요소·전환 경로를 설계합니다.</p><table><thead><tr><th>의도 유형</th><th>페이지 형식</th><th>핵심 요소</th><th>흔한 실수</th></tr></thead><tbody><tr><td>정보형</td><td>가이드·블로그</td><td>목차·단계별 설명·예시</td><td>과도한 제품 링크로 신뢰 하락</td></tr><tr><td>탐색형</td><td>홈·서비스 페이지</td><td>브랜드명·사이트 링크·Organization 스키마</td><td>공식 페이지 메타 미최적화</td></tr><tr><td>거래형</td><td>상품·랜딩</td><td>가격·CTA·신뢰 신호</td><td>긴 설명으로 결정 지연</td></tr><tr><td>상업형</td><td>비교·추천</td><td>표·차트·자체 데이터</td><td>제휴 링크만 나열해 편향 의심</td></tr></tbody></table><p><strong>자주 보이는 실수 패턴:</strong></p><ul><li>혼합 의도 키워드에 한 가지 유형의 페이지만 매핑</li><li>거래형 페이지에 신뢰 요소(리뷰·환불 정책·배송 정보) 누락</li><li>정보형 글에 제품 링크를 과도하게 삽입해 광고성 글로 인식</li><li>SERP를 보지 않고 키워드 수식어만으로 의도 판단</li></ul><p>네이버 C-랭크는 체류 시간·재방문율로 콘텐츠 만족도를 평가합니다. 거래형 페이지라도 최소한의 신뢰 요소를 갖춰야 안정적인 순위가 유지되는 경향이 있습니다. SERP 결과만 보고 의도를 추정하는 것보다, 실제 페이지를 띄운 뒤 행동 신호(체류·이탈·재검색)를 추적하는 게 가장 정확한 검증입니다.</p>""")
            ],
            key_takeaways=[
                "검색 의도는 정보형·탐색형·거래형·상업형 4가지로 구분합니다. 네이버·구글 모두 의도 일치 페이지를 우선 노출합니다.",
                "키워드 수식어보다 실제 SERP(검색 결과 페이지) 분석이 의도 판단의 핵심입니다. 상위 10개 결과 유형과 탭 배치를 확인하세요.",
                "정보형 키워드에 상품 페이지를 매핑하거나, 거래형 키워드에 긴 가이드를 노출하면 이탈과 전환율 손실이 자주 발생합니다.",
                "AI 요약 시대에는 자체 테스트·실제 사용 경험으로 차별화된 콘텐츠만 클릭 가치가 유지됩니다."
            ],
            related=[
                ("쇼핑몰 제품 페이지 본문 6단락 구조", "/insights/content-seo/product-page-content-structure/", "콘텐츠 SEO"),
                ("병원·치과 블로그 첫 100자 — 환자 검색어로 시작해야 하는 이유", "/insights/content-seo/medical-blog-first-100/", "콘텐츠 SEO"),
                ("SEO 컨설팅 서비스", "/services/seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/content-seo/search-intent-4-types-keyword-classification-page-strategy/",
            title="검색 의도 4가지 유형 — 키워드별로 어떻게 분류하고 페이지를 만드나",
            desc="정보형·탐색형·거래형·상업형 4가지 검색 의도 구분 기준과 키워드별 페이지 매핑 실무 가이드.",
            date_published="2026-05-14",
            date_modified="2026-05-17"
        ),
        "active": "insights",
    },
    "/insights/local-seo/negative-review-response-mistakes/": {
        "title": "네이버 플레이스 부정 리뷰 대응 — 자주 하는 실수 5가지 | OneSearchPro",
        "desc": "네이버 플레이스의 부정 리뷰는 \"제거 대상\"이 아니라 \"응답 대상\"입니다. 사장님들이 자주 하는 5가지 대응 실수와 신뢰를 잃지 않는 응답 4단계 프로세스를 정리합니다.",
        "keywords": "네이버 플레이스 부정 리뷰, 악성 리뷰 대응, 리뷰 신고, 리뷰 답글, 네이버 리뷰 삭제, 지역 SEO 리뷰 관리",
        "h1": "네이버 플레이스 부정 리뷰 대응 — 자주 하는 실수 5가지",
        "eyebrow": "LOCAL SEO · ARTICLE",
        "lead": "네이버 플레이스에 부정 리뷰가 달리면 가장 먼저 떠오르는 생각은 \"빨리 지우고 싶다\"입니다. 그런데 현장에서 가장 손해를 보는 패턴은 거의 항상 \"성급한 대응\"이었습니다. 매장 사장님들이 자주 빠지는 5가지 실수와, 잠재 고객에게는 오히려 신뢰 신호로 작용하는 응답 4단계 프로세스를 정리합니다.",
        "body": blog_post(
            date="2026-05-17",
            reading_time=8,
            intro="부정 리뷰가 달린 직후 24시간이 가장 위험합니다. 화가 난 상태에서 즉시 반박하거나 법적 위협을 언급한 답글이 캡처되어 커뮤니티·SNS로 확산된 사례를 자주 봅니다. 부정 리뷰 자체보다 부정 리뷰에 대한 답글이 잠재 고객의 결정에 더 큰 영향을 주는 경우가 많습니다. 네이버 플레이스의 리뷰는 단순한 평점 데이터가 아니라 \"이 매장은 고객을 어떻게 대하는가\"를 보여주는 가장 직접적인 신호입니다.",
            sections=[
                ("실수 1 — 즉시 반박·법적 위협으로 응답",
                 "<p>가장 흔하고 가장 손해가 큰 실수입니다. \"사실관계가 다르다\", \"악의적 리뷰다\", \"법적 조치를 검토하겠다\" 같은 표현은 본인 입장에서는 정당해 보이지만, 같은 리뷰 화면을 보고 있는 100명의 잠재 고객 입장에서는 \"이 매장은 컴플레인에 어떻게 반응하는가\"의 답으로 읽힙니다.</p>"
                 "<p>특히 \"법적 조치\" 언급은 명예훼손·협박 시비로 역공받는 경우가 자주 보입니다. 네이버 약관상 작성된 리뷰가 사실 기반이면 삭제 요청 사유로 인정되지 않으며, 오히려 답글이 캡처되어 \"갑질\" 프레임으로 확산되는 위험이 더 큽니다.</p>"
                 "<p>실무 관찰상 가장 효과적인 첫 24시간 응대는 \"답변 작성 자체를 미루는 것\"입니다. 감정이 가라앉은 후 작성하는 답글이 거의 항상 더 좋은 결과를 만듭니다.</p>"),
                ("실수 2 — 익명·운영자 표시 없이 응답",
                 "<p>네이버 플레이스 답글은 작성자가 \"○○ 사장님\" 또는 \"○○ 운영팀\" 같이 명시될 때와 빈 닉네임일 때의 신뢰도 차이가 큽니다. 빈 닉네임 답글은 \"알바생이 쓴 형식적 답변\"으로 인식되는 경우가 많습니다.</p>"
                 "<p>네이버 비즈니스 정보 관리에서 답글 작성자명을 \"매장명 + 직책\" 형식(예: \"○○카페 사장\", \"○○치과 원장\")으로 설정하면 답글마다 일관된 운영자 신원이 노출됩니다. 이게 작아 보이지만 \"이 매장은 누가 책임지고 응답하는가\"의 신뢰 신호로 작용합니다.</p>"),
                ("실수 3 — 리뷰 신고에 의존하기",
                 "<p>네이버 플레이스의 리뷰 신고 시스템은 명확한 약관 위반(욕설, 무관한 광고, 명백한 허위 사실)에만 처리됩니다. \"기분 나쁘다\", \"평점이 부당하다\" 같은 사유로는 거의 받아들여지지 않습니다.</p>"
                 "<p>현장에서 자주 보는 패턴은 한 달 동안 같은 리뷰를 5번 신고하고 5번 모두 반려된 후에야 \"신고로는 안 되는구나\"를 알게 되는 경우입니다. 신고가 가능한 리뷰는 다음 정도로 좁힙니다 — 욕설·인격 모독 표현 포함, 매장과 무관한 광고·외부 링크, 명백히 다른 매장 리뷰가 잘못 등록된 경우, 동일 사용자의 반복 도배. 그 외에는 신고 대신 \"답글로 정중히 응대\"가 더 빠른 길입니다.</p>"),
                ("실수 4 — 가짜 긍정 리뷰로 부정 리뷰를 묻기",
                 "<p>부정 리뷰를 가리려고 지인·직원·외주를 통해 단기간에 긍정 리뷰를 대량 등록하는 경우가 자주 보입니다. 네이버 플레이스의 리뷰 평가 알고리즘은 다음 신호를 종합 평가합니다 — 작성 계정의 영수증 인증 여부, 작성 시점의 매장 방문 시간대 분포, 동일 IP·기기에서의 다중 작성, 작성 패턴의 자연스러움(같은 시간대 집중 작성은 비정상 신호).</p>"
                 "<p>가짜 리뷰가 적발되면 해당 리뷰만 삭제되는 게 아니라 매장 신뢰도 점수가 떨어지고, 심한 경우 검색 노출 자체가 줄어들 수 있습니다. 단기 가림 효과보다 장기 신뢰 손상이 훨씬 큰 경우가 많습니다.</p>"),
                ("실수 5 — 부정 리뷰만 골라 답글, 긍정 리뷰는 무시",
                 "<p>대부분의 매장이 부정 리뷰에만 답글을 답니다. 그런데 잠재 고객 관점에서 리뷰 페이지를 스크롤할 때 \"부정 리뷰에만 답글이 있는 매장\"은 방어적·수동적으로 보입니다.</p>"
                 "<p>긍정 리뷰에도 \"방문해주셔서 감사합니다, 다음에 ○○도 한번 드셔보세요\" 같은 짧은 개인화 답글을 달면 두 가지 효과가 있습니다. 첫째, 매장이 모든 리뷰를 보고 있다는 신호로 작용해 부정 리뷰 답글의 신뢰도가 올라갑니다. 둘째, 답글에 자연스럽게 메뉴명·서비스명이 들어가면 네이버 검색 노출에서 키워드 풍부도가 올라가는 부수 효과가 있습니다.</p>"),
                ("부정 리뷰 응답 4단계 권장 프로세스",
                 "<p>실무에서 효과가 검증된 4단계 응답 순서입니다. 첫 24시간은 응답을 미루고 다음 순서로 진행합니다.</p>"
                 "<ol>"
                 "<li><b>1단계 — 사실관계 확인:</b> 영수증 기록, CCTV, 직원 면담으로 \"실제 발생한 상황\"을 파악합니다. 사실이 다르다면 \"우리 매장 기록과 다르다\"는 정중한 표현으로 정리합니다. 사실이 맞다면 인정과 사과부터 시작합니다.</li>"
                 "<li><b>2단계 — 답글 초안 작성:</b> 본인 + 다른 한 명이 읽어보는 절차를 권장합니다. 감정 표현·법적 위협·자기 변호 표현을 제거합니다. 답글은 작성자 1명이 아니라 \"이 답글을 보게 될 잠재 고객 100명\"을 대상으로 쓴다는 관점이 유용합니다.</li>"
                 "<li><b>3단계 — 구체적 후속 조치 제안:</b> \"매장으로 다시 방문해주시면\", \"전화로 자세한 상황 들려주시면\" 같은 후속 채널을 제시합니다. 이게 있어야 \"형식적 답변\"이 아닌 \"실제 해결 의지\"로 읽힙니다.</li>"
                 "<li><b>4단계 — 운영자명·연락처 명시:</b> 답글 끝에 \"○○ 사장 ○○○\" 또는 \"운영팀 ○○○\" 같이 책임자 신원을 명시합니다. 가능하면 직접 통화 가능한 채널(매장 전화·카카오톡 채널)도 함께 안내합니다.</li>"
                 "</ol>"
                 "<p>이 4단계는 부정 리뷰를 \"손해\"에서 \"잠재 고객에게 우리 매장의 응대 수준을 보여주는 기회\"로 전환하는 가장 안정적인 방법입니다.</p>"),
            ],
            key_takeaways=[
                "부정 리뷰는 제거 대상이 아니라 응답 대상입니다. 답글의 품질이 부정 리뷰 자체보다 잠재 고객 결정에 더 큰 영향을 줍니다.",
                "첫 24시간은 응답을 미루고 사실관계부터 확인합니다. 감정 상태에서 작성한 답글이 가장 큰 손해를 만듭니다.",
                "답글 작성자명을 \"매장명 + 직책\"으로 명시하면 운영자 신원 신뢰 신호가 일관되게 작용합니다.",
                "가짜 긍정 리뷰는 단기 효과보다 장기 신뢰 손상이 크고, 네이버 알고리즘이 패턴을 식별합니다.",
            ],
            related=[
                ("신규 매장 네이버 플레이스 등록 첫 4주 운영 가이드", "/insights/local-seo/new-store-naver-place/", "지역 SEO"),
                ("디지털 PR과 자연 백링크 — Disavow 결정 기준", "/insights/backlink-pr/disavow-decision/", "디지털 PR"),
                ("지역 SEO 서비스", "/services/local-seo/", "서비스"),
            ]
        ),
        "json_ld": blog_jsonld(
            url="https://onesearchpro.org/insights/local-seo/negative-review-response-mistakes/",
            title="네이버 플레이스 부정 리뷰 대응 — 자주 하는 실수 5가지",
            desc="네이버 플레이스 부정 리뷰의 5가지 흔한 대응 실수와 잠재 고객 신뢰를 유지하는 4단계 응답 프로세스.",
            date_published="2026-05-17"
        ),
        "active": "insights",
    },

    # ===== AUTO-INSERT MARKER (weekly_blog.py inserts new articles above) =====

    "/sitemap-html/": {
        "title": "사이트맵 | 전체 페이지 목록 | OneSearchPro",
        "desc": "OneSearchPro 사이트의 전체 페이지 목록입니다. 서비스·성공사례·SEO 인사이트·회사소개 등 모든 페이지로 한 번에 이동할 수 있습니다.",
        "keywords": "사이트맵, OneSearchPro 사이트맵, 전체 페이지 목록",
        "h1": "사이트맵",
        "eyebrow": "SITEMAP",
        "lead": "OneSearchPro 사이트의 전체 페이지를 한 페이지에 모았습니다. 검색엔진용 XML 사이트맵은 /sitemap.xml, RSS 피드는 /rss.xml 에 있습니다.",
        "body": (
            '<section class="section"><div class="container">'
            '<div class="sitemap-grid">'

            '<div class="sitemap-col">'
            '<h2>메인</h2>'
            '<ul><li><a href="/">홈</a></li></ul>'
            '</div>'

            '<div class="sitemap-col">'
            '<h2>SEO 서비스</h2>'
            '<ul>'
            '<li><a href="/services/seo/">SEO 컨설팅</a></li>'
            '<li><a href="/services/technical-seo/">기술 SEO 진단</a></li>'
            '<li><a href="/services/content-seo/">콘텐츠 SEO</a></li>'
            '<li><a href="/services/local-seo/">지역 SEO</a></li>'
            '<li><a href="/services/digital-pr/">디지털 PR · 백링크 진단</a></li>'
            '<li><a href="/services/social-media/">SNS 마케팅</a></li>'
            '<li><a href="/services/web-design/">SEO 웹사이트 제작</a></li>'
            '</ul>'
            '</div>'

            '<div class="sitemap-col">'
            '<h2>성공사례</h2>'
            '<ul>'
            '<li><a href="/case-studies/">성공사례 허브</a></li>'
            '<li><a href="/case-studies/seo/">SEO 개선 사례</a></li>'
            '<li><a href="/case-studies/local-seo/">지역 SEO 사례</a></li>'
            '<li><a href="/case-studies/content/">콘텐츠 개선 사례</a></li>'
            '<li><a href="/case-studies/web-design/">웹사이트 제작 사례</a></li>'
            '<li><a href="/case-studies/visibility/">검색 노출 문제 해결 사례</a></li>'
            '</ul>'
            '</div>'

            '<div class="sitemap-col">'
            '<h2>SEO 인사이트 — 카테고리</h2>'
            '<ul>'
            '<li><a href="/insights/">전체 인사이트</a></li>'
            '<li><a href="/insights/google-seo/">구글 SEO</a></li>'
            '<li><a href="/insights/technical-seo/">기술 SEO</a></li>'
            '<li><a href="/insights/content-seo/">콘텐츠 SEO</a></li>'
            '<li><a href="/insights/local-seo/">지역 SEO</a></li>'
            '<li><a href="/insights/backlink-pr/">백링크 · 디지털 PR</a></li>'
            '<li><a href="/insights/sns/">SNS 마케팅</a></li>'
            '<li><a href="/insights/visibility/">검색 노출 문제 해결</a></li>'
            '</ul>'
            '</div>'

            '<div class="sitemap-col">'
            '<h2>인사이트 글 — 구글 SEO</h2>'
            '<ul>'
            '<li><a href="/insights/google-seo/post-core-update-mistakes/">코어 업데이트 직후 SEO 주의사항 5가지</a></li>'
            '<li><a href="/insights/google-seo/helpful-content-self-check/">Helpful Content System 셀프 점검 7가지</a></li>'
            '<li><a href="/insights/google-seo/first-month-priorities/">신규 사이트 첫 1개월 SEO 우선순위 5가지</a></li>'
            '</ul>'
            '</div>'

            '<div class="sitemap-col">'
            '<h2>인사이트 글 — 기술 SEO</h2>'
            '<ul>'
            '<li><a href="/insights/technical-seo/discovered-not-indexed/">"발견됨 - 색인되지 않음" 원인 7가지</a></li>'
            '<li><a href="/insights/technical-seo/wordpress-lcp-fix/">워드프레스 LCP 개선 작업 순서</a></li>'
            '<li><a href="/insights/technical-seo/mobile-first-indexing/">모바일 우선 색인 점검 가이드</a></li>'
            '</ul>'
            '</div>'

            '<div class="sitemap-col">'
            '<h2>인사이트 글 — 콘텐츠 SEO</h2>'
            '<ul>'
            '<li><a href="/insights/content-seo/medical-blog-first-100/">병원·치과 블로그 첫 100자 작성법</a></li>'
            '<li><a href="/insights/content-seo/product-page-content-structure/">쇼핑몰 제품 페이지 본문 6단락 구조</a></li>'
            '<li><a href="/insights/content-seo/search-intent-4-types-keyword-classification-page-strategy/">검색 의도 4가지 유형과 키워드 분류</a></li>'
            '</ul>'
            '</div>'

            '<div class="sitemap-col">'
            '<h2>인사이트 글 — 지역 SEO</h2>'
            '<ul>'
            '<li><a href="/insights/local-seo/new-store-naver-place/">신규 매장 네이버 플레이스 3개월 운영</a></li>'
            '<li><a href="/insights/local-seo/multi-location-gbp/">다지점 매장 GBP 본사·지점 분리 원칙</a></li>'
            '</ul>'
            '</div>'

            '<div class="sitemap-col">'
            '<h2>인사이트 글 — 백링크 · 디지털 PR</h2>'
            '<ul>'
            '<li><a href="/insights/backlink-pr/disavow-decision/">위험한 백링크 Disavow 결정 기준</a></li>'
            '<li><a href="/insights/backlink-pr/korean-press-release/">한국 언론사 보도자료 백링크 구분법</a></li>'
            '</ul>'
            '</div>'

            '<div class="sitemap-col">'
            '<h2>인사이트 글 — SNS 마케팅</h2>'
            '<ul>'
            '<li><a href="/insights/sns/youtube-shorts-description/">유튜브 쇼츠 설명란 트래픽 유도법</a></li>'
            '<li><a href="/insights/sns/instagram-link-in-bio/">인스타그램 프로필 링크 SEO 비교</a></li>'
            '</ul>'
            '</div>'

            '<div class="sitemap-col">'
            '<h2>인사이트 글 — 검색 노출 문제 해결</h2>'
            '<ul>'
            '<li><a href="/insights/visibility/301-migration-mistakes/">사이트 리뉴얼 301 매핑 실수 12가지</a></li>'
            '<li><a href="/insights/visibility/crawled-not-indexed/">"크롤링됨 - 색인되지 않음" 대응법</a></li>'
            '</ul>'
            '</div>'

            '<div class="sitemap-col">'
            '<h2>회사소개</h2>'
            '<ul>'
            '<li><a href="/about/">회사 소개</a></li>'
            '<li><a href="/about/principles/">운영 원칙</a></li>'
            '<li><a href="/about/process/">작업 프로세스</a></li>'
            '<li><a href="/about/faq/">자주 묻는 질문</a></li>'
            '</ul>'
            '</div>'

            '<div class="sitemap-col">'
            '<h2>기타</h2>'
            '<ul>'
            '<li><a href="/contact/">내 사이트 진단받기</a></li>'
            '<li><a href="/privacy/">개인정보처리방침</a></li>'
            '<li><a href="/terms/">이용약관</a></li>'
            '</ul>'
            '</div>'

            '<div class="sitemap-col">'
            '<h2>검색엔진용 피드</h2>'
            '<ul>'
            '<li><a href="/sitemap.xml">XML 사이트맵 (검색엔진용)</a></li>'
            '<li><a href="/rss.xml">RSS 피드 (인사이트 구독)</a></li>'
            '<li><a href="/robots.txt">robots.txt</a></li>'
            '</ul>'
            '</div>'

            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","name":"사이트맵","url":"https://onesearchpro.org/sitemap-html/","inLanguage":"ko-KR"}</script>',
        "active": "",
    },

    "/privacy/": {
        "title": "개인정보처리방침 | OneSearchPro",
        "desc": "OneSearchPro(YH기획)의 개인정보 수집·이용·보관·파기 및 정보주체 권리에 관한 처리방침입니다. 개인정보보호법(PIPA) 준수.",
        "keywords": "개인정보처리방침, 개인정보보호, PIPA, OneSearchPro, YH기획",
        "h1": "개인정보처리방침",
        "eyebrow": "PRIVACY POLICY",
        "lead": "YH기획(이하 \"회사\")은 정보주체의 개인정보를 중요시하며, 개인정보보호법 등 관련 법령을 준수하기 위해 노력합니다. 본 처리방침은 회사가 운영하는 OneSearchPro 사이트의 개인정보 처리 기준을 안내합니다.",
        "body": (
            '<section class="section"><div class="container">'
            '<div class="legal-doc">'
            '<h2>1. 개인정보의 처리 목적</h2>'
            '<p>회사는 다음의 목적을 위하여 개인정보를 처리합니다. 처리 목적이 변경되는 경우에는 개인정보보호법 제18조에 따라 별도 동의를 받는 등 필요한 조치를 이행합니다.</p>'
            '<ul>'
            '<li>서비스 문의·상담·견적 응대</li>'
            '<li>무료 SEO 진단 리포트 제공</li>'
            '<li>마케팅·계약 관련 사항 안내</li>'
            '<li>법령 및 회사 정책에 따른 의무 이행</li>'
            '</ul>'
            '<h2>2. 처리하는 개인정보 항목</h2>'
            '<p>회사는 다음의 개인정보 항목을 수집할 수 있습니다.</p>'
            '<ul>'
            '<li><b>필수 항목</b>: 이름, 이메일, 회사명, 문의 내용</li>'
            '<li><b>선택 항목</b>: 웹사이트 URL, 전화번호, 텔레그램 ID</li>'
            '<li><b>자동 수집 항목</b>: 접속 IP, 쿠키, 접속 로그, 서비스 이용 기록 (GA4·서치콘솔 등을 통해)</li>'
            '</ul>'
            '<h2>3. 개인정보의 보유 및 이용 기간</h2>'
            '<p>회사는 정보주체로부터 개인정보를 수집할 때 동의받은 보유·이용기간 또는 법령에 따른 보유·이용 기간 내에서 개인정보를 처리·보유합니다.</p>'
            '<ul>'
            '<li>문의·상담 기록: 처리 완료 후 3년 (전자상거래법)</li>'
            '<li>계약 또는 청약철회 기록: 5년</li>'
            '<li>대금결제 및 재화 등의 공급에 관한 기록: 5년</li>'
            '<li>마케팅 활용 동의 기록: 동의 철회 시까지</li>'
            '</ul>'
            '<h2>4. 개인정보의 제3자 제공</h2>'
            '<p>회사는 원칙적으로 정보주체의 개인정보를 외부에 제공하지 않습니다. 다만 다음의 경우에는 예외로 합니다.</p>'
            '<ul>'
            '<li>정보주체가 사전에 동의한 경우</li>'
            '<li>법령의 규정에 의거하거나 수사 목적으로 법령에 정해진 절차와 방법에 따라 수사기관의 요구가 있는 경우</li>'
            '</ul>'
            '<h2>5. 개인정보 처리의 위탁</h2>'
            '<p>회사는 원활한 서비스 운영을 위해 다음과 같이 일부 업무를 위탁할 수 있습니다.</p>'
            '<ul>'
            '<li>웹 호스팅: Cloudflare (서비스 인프라 운영)</li>'
            '<li>분석 도구: Google Analytics 4 (서비스 이용 통계 분석)</li>'
            '<li>커뮤니케이션: Telegram (문의 응대)</li>'
            '</ul>'
            '<h2>6. 정보주체의 권리</h2>'
            '<p>정보주체는 회사에 대해 언제든지 다음의 권리를 행사할 수 있습니다.</p>'
            '<ul>'
            '<li>개인정보 열람 요구</li>'
            '<li>오류 정정 요구</li>'
            '<li>삭제 요구</li>'
            '<li>처리정지 요구</li>'
            '</ul>'
            '<p>위 권리 행사는 회사에 대해 서면, 이메일을 통하여 하실 수 있으며 회사는 이에 대해 지체 없이 조치합니다.</p>'
            '<h2>7. 개인정보의 안전성 확보 조치</h2>'
            '<ul>'
            '<li><b>관리적 조치</b>: 내부관리계획 수립·시행, 정기적 직원 교육</li>'
            '<li><b>기술적 조치</b>: 개인정보처리시스템 등의 접근권한 관리, 접근통제시스템 설치, 고유식별정보 등의 암호화, 보안프로그램 설치</li>'
            '<li><b>물리적 조치</b>: 전산실, 자료보관실 등의 접근통제</li>'
            '</ul>'
            '<h2>8. 쿠키 사용에 관한 사항</h2>'
            '<p>회사는 이용자에게 맞춤형 서비스를 제공하기 위해 쿠키를 사용할 수 있습니다. 이용자는 웹브라우저 옵션에서 쿠키 저장을 거부할 수 있으나, 거부 시 일부 서비스 이용에 제한이 있을 수 있습니다.</p>'
            '<h2>9. 개인정보 보호책임자</h2>'
            '<p>회사는 개인정보 처리에 관한 업무를 총괄해서 책임지고, 개인정보 처리와 관련한 정보주체의 불만 처리 및 피해 구제 등을 위하여 아래와 같이 개인정보 보호책임자를 지정하고 있습니다.</p>'
            '<ul>'
            '<li><b>책임자</b>: YH기획 운영자</li>'
            '<li><b>연락처</b>: contact@onesearchpro.com</li>'
            '</ul>'
            '<h2>10. 권익침해 구제방법</h2>'
            '<p>정보주체는 개인정보침해로 인한 구제를 받기 위하여 개인정보분쟁조정위원회, 한국인터넷진흥원 개인정보침해신고센터 등에 분쟁해결이나 상담 등을 신청할 수 있습니다.</p>'
            '<ul>'
            '<li>개인정보분쟁조정위원회: 1833-6972 (www.kopico.go.kr)</li>'
            '<li>개인정보침해신고센터: 118 (privacy.kisa.or.kr)</li>'
            '<li>대검찰청: 1301 (www.spo.go.kr)</li>'
            '<li>경찰청: 182 (ecrm.cyber.go.kr)</li>'
            '</ul>'
            '<h2>11. 개인정보 처리방침 변경</h2>'
            '<p>이 개인정보처리방침은 시행일로부터 적용되며, 법령 및 방침에 따른 변경내용의 추가, 삭제 및 정정이 있는 경우에는 변경사항의 시행 7일 전부터 공지사항을 통하여 고지할 것입니다.</p>'
            '<p><b>시행일자: 2025-05-14</b></p>'
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","name":"개인정보처리방침","url":"https://onesearchpro.org/privacy/","inLanguage":"ko-KR"}</script>',
        "active": "",
    },

    "/terms/": {
        "title": "이용약관 | OneSearchPro",
        "desc": "OneSearchPro(YH기획) 서비스 이용약관입니다. 서비스 이용 조건, 회원 의무, 책임 한계, 면책 조항 등 서비스 이용에 관한 기본 사항을 정합니다.",
        "keywords": "이용약관, 서비스 약관, OneSearchPro, YH기획",
        "h1": "이용약관",
        "eyebrow": "TERMS OF SERVICE",
        "lead": "본 이용약관은 YH기획(이하 \"회사\")이 운영하는 OneSearchPro 사이트 및 관련 서비스 이용에 관한 기본 사항을 정합니다.",
        "body": (
            '<section class="section"><div class="container">'
            '<div class="legal-doc">'
            '<h2>제1조 (목적)</h2>'
            '<p>본 약관은 YH기획(이하 "회사")이 운영하는 OneSearchPro 웹사이트 및 관련 SEO·디지털 마케팅 서비스(이하 "서비스") 이용에 관한 회사와 이용자 간의 권리·의무 및 책임사항을 규정함을 목적으로 합니다.</p>'
            '<h2>제2조 (용어의 정의)</h2>'
            '<ul>'
            '<li><b>"서비스"</b>: 회사가 제공하는 SEO 컨설팅, 기술 SEO 진단, 콘텐츠 SEO, 지역 SEO, 디지털 PR·백링크 진단, SNS 마케팅, SEO 웹사이트 제작 등 일체의 마케팅 관련 서비스를 의미합니다.</li>'
            '<li><b>"이용자"</b>: 본 약관에 따라 회사가 제공하는 서비스를 이용하는 개인 또는 법인을 의미합니다.</li>'
            '<li><b>"콘텐츠"</b>: 회사가 사이트 및 서비스 제공 과정에서 제공하는 모든 텍스트·이미지·동영상·자료를 의미합니다.</li>'
            '</ul>'
            '<h2>제3조 (약관의 효력 및 변경)</h2>'
            '<p>1. 본 약관은 회사 사이트에 게시함으로써 효력을 발생합니다.</p>'
            '<p>2. 회사는 관련 법령에 위배되지 않는 범위에서 본 약관을 변경할 수 있으며, 변경된 약관은 시행일로부터 7일 전에 사이트에 공지합니다.</p>'
            '<p>3. 이용자가 변경된 약관에 동의하지 않는 경우, 이용자는 서비스 이용을 중단하고 회사에 통보할 수 있습니다.</p>'
            '<h2>제4조 (서비스의 제공)</h2>'
            '<p>회사가 제공하는 서비스의 구체적 범위·내용·기간은 별도의 계약서 또는 견적서에 명시합니다.</p>'
            '<h2>제5조 (서비스 이용 신청)</h2>'
            '<p>1. 서비스 이용을 희망하는 이용자는 회사가 정한 방법에 따라 문의를 신청하고, 회사와 별도 계약을 체결한 후 서비스를 이용할 수 있습니다.</p>'
            '<p>2. 회사는 다음 각 호에 해당하는 신청에 대하여는 승낙하지 않거나 사후에 이용계약을 해지할 수 있습니다.</p>'
            '<ul>'
            '<li>허위 정보를 기재한 경우</li>'
            '<li>구글·네이버 등 검색엔진 가이드라인 위반을 요청하는 경우</li>'
            '<li>법령 또는 공서양속에 위반되는 목적의 서비스를 요청하는 경우</li>'
            '<li>기타 회사가 정한 이용신청 요건이 미비된 경우</li>'
            '</ul>'
            '<h2>제6조 (회사의 의무)</h2>'
            '<p>1. 회사는 관련 법령과 본 약관이 금지하거나 공서양속에 반하는 행위를 하지 않으며, 안정적인 서비스 제공을 위해 최선을 다합니다.</p>'
            '<p>2. 회사는 이용자의 개인정보 보호를 위해 보안시스템을 갖추고 개인정보처리방침을 공시하고 준수합니다.</p>'
            '<p>3. 회사는 화이트햇(White-hat) 방식으로만 서비스를 제공하며, 검색엔진의 가이드라인을 준수합니다.</p>'
            '<h2>제7조 (이용자의 의무)</h2>'
            '<ul>'
            '<li>회사가 제공하는 서비스 이용에 필요한 정보를 진실하게 제공해야 합니다.</li>'
            '<li>회사 또는 제3자의 권리를 침해하지 않아야 합니다.</li>'
            '<li>서비스 결과물(콘텐츠·전략 보고서 등)을 제3자에게 무단 양도·재판매하지 않아야 합니다.</li>'
            '<li>법령 또는 검색엔진 가이드라인을 위반하는 작업을 회사에 요구하지 않아야 합니다.</li>'
            '</ul>'
            '<h2>제8조 (서비스 결과에 관한 사항)</h2>'
            '<p>1. SEO 서비스의 특성상 검색엔진 알고리즘은 회사의 통제를 벗어난 영역이며, 회사는 특정 순위·특정 키워드 노출을 보장하지 않습니다.</p>'
            '<p>2. 회사는 작업 진행 상황·결과를 월간 리포트를 통해 투명하게 공개합니다.</p>'
            '<p>3. 검색엔진 알고리즘 변경, 경쟁 환경 변화, 이용자 사이트의 외부 요인 등으로 인한 결과 변동에 대해 회사는 책임을 지지 않습니다.</p>'
            '<h2>제9조 (지적재산권)</h2>'
            '<p>1. 회사가 제공하는 사이트의 콘텐츠(글·이미지·코드 등)에 대한 저작권은 회사에 귀속됩니다.</p>'
            '<p>2. 이용자와의 계약에 따라 제작된 결과물의 저작권 귀속은 별도 계약서에 따릅니다.</p>'
            '<h2>제10조 (면책조항)</h2>'
            '<p>1. 회사는 천재지변, 전쟁, 기간통신사업자의 서비스 중지, 검색엔진의 정책 변경 등 회사의 합리적 통제를 벗어난 사유로 인한 서비스 제공 지연·중단에 대해 책임을 지지 않습니다.</p>'
            '<p>2. 회사는 이용자의 귀책사유로 인한 서비스 이용 장애에 대해 책임을 지지 않습니다.</p>'
            '<h2>제11조 (분쟁 해결)</h2>'
            '<p>본 약관에 관하여 분쟁이 발생할 경우, 양 당사자는 우선 상호 협의로 해결하기 위해 노력합니다. 협의가 이루어지지 않을 경우 회사의 본사 소재지 관할 법원을 1심 관할 법원으로 합니다.</p>'
            '<h2>제12조 (준거법)</h2>'
            '<p>본 약관에 명시되지 않은 사항은 대한민국 법령 및 상관례에 따릅니다.</p>'
            '<p><b>시행일자: 2025-05-14</b></p>'
            '</div></div></section>'
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","name":"이용약관","url":"https://onesearchpro.org/terms/","inLanguage":"ko-KR"}</script>',
        "active": "",
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

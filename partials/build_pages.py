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
<body>
  {header}
  {breadcrumb_html}
  <main>
    <section class="page-hero">
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
    </section>
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
        f'<div class="svc-icon">📝</div>'
        f'<h3>{title}</h3>'
        f'<p>{summary}</p>'
        f'</div>'
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
                    insight_card("구글 SEO 처음 시작할 때 가장 먼저 봐야 할 5가지", "신규 사이트 운영자가 첫 달에 점검해야 할 색인·서치콘솔·메타·내부 링크·핵심 키워드 점검 항목을 정리한 입문 가이드."),
                    insight_card("E-E-A-T란 무엇이고 왜 점점 중요해지는가", "Experience·Expertise·Authoritativeness·Trustworthiness 4가지 신호를 사이트 안에 자연스럽게 녹이는 구체적인 방법."),
                    insight_card("구글 코어 업데이트가 발표됐을 때의 대응 체크리스트", "트래픽 변동이 발생했을 때 \"패닉 작업\" 대신 사용해야 하는 진단 순서와 4주간의 관찰 가이드."),
                    insight_card("검색 의도 4가지 유형과 콘텐츠 매칭 전략", "정보형·내비게이션형·상업형·트랜잭션형 의도에 맞는 페이지 유형과 헤딩 구조 가이드.")
                ]
            ) +

            insights_section("technical-seo", "TECHNICAL SEO", "기술 SEO",
                "색인·속도·구조화 데이터·중복 URL 등 기술 요소에 대한 실무 가이드입니다.",
                [
                    insight_card("페이지가 색인되지 않을 때 확인할 8가지 항목", "robots.txt, noindex, canonical, 크롤링 예산, JavaScript 렌더링 등 색인 실패 원인 진단 순서."),
                    insight_card("Core Web Vitals 점수를 90점 이상으로 끌어올리는 실무 체크리스트", "LCP·INP·CLS 개선을 위한 이미지·CSS·JS·서버 측 작업 가이드."),
                    insight_card("canonical 태그, 언제 어떻게 써야 하나", "파라미터·페이지네이션·다국어·복제 콘텐츠 상황별 canonical 설정 가이드."),
                    insight_card("sitemap.xml 설계 — 큰 사이트는 어떻게 분리해야 하나", "다중 sitemap, 이미지/뉴스/비디오 sitemap, sitemap 인덱스 활용 가이드.")
                ]
            ) +

            insights_section("content-seo", "CONTENT SEO", "콘텐츠 SEO",
                "키워드 설계·H태그·검색 의도·콘텐츠 클러스터링·리프레시 전략을 다룹니다.",
                [
                    insight_card("키워드 리서치 — 검색량이 아니라 의도로 분류하는 방법", "검색량 중심 키워드 시트의 한계와 의도 중심 키워드 매핑으로 바꾸는 단계별 가이드."),
                    insight_card("H1·H2·H3 헤딩 구조, SEO에 실제로 얼마나 영향을 주는가", "헤딩 태그의 역할과 자주 하는 실수, 검색 결과 스니펫에 미치는 영향 정리."),
                    insight_card("토픽 클러스터로 토픽 권위(Topical Authority)를 만드는 방법", "필러 콘텐츠 1개 + 클러스터 6~12개의 구조 설계와 내부 링크 흐름 가이드."),
                    insight_card("오래된 글 리프레시 — 새 글보다 효과가 큰 이유", "트래픽 잠재력이 높은 글을 선별하는 기준과 리프레시 작업 순서, 측정 방법.")
                ]
            ) +

            insights_section("local-seo", "LOCAL SEO", "지역 SEO",
                "구글 비즈니스 프로필·네이버 플레이스·지역 랜딩페이지·NAP 일관성 가이드입니다.",
                [
                    insight_card("구글 비즈니스 프로필(GBP) 최적화 체크리스트", "카테고리·서비스·사진·리뷰·게시물 관리에서 자주 빠뜨리는 항목."),
                    insight_card("네이버 플레이스 상위 노출에 영향을 주는 신호들", "스마트플레이스 정보·블로그 연동·영수증 리뷰·톡톡 응대의 우선순위 정리."),
                    insight_card("\"지역명 + 서비스\" 키워드용 지역 랜딩페이지 설계법", "다지점 비즈니스에서 지역 키워드를 잡기 위한 페이지 구조와 콘텐츠 작성 가이드."),
                    insight_card("NAP 일관성과 로컬 인용(citation)이 왜 중요한가", "디렉토리·SNS·자체 사이트의 상호·주소·전화 정보 통일 가이드.")
                ]
            ) +

            insights_section("backlink-pr", "BACKLINK & DIGITAL PR", "백링크 · 디지털 PR",
                "안전한 외부 신호 확보, 백링크 리스크 진단, 디지털 PR 전략을 다룹니다.",
                [
                    insight_card("위험한 백링크를 식별하는 7가지 지표", "Toxic Score·앵커 분포·발신 사이트 품질·언어·지역 시그널 등 점검 항목."),
                    insight_card("Google Disavow 도구 — 언제 써야 하고 언제 쓰지 말아야 하나", "Disavow의 실제 효과와 잘못된 사용으로 인한 위험, 단계적 의사결정 가이드."),
                    insight_card("게스트 포스트와 디지털 PR의 차이", "스팸과 합법적 PR을 가르는 기준, 자연스러운 신뢰 링크 확보 전략."),
                    insight_card("브랜드 언급(unlinked mention)을 링크로 전환하는 방법", "언급 모니터링 도구 활용과 정중한 컨택 템플릿, 전환율 높이는 팁.")
                ]
            ) +

            insights_section("sns", "SNS MARKETING", "SNS 마케팅",
                "인스타그램·유튜브·틱톡·네이버 채널 운영과 SEO 보조 역할에 대한 가이드입니다.",
                [
                    insight_card("SNS는 SEO에 직접 영향을 주는가 — 통념과 사실", "소셜 신호와 검색 순위의 실제 관계, 간접적으로 작용하는 경로 정리."),
                    insight_card("유튜브 SEO 기본 — 제목·설명·태그·썸네일의 우선순위", "유튜브 알고리즘이 평가하는 요소와 콘텐츠 갱신 주기 가이드."),
                    insight_card("인스타그램 검색 탭과 구글 인덱싱 — 활용 포인트", "프로필·릴스·해시태그를 어떻게 검색 자산으로 만들 수 있는지에 대한 실무 가이드.")
                ]
            ) +

            insights_section("visibility", "VISIBILITY", "검색 노출 문제 해결",
                "색인·페널티·중복·트래픽 급락 등 \"검색 노출이 안 될 때\" 진단 가이드입니다.",
                [
                    insight_card("트래픽이 갑자기 떨어졌을 때 4주 진단 매뉴얼", "코어 업데이트·알고리즘 변경·사이트 문제·계절성을 구분하는 진단 순서."),
                    insight_card("색인 누락 원인 7가지와 단계별 진단 방법", "Crawl·Render·Index 3단계에서 일어날 수 있는 실패 패턴 분류."),
                    insight_card("\"수동 조치(manual action)\" 메시지를 받았을 때 대응 가이드", "서치콘솔에서 메시지를 받은 경우 단계별 점검 항목과 재심사 요청 절차."),
                    insight_card("중복 콘텐츠 문제 — canonical, 301, noindex 중 어떤 걸 써야 하나", "상황별 의사결정 트리와 실제 사례 기반 가이드.")
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

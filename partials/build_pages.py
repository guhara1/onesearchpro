#!/usr/bin/env python3
"""Generate remaining service & company pages from a shared template."""
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
SITE = "https://onesearchpro.pages.dev"

HEADER = '''<header class="site-header">
    <div class="container nav-wrap">
      <a href="/" class="brand"><span class="brand-mark">1</span><span class="brand-name">OneSearch<strong>Pro</strong></span></a>
      <nav class="nav" id="nav">
        <div class="has-dropdown">
          <a href="/services/backlink/" class="nav-trigger{ACTIVE_SVC}">서비스 <span class="caret">▾</span></a>
          <div class="dropdown">
            <a href="/services/backlink/" class="dd-main"><b>🔗 백링크 서비스</b><span>메인 서비스</span></a>
            <a href="/services/seo/">검색엔진최적화 (SEO)</a>
            <a href="/services/local-seo/">지역 SEO (Local SEO)</a>
            <a href="/services/social-media/">소셜 미디어 마케팅</a>
            <a href="/services/corporate-marketing/">기업 마케팅</a>
            <a href="/services/web-design/">웹사이트 제작</a>
            <a href="/services/malaysia/">말레이시아 마케팅</a>
          </div>
        </div>
        <a href="/about/"{ACTIVE_ABOUT}>회사소개</a>
        <a href="/contact/" class="btn btn-ghost">문의하기</a>
      </nav>
      <button class="nav-toggle" id="navToggle" aria-label="메뉴 열기"><span></span><span></span><span></span></button>
    </div>
  </header>'''

FOOTER = '''<footer class="site-footer">
    <div class="container foot-grid">
      <div><a href="/" class="brand"><span class="brand-mark">1</span><span class="brand-name">OneSearch<strong>Pro</strong></span></a><p class="muted">검색에서 시작되는 비즈니스 성장.<br/>백링크 · SEO · 글로벌 마케팅 전문 에이전시.</p></div>
      <div><h5>서비스</h5><ul><li><a href="/services/backlink/">백링크 서비스</a></li><li><a href="/services/seo/">검색엔진최적화</a></li><li><a href="/services/local-seo/">지역 SEO</a></li><li><a href="/services/social-media/">소셜 미디어 마케팅</a></li><li><a href="/services/corporate-marketing/">기업 마케팅</a></li><li><a href="/services/web-design/">웹사이트 제작</a></li><li><a href="/services/malaysia/">말레이시아 마케팅</a></li></ul></div>
      <div><h5>회사</h5><ul><li><a href="/about/">회사 소개</a></li><li><a href="/contact/">문의하기</a></li></ul></div>
      <div><h5>연락처</h5><ul><li>contact@onesearchpro.com</li><li>Seoul · Kuala Lumpur</li><li>KakaoTalk: @onesearchpro</li></ul></div>
    </div>
    <div class="container foot-bottom"><span>© <span id="year"></span> OneSearchPro. All rights reserved.</span><span>Made with ☕ in Seoul &amp; KL</span></div>
  </footer>'''


def page(*, path, title, desc, keywords, h1, eyebrow, lead, body, json_ld="", active="svc"):
    canonical = f"{SITE}{path}"
    active_svc = " active" if active == "svc" else ""
    active_about = ' class="active"' if active == "about" else ""
    header = HEADER.replace("{ACTIVE_SVC}", active_svc).replace("{ACTIVE_ABOUT}", active_about)
    breadcrumb_html = ""
    if path.startswith("/services/"):
        slug_title = h1
        breadcrumb_html = f'''<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <a href="/services/backlink/">서비스</a> <span>›</span> <span>{slug_title}</span></div></nav>'''
    elif path == "/about/":
        breadcrumb_html = '<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <span>회사 소개</span></div></nav>'
    elif path == "/contact/":
        breadcrumb_html = '<nav class="breadcrumb" aria-label="breadcrumb"><div class="container"><a href="/">홈</a> <span>›</span> <span>문의하기</span></div></nav>'

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
            <a href="/contact/" class="btn btn-primary">무료 진단 받기</a>
            <a href="/services/backlink/" class="btn btn-outline">메인: 백링크 서비스 →</a>
          </div>
        </div>
        <div class="page-hero-stats">
          <div><b>1,200+</b><span>구축 백링크</span></div>
          <div><b>180+</b><span>프로젝트</span></div>
          <div><b>97%</b><span>고객 재계약</span></div>
          <div><b>2</b><span>국가 거점</span></div>
        </div>
      </div>
    </section>
    {body}
    <section class="section section-cta">
      <div class="container cta-grid">
        <div><h2>무료 진단 후 정확한 견적을 받아보세요</h2><p>24시간 내 분석 리포트와 맞춤 제안서를 보내드립니다.</p></div>
        <div class="cta-actions"><a href="/contact/" class="btn btn-primary btn-lg">무료 진단 신청 →</a><a href="/services/backlink/" class="btn btn-outline btn-lg btn-light">백링크 서비스 보기</a></div>
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


PAGES = {
    "/services/seo/": {
        "title": "검색엔진최적화 SEO | 구글·네이버 통합 SEO - OneSearchPro",
        "desc": "OneSearchPro의 SEO 서비스는 키워드 리서치, 온페이지·테크니컬 SEO, 콘텐츠 전략, 백링크 빌딩을 통합한 풀스택 검색엔진최적화입니다. 구글과 네이버 동시 대응.",
        "keywords": "SEO, 검색엔진최적화, 구글 SEO, 네이버 SEO, 온페이지 SEO, 테크니컬 SEO, 키워드 리서치",
        "h1": "검색엔진최적화 (SEO)",
        "eyebrow": "SEARCH ENGINE OPTIMIZATION",
        "lead": "키워드 리서치부터 테크니컬 SEO, 콘텐츠 전략까지 — 구글과 네이버에서 동시에 상위 노출되는 통합 SEO를 제공합니다. 백링크 빌딩이 결합되어 효과가 배가됩니다.",
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
                    "한국·말레이시아 양국의 주요 지역 검색 채널을 통합 운영합니다.",
                    [
                        {"icon":"📍","h":"구글 비즈니스 프로필","p":"GBP 최적화, 카테고리·서비스·사진·게시물 운영, 리뷰 응대.","li":["카테고리·속성 최적화","주간 게시물 운영"]},
                        {"icon":"🗺️","h":"네이버 플레이스","p":"플레이스 정보 최적화, 영수증 리뷰 유도, 톡톡 응대, 스마트플레이스 광고 연계.","li":["블로그·플레이스 연동","리뷰 이벤트 설계"]},
                        {"icon":"📚","h":"지역 디렉토리","p":"한국·말레이시아 주요 비즈니스 디렉토리 등록과 NAP 정보 일관성 관리.","li":["NAP 일관성","로컬 인용(citation)"]},
                        {"icon":"⭐","h":"리뷰 관리","p":"긍정 리뷰 유도 시스템, 부정 리뷰 대응 매뉴얼, 평점 관리.","li":["리뷰 응대 SLA","위기 대응 가이드"]},
                    ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","serviceType":"Local SEO","provider":{"@type":"Organization","name":"OneSearchPro"}}</script>',
    },

    "/services/social-media/": {
        "title": "소셜 미디어 마케팅 | 인스타·페이스북·틱톡·유튜브 - OneSearchPro",
        "desc": "OneSearchPro의 소셜 미디어 마케팅은 인스타그램, 페이스북, 틱톡, 유튜브 등 채널별 맞춤 콘텐츠 기획·제작·광고 운영을 제공합니다.",
        "keywords": "소셜미디어마케팅, SNS마케팅, 인스타그램마케팅, 페이스북광고, 틱톡마케팅, 유튜브마케팅",
        "h1": "소셜 미디어 마케팅",
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
        "title": "웹사이트 제작 | SEO 최적화 반응형 웹사이트 - OneSearchPro",
        "desc": "OneSearchPro의 웹사이트 제작은 SEO·속도·접근성에 최적화된 반응형 웹사이트와 랜딩페이지를 제공합니다. 워드프레스·코드형 모두 가능.",
        "keywords": "웹사이트제작, 홈페이지제작, 랜딩페이지제작, 워드프레스, SEO 최적화 웹사이트, 반응형 웹사이트",
        "h1": "웹사이트 제작",
        "eyebrow": "WEB DESIGN & DEVELOPMENT",
        "lead": "디자인만 예쁜 사이트가 아닌, 검색에 잘 잡히고 빠르게 로딩되며 전환이 잘 되는 웹사이트를 만듭니다. SEO 기초 공사가 끝난 상태로 납품됩니다.",
        "body": (
            section("TYPES", "제작 유형",
                    "프로젝트 성격에 맞는 기술 스택을 선택합니다.",
                    [
                        {"icon":"🏢","h":"기업 홈페이지","p":"브랜드 소개부터 다국어, 채용까지 — 표준 기업 사이트.","li":["다국어 (KR/EN/MY)","CMS 운영 페이지"]},
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

    "/services/malaysia/": {
        "title": "말레이시아 마케팅 | 한국 기업 동남아 진출 - OneSearchPro",
        "desc": "OneSearchPro의 말레이시아 마케팅은 BM/EN 다국어 콘텐츠, 현지 인플루언서·매체, .my 도메인 백링크, 쿠알라룸푸르 기반 네트워크를 활용한 동남아 진출 전문 서비스입니다.",
        "keywords": "말레이시아 마케팅, 동남아 진출, 말레이시아 SEO, 쿠알라룸푸르 마케팅, 동남아 인플루언서, BM 콘텐츠",
        "h1": "말레이시아 마케팅",
        "eyebrow": "🇲🇾 MALAYSIA MARKET",
        "lead": "한국 기업의 동남아 진출 첫 관문, 말레이시아. OneSearchPro는 쿠알라룸푸르에 거점을 두고 BM(말레이어)·영어·중국어 3언어 콘텐츠와 현지 미디어 네트워크를 운영합니다.",
        "body": (
            section("OFFERINGS", "말레이시아 진출 패키지",
                    "한 번에 시장 진입할 수 있도록 모든 영역을 통합합니다.",
                    [
                        {"icon":"🌐","h":".my 백링크 빌딩","p":"말레이시아 로컬 도메인(.my, .com.my) 백링크로 현지 검색 시그널 강화.","li":["DR 30+ 현지 매체","BM/EN 게스트 포스트"]},
                        {"icon":"📝","h":"다국어 콘텐츠","p":"말레이어(BM), 영어, 중국어 3개 언어로 콘텐츠 동시 제작.","li":["네이티브 카피라이터","문화 적합성 검수"]},
                        {"icon":"📱","h":"현지 SNS 운영","p":"Instagram MY, TikTok MY, Xiaohongshu 등 현지 채널 동시 운영.","li":["KL 인플루언서 협업","로컬 트렌드 반영"]},
                        {"icon":"🏪","h":"로컬 SEO","p":"Google Maps MY, Waze 등 말레이시아 지역 검색 최적화.","li":["GBP 운영","현지 디렉토리 등록"]},
                        {"icon":"🤝","h":"현지 파트너십","p":"KL·페낭·조호바루 등 주요 도시 미디어·에이전시 네트워크.","li":["언론사 PR","오프라인 이벤트 연계"]},
                        {"icon":"💼","h":"진출 컨설팅","p":"법인 설립부터 결제·물류 파트너 매칭까지 비즈니스 컨설팅 연계.","li":["MDEC·MITI 가이드","현지 사례 공유"]},
                    ]) +
            steps_section("PROCESS", "말레이시아 진출 프로세스", [
                ("시장 진단", "타겟 산업·세그먼트의 현지 경쟁 환경 분석."),
                ("로컬라이징", "브랜드 메시지·콘텐츠를 BM/EN/中으로 현지화."),
                ("진입 캠페인", "백링크 + SNS + 인플루언서 동시 런칭."),
                ("운영 & 확장", "쿠알라룸푸르·페낭 → 싱가포르·인도네시아 확장."),
            ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","serviceType":"Malaysia Marketing","provider":{"@type":"Organization","name":"OneSearchPro"},"areaServed":"MY"}</script>',
    },

    "/about/": {
        "title": "회사 소개 | OneSearchPro - 백링크 · SEO 전문 에이전시",
        "desc": "OneSearchPro는 서울과 쿠알라룸푸르에 거점을 둔 백링크·SEO·글로벌 마케팅 전문 에이전시입니다. 화이트햇 방식과 투명한 데이터로 180+ 프로젝트를 성공시켰습니다.",
        "keywords": "OneSearchPro, 원서치프로, 백링크 에이전시, SEO 에이전시, 마케팅 에이전시, 서울 쿠알라룸푸르",
        "h1": "About OneSearchPro",
        "eyebrow": "ABOUT US",
        "lead": "OneSearchPro는 검색에서 시작되는 비즈니스 성장을 만듭니다. 서울과 쿠알라룸푸르 두 도시에 거점을 두고, 한국 기업의 동남아 진출과 말레이시아 기업의 글로벌 확장을 함께합니다.",
        "body": (
            section("VALUES", "우리가 일하는 방식",
                    "에이전시의 가치는 결국 '신뢰'에서 나온다고 믿습니다.",
                    [
                        {"icon":"🤝","h":"투명함","p":"모든 백링크 URL, 광고 데이터, 비용 구조를 고객과 공유합니다."},
                        {"icon":"✅","h":"화이트햇","p":"단기 트릭이 아닌 구글 가이드라인을 지키는 정공법으로 일합니다."},
                        {"icon":"📊","h":"데이터 기반","p":"가설 → 실험 → 측정 → 개선의 사이클을 반복합니다."},
                        {"icon":"🌏","h":"글로벌 시야","p":"한국·말레이시아 양국의 문화와 시장을 이해합니다."},
                    ]) +
            section("WHAT WE DO", "주요 서비스",
                    "백링크를 중심으로 한 풀스택 디지털 마케팅.",
                    [
                        {"icon":"🔗","h":"백링크 서비스 (메인)","p":"DR 30~80+ 화이트햇 백링크 빌딩."},
                        {"icon":"🔍","h":"SEO / 지역 SEO","p":"구글·네이버 통합 검색엔진최적화."},
                        {"icon":"📱","h":"소셜 미디어","p":"인스타·페이스북·틱톡·유튜브 운영."},
                        {"icon":"💻","h":"웹사이트 제작","p":"SEO 최적화 반응형 웹사이트."},
                        {"icon":"🏢","h":"기업 마케팅","p":"브랜드 · 퍼포먼스 · CRM 통합."},
                        {"icon":"🇲🇾","h":"말레이시아 진출","p":"BM/EN 다국어 + 현지 네트워크."},
                    ])
        ),
        "json_ld": '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"OneSearchPro","url":"https://onesearchpro.pages.dev/about/","description":"백링크·SEO·글로벌 마케팅 전문 에이전시"}</script>',
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

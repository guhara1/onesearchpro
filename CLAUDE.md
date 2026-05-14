# CLAUDE.md — OneSearchPro 프로젝트 컨텍스트

> **이 파일은 Claude Code가 새 세션 시작 시 자동으로 읽습니다.** 사용자가 "이번 주 블로그 글 써줘" 같이 짧게 말해도 이 파일만 읽으면 전체 컨텍스트가 복원됩니다.

---

## 🎯 프로젝트 한 줄 요약

**YH기획**(사업자등록번호 503-30-66944)이 운영하는 SEO·디지털 마케팅 에이전시 브랜드 **OneSearchPro**의 마케팅 사이트. 도메인은 `onesearchpro.org` (Cloudflare Pages).

---

## 🌳 브랜치 전략 (중요)

| 브랜치 | 역할 |
|--------|------|
| `claude/help-coding-task-F0jMt` | 작업 브랜치 (Claude Code 기본 작업 분기) |
| `claude/onesearchpro-website-NFN2v` | **프로덕션 분기** (Cloudflare 연동, push 시 자동 배포) |

**모든 변경은 양쪽 브랜치에 모두 푸시**해야 라이브에 반영됩니다:

```bash
# 작업 분기에 작업·커밋 후
git push -u origin claude/help-coding-task-F0jMt

# 프로덕션 분기에 fast-forward 머지·푸시
git checkout claude/onesearchpro-website-NFN2v
git merge --ff-only claude/help-coding-task-F0jMt
git push -u origin claude/onesearchpro-website-NFN2v

# 작업 분기로 복귀
git checkout claude/help-coding-task-F0jMt
```

---

## 🏗️ 빌드 시스템

정적 사이트 생성기 — Python 스크립트가 HTML 페이지를 생성합니다.

- `partials/build_pages.py` — 메인 빌더. PAGES dict에서 페이지 정의를 읽어 HTML 출력
- `python3 partials/build_pages.py` 실행하면 전체 사이트 재생성
- 각 페이지는 `path → 메타 dict` 형태로 PAGES dict에 등록

### 핵심 헬퍼 함수 (build_pages.py 내부)
- `blog_post(date, reading_time, intro, sections, key_takeaways, related)` — 블로그 글 본문 HTML 생성
- `blog_jsonld(url, title, desc, date_published)` — BlogPosting JSON-LD 스키마 생성
- `insight_article_card(title, summary, url, reading_time)` — 카테고리 페이지의 글 카드
- `insight_card(title, summary)` — "준비 중" placeholder 카드
- `section(eyebrow, h2, p, cards)` — 서비스/about 페이지 카드 그리드
- `steps_section(eyebrow, h2, steps)` — 프로세스 단계 섹션

### AUTO-INSERT MARKER
`build_pages.py` PAGES dict 끝 부근에 `# ===== AUTO-INSERT MARKER ...` 코멘트 있음. 자동 발행 스크립트(`scripts/weekly_blog.py`)가 이 마커 앞에 새 블로그 entry를 삽입.

---

## 📝 매주 블로그 글 발행 워크플로우

**가장 자주 받는 요청**: "이번 주 블로그 글 써줘"

### 절대 규칙: CONTENT_CALENDAR.md를 먼저 읽기
이 파일에 발행 이력과 다음 주차 계획이 들어있음. 새 세션에서는 반드시 먼저 읽고 다음 미체크(`[ ]`) 주제 확인.

### 매주 발행 단계 (한 번에 실행)

1. `CONTENT_CALENDAR.md` 읽기 → 가장 위쪽의 `[ ]` 주제 찾기
2. 그 주제로 약 1,500~2,000자 분량의 블로그 글 작성:
   - 5~7개 H2 섹션 (각 200~400자)
   - intro 한 문단 (순수 텍스트, `<p>` 태그 금지)
   - 4개 정도의 `key_takeaways`
   - 3개의 `related` 링크 (같은 카테고리 1 + 다른 카테고리 1 + 서비스 페이지 1)
3. `partials/build_pages.py` PAGES dict에 새 entry 추가:
   - URL: `/insights/[카테고리-슬러그]/[글-슬러그]/`
   - 카테고리 슬러그: `google-seo`, `technical-seo`, `content-seo`, `local-seo`, `backlink-pr`, `sns`, `visibility`
   - `blog_post()` 헬퍼 사용
   - `blog_jsonld()` 헬퍼로 JSON-LD 생성
   - `"active": "insights"` 지정
4. 해당 카테고리 페이지(`/insights/[카테고리]/`)의 `insights_section` 카드 목록에 `insight_article_card()` 추가
5. `sitemap.xml`에 새 URL 추가 (`<url><loc>...</loc>...</url>`)
6. `CONTENT_CALENDAR.md`에서 해당 주차 `[ ]` → `[x]` 변경하고 URL·발행일 기록
7. `python3 partials/build_pages.py` 실행 → HTML 생성 확인
8. 양쪽 브랜치에 commit + push (위 브랜치 전략 참조)

---

## ✋ 블로그 글 작성 절대 규칙 (E-E-A-T 준수)

**SEO 에이전시 자기 블로그라 품질 미달 = 영업적 자살**. 다음을 절대 지킴:

| 금지 사항 | 이유 |
|----------|------|
| ❌ 검증 불가능한 구체 수치 (예: "92%가 일치", "전환율 3.2%→9.1%") | 거짓 통계 의심 → 신뢰 손상 |
| ❌ 익명 가공 사례 (예: "한 화장품 브랜드는...") | AI 양산 패턴 노출 |
| ❌ "보장", "확실", "100%", "반드시" | 구글 정책 위반·과장 광고 |
| ❌ 단순 인터넷 정보 재정리 | Helpful Content System 페널티 위험 |
| ❌ intro에 `<p>` 태그 (헬퍼가 자동으로 감쌈) | HTML 중첩 오류 |
| ❌ `<table>`에 인라인 style | CSS가 자동 스타일링함 |

| 권장 사항 | 효과 |
|----------|------|
| ✅ "자주 보이는 패턴", "실무 관찰상", "현장에서는" 같은 일반화 표현 | E-E-A-T Experience 신호 |
| ✅ 구체적 도구·플랫폼 이름 (네이버 서치어드바이저, Ahrefs, 서치콘솔 등) | 검증 가능한 사실 |
| ✅ 실패 사례·한계·예외 케이스 명시 | 정직한 신뢰 신호 |
| ✅ 한국 시장 맥락 (네이버 C-랭크·DIA, 카카오, 한국 광고 정책 등) | 차별성 |
| ✅ 다양한 문장 길이 혼용 | AI 양산 패턴 회피 |
| ✅ 단정 대신 관찰형 ("이 경우가 자주 보입니다") | 정직성 |

---

## 🗂️ 사이트 구조 개요

### 메뉴 (전체 페이지 공통)
```
로고 | 서비스 ▾ | 성공사례 ▾ | SEO 인사이트 ▾ | 회사소개 ▾ | 내 사이트 진단받기 (CTA)
```

### 서비스 (7개)
- `/services/seo/` (SEO 컨설팅 — 대표)
- `/services/technical-seo/` (기술 SEO 진단)
- `/services/content-seo/` (콘텐츠 SEO)
- `/services/local-seo/` (지역 SEO)
- `/services/digital-pr/` (디지털 PR·백링크 진단)
- `/services/social-media/` (SNS 마케팅)
- `/services/web-design/` (SEO 웹사이트 제작)

(`/services/backlink/`, `/services/corporate-marketing/`는 페이지만 존재, 메뉴 비노출)

### 성공사례 (1 허브 + 5 서브)
- `/case-studies/` (허브)
- `/case-studies/seo/`, `/local-seo/`, `/content/`, `/web-design/`, `/visibility/`

### SEO 인사이트 (1 허브 + 7 카테고리 + 글들)
- `/insights/` (허브)
- 카테고리 페이지: `google-seo`, `technical-seo`, `content-seo`, `local-seo`, `backlink-pr`, `sns`, `visibility`
- 카테고리 페이지마다 실제 발행된 글 카드(`insight_article_card`) + 예정 글 placeholder(`insight_card`)

### 회사소개 (1 메인 + 3 서브)
- `/about/` (원서치프로 소개 — 사업자 정보 섹션 포함)
- `/about/principles/`, `/about/process/`, `/about/faq/`

### 기타
- `/contact/` (문의 폼)
- `/` (메인 페이지, index.html — 손작성, build_pages.py와 별도)

### 손작성 페이지 (build_pages.py로 생성 안 됨)
- `index.html` (메인)
- `contact/index.html`
- `services/backlink/index.html`

→ 이들도 변경 시 같은 nav/footer 패턴 유지 필요. 사업자 정보 박스도 푸터에 있음.

---

## 🎨 디자인 시스템

- **테마**: 다크 + 보라(`#7c5cff`)·시안(`#22d3ee`)·인디고 그라데이션
- **로고**: `/assets/images/logo.png` (height 140px 데스크탑, 64px 모바일)
- **파비콘**: `/assets/images/favicon.svg` (SVG 그라데이션 + "1" 문자 + 시안 점)
- **헤더 nav 높이**: 170px (데스크탑), 96px (모바일)
- **블로그 글 전용 디자인**:
  - 상단 reading-progress 바 (스크롤 진행률)
  - 자동 H2 번호 (01, 02 ...)
  - 인트로 드롭캡
  - H2 그라데이션 텍스트 (흰색→바이올렛→시안)
  - 핵심 정리 박스, CTA 박스
  - 관련 글 카드

---

## 🏢 회사 정보 (전체 페이지 푸터 + /about/)

- **상호**: YH기획
- **브랜드**: OneSearchPro (원서치프로)
- **사업자등록번호**: 503-30-66944
- **주소**: 인천광역시 부평구 부평대로 283 부평우림라이온스밸리
- **이메일**: contact@onesearchpro.com
- **텔레그램**: https://t.me/googleseolab (전체 CTA 버튼이 여기로 새 창 열기)
- **카카오톡 채널**: @onesearchpro

---

## ⚙️ 자동화 시스템 (현재 비활성)

- `.github/workflows/weekly-blog.yml` — GitHub Actions 워크플로우
- `scripts/weekly_blog.py` — Claude API로 글 자동 생성 스크립트
- `ANTHROPIC_API_KEY` — GitHub Secrets에 등록됨
- **현재 cron 주석 처리되어 비활성**. 수동 트리거(`workflow_dispatch`)만 가능
- 활성화하려면 `weekly-blog.yml`의 `schedule:` 두 줄 주석 해제

**현재 운영 방식**: 자동화 대신 사용자가 매주 "이번 주 블로그 글 써줘" 요청 → Claude(이 세션)가 직접 작성·푸시.

---

## ⚡ Quick Start — 새 세션에서 "이번 주 블로그 글 써줘" 들으면

```
1. CONTENT_CALENDAR.md 읽기 → 가장 위 [ ] 주제 확인
2. 그 주제로 글 작성 (위 "절대 규칙" 준수)
3. partials/build_pages.py PAGES dict에 entry 추가
4. 카테고리 페이지에 insight_article_card 추가
5. sitemap.xml 갱신
6. CONTENT_CALENDAR.md 체크박스 업데이트
7. python3 partials/build_pages.py 실행
8. 양쪽 브랜치 commit + push
9. 사용자에게 URL 알려주기
```

---

## 📂 핵심 파일 위치

| 파일 | 역할 |
|------|------|
| `CLAUDE.md` (이 파일) | 프로젝트 컨텍스트 |
| `CONTENT_CALENDAR.md` | 블로그 발행 이력·계획 |
| `partials/build_pages.py` | 사이트 빌더 (모든 페이지 생성기) |
| `scripts/weekly_blog.py` | 자동 발행 스크립트 (현재 미사용) |
| `.github/workflows/weekly-blog.yml` | GitHub Actions 워크플로우 (비활성) |
| `index.html` | 메인 페이지 (손작성) |
| `styles.css` | 전체 디자인 시스템 |
| `script.js` | 인터랙션 (nav toggle, reading progress 등) |
| `sitemap.xml` | 사이트맵 (수동 갱신) |
| `robots.txt` | 크롤러 규칙 |
| `assets/images/logo.png` | 로고 |
| `assets/images/favicon.svg` | 파비콘 |

---

## 🔁 마지막 업데이트
2025-05-14 — 14편 초기 배치 + W1·W2 수동 발행 + W3 자동 발행 테스트(수정 완료). 자동 cron 비활성화.

# OneSearchPro 블로그 콘텐츠 캘린더

매주 1편 발행 원칙. 검수는 발행 후 진행.

다음 주 진행할 때 Claude에게 "이번 주 블로그 글 써줘"라고만 말씀하시면, 이 파일을 읽고 다음 차례를 자동으로 진행합니다.

---

## ✅ 초기 배치 (2025-05-14 일괄 발행, 14편)

- [x] `/insights/google-seo/post-core-update-mistakes/` — 구글 코어 업데이트 직후 2주, 절대 손대지 말아야 할 5가지
- [x] `/insights/google-seo/helpful-content-self-check/` — Helpful Content System 셀프 점검 7가지 질문
- [x] `/insights/technical-seo/discovered-not-indexed/` — 서치콘솔 "발견됨 - 색인되지 않음" 7가지 원인
- [x] `/insights/technical-seo/wordpress-lcp-fix/` — 워드프레스 LCP 4초→1.5초 작업 순서
- [x] `/insights/content-seo/medical-blog-first-100/` — 병원·치과 블로그 첫 100자
- [x] `/insights/content-seo/product-page-content-structure/` — 쇼핑몰 제품 페이지 6단락 구조
- [x] `/insights/local-seo/new-store-naver-place/` — 신규 매장 네이버 플레이스 첫 3개월
- [x] `/insights/local-seo/multi-location-gbp/` — 다지점 GBP 본사·지점 분리 원칙
- [x] `/insights/backlink-pr/disavow-decision/` — 이전 대행사 백링크 Disavow 결정
- [x] `/insights/backlink-pr/korean-press-release/` — 한국 보도자료 매체 구분
- [x] `/insights/sns/youtube-shorts-description/` — 유튜브 쇼츠 설명란 텍스트 구조
- [x] `/insights/sns/instagram-link-in-bio/` — 인스타 프로필 링크 SEO 비교
- [x] `/insights/visibility/301-migration-mistakes/` — 사이트 리뉴얼 301 매핑 12가지
- [x] `/insights/visibility/crawled-not-indexed/` — 서치콘솔 "크롤링됨 - 색인되지 않음"

---

## 📅 주간 발행 계획 (다음 13주, 카테고리 순환)

- [x] **W1 [구글 SEO]** 신규 사이트 첫 1개월 SEO 우선순위 5가지 → `/insights/google-seo/first-month-priorities/` (2025-05-14 발행)
- [ ] **W2 [기술 SEO]** 모바일 우선 색인(Mobile-First Indexing) — 무엇이 다르고 어떻게 점검하나
- [ ] **W3 [콘텐츠 SEO]** 검색 의도 4가지 유형 — 키워드별로 어떻게 분류하고 페이지를 만드나
- [ ] **W4 [지역 SEO]** 네이버 플레이스 부정 리뷰 대응 — 자주 하는 실수 5가지
- [ ] **W5 [백링크·디지털 PR]** 게스트 포스트 — 안전한 매체 골라내는 6가지 기준
- [ ] **W6 [SNS 마케팅]** 유튜브 영상 vs 쇼츠 — SEO 관점의 차이와 활용
- [ ] **W7 [검색 노출 문제 해결]** 색인 누락 페이지 — 사이트맵 재제출 효과 측정법
- [ ] **W8 [구글 SEO]** 2025년 구글 검색 결과 페이지(SERP) 변화 주요 패턴
- [ ] **W9 [기술 SEO]** JavaScript SEO — SPA 사이트에서 자주 빠지는 함정
- [ ] **W10 [콘텐츠 SEO]** 영문 vs 한글 콘텐츠 — 같은 사이트 운영 시 분리 원칙
- [ ] **W11 [지역 SEO]** 다지점 매장 리뷰 운영 — 본사 통합 vs 지점 자율
- [ ] **W12 [백링크·디지털 PR]** 디지털 PR 캠페인 — 데이터 리서치로 언론 인용 만드는 법
- [ ] **W13 [SNS 마케팅]** 인스타그램 검색 탭 — 비즈니스 계정이 활용할 5가지

---

## 📝 운영 원칙

- 매주 1편 발행 (월요일 권장)
- 발행 후 사용자가 검수, 수정 요청 시 추가 푸시
- 카테고리 순환으로 토픽 권위 균형 잡기
- 글이 누적되면 13주 캘린더 다음 분량 추가 작성
- 카테고리당 6편 이상 누적되면 placeholder 카드 모두 제거

## 🧭 Claude를 위한 메모

다음 주 사용자가 "이번 주 글 써줘"라고 하면:
1. 이 파일에서 가장 위쪽의 `[ ]` (미체크) 주제 확인
2. 해당 주제로 블로그 글 작성 (1,500~2,000자, 5~6 섹션, blog_post 헬퍼 사용)
3. `/insights/[카테고리]/[slug]/` 형식 URL
4. sitemap.xml에 새 URL 추가
5. 해당 카테고리 페이지(`/insights/[카테고리]/`)에 insight_article_card로 링크 추가
6. build_pages.py 실행 → 양쪽 브랜치(`claude/help-coding-task-F0jMt`, `claude/onesearchpro-website-NFN2v`)에 푸시
7. 이 파일에서 해당 주차 `[ ]` → `[x]` 변경하고 URL과 발행일 기록

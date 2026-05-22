# 이커머스 이미지 제작 에이전트 v2.6

> 이커머스 농수산물 상세페이지 & 썸네일 & 토스 게시물 광고를 자동 설계하고 Gemini AI로 이미지까지 제작하는 에이전트

---

## 에이전트 개요

이 에이전트는 **3가지 제작 유형**을 제공합니다.

```
[제작 유형]
A) 상세페이지 제작    — 상품 상세페이지 이미지 (4가지 모드)
B) 썸네일 제작        — 상품 대표 이미지 / 마케팅 썸네일
C) 토스 게시물 광고   — 토스 쇼핑 피드 게시물 이미지 + 문구
```

### 상세페이지 모드
```
① 빠른 제작 (경량) — 블록 5개, 분석 스킵, 토큰 절약 ⭐ 기본
② 표준 제작 (중간) — 블록 7개, 간단 분석 + 카피, 균형
③ 정밀 제작 (풀)   — 블록 9개+, 병렬 분석 3개, 높은 품질
④ 프롬프트 추출    — 블록 5개, 이미지 프롬프트만 출력 (API 호출 없음)
```

---

## Phase 0: 초기 설정

### API 키 확인 (자동)

1. Read 도구로 `.env` 파일 존재 여부 확인
2. 파일이 없거나 GEMINI_API_KEY 값이 `your-api-key-here`이면:

```
[AskUserQuestion]
Gemini API 키가 설정되어 있지 않습니다.

📋 API 키 발급 방법:
1. https://aistudio.google.com/apikey 접속
2. Google 로그인 → "Create API Key" 클릭
3. 생성된 키를 아래에 붙여넣기

API 키를 입력해주세요:
```

3. 입력받은 키로 `.env` 파일 생성 (Write 도구):
   ```
   GEMINI_API_KEY={입력값}
   ```

4. Python 패키지 확인:
   ```bash
   python3 -c "import google.genai" 2>/dev/null || pip3 install -r requirements.txt
   ```

### 제작 유형 선택

```
[AskUserQuestion]
무엇을 만들까요?

① 상세페이지 — 상품 상세페이지 이미지
② 썸네일 — 상품 대표 이미지 (검색 결과/목록용)
③ 토스 게시물 광고 — 토스 쇼핑 피드 게시물 이미지 + 문구
```

`task_type` 변수로 저장 (detail / thumbnail / toss_ad).

- **① 상세페이지** → 아래 "제작 모드 선택"으로 이동
- **② 썸네일** → "🖼️ 썸네일 제작 모드"로 이동
- **③ 토스 게시물 광고** → "📢 토스 게시물 광고 제작 모드"로 이동

### 제작 모드 선택 (상세페이지일 때만)

```
[AskUserQuestion]
제작 모드를 선택해주세요:

① 빠른 제작 (경량) — 이미지 5장, 빠르고 토큰 절약 ⭐ 추천
② 표준 제작 (중간) — 이미지 7장, 간단 분석 + 카피
③ 정밀 제작 (풀) — 이미지 9장+, 시장 분석 포함, 고품질
④ 프롬프트 추출 — 기획 + 프롬프트만 (이미지 생성 안 함, API 비용 0원)

초보자는 ①, 일반적으로는 ②를 추천합니다.
프롬프트를 먼저 확인/수정하고 싶으면 ④를 선택하세요.
```

`mode` 변수로 저장 (lite / standard / full / prompt_only).

### 상품명 입력

```
[AskUserQuestion]
상품명을 입력해주세요.
예: "해남 꿀고구마", "제주 감귤", "완도 전복" 등
```

### 플랫폼 선택

```
[AskUserQuestion]
어떤 플랫폼에 등록할 상세페이지인가요?

① 쿠팡 (가로 780px)
② 네이버 스마트스토어 (가로 860px)
③ 올웨이즈 (가로 720px, 모바일 최적화)
④ 토스 쇼핑 (가로 860px)
⑤ 공통 (860px — 4개 플랫폼 호환)
```

`platform` 변수로 저장: coupang / smartstore / alwayz / toss / universal

### 디자인 스타일 선택

```
[AskUserQuestion]
디자인 스타일을 선택해주세요:

① 쇼핑몰 클린 (기본) — 화이트 배경, 쿠팡/마켓컬리 느낌
② 프리미엄 다크 — 고급스러운 다크 톤
③ 내추럴 따뜻한 — 크래프트지, 자연/건강 느낌
④ 비비드 팝 — 강렬한 컬러, 프로모션 느낌
```

`style` 변수로 저장: clean / premium / natural / vivid

스타일별 프롬프트 파일:

| 스타일 키 | 프롬프트 파일 |
|----------|-------------|
| `clean` | `prompts/style-clean.txt` |
| `premium` | `prompts/style-premium.txt` |
| `natural` | `prompts/style-natural.txt` |
| `vivid` | `prompts/style-vivid.txt` |

### 가격 표시 여부 (필수 확인)

```
[AskUserQuestion]
상세페이지 이미지에 가격을 포함할까요?

① 가격 포함 — 이미지에 가격/할인가 직접 표시
② 가격 제외 — 이미지에 가격 넣지 않음 (플랫폼 가격란 사용)

※ 가격 변경이 잦다면 ②를 추천합니다.
```

`include_price` 변수로 저장 (true / false).

**include_price == false일 때 적용 규칙:**
- 히어로 블록: 가격/할인가 뱃지 제거, 인증/배송 뱃지만 표시
- 가격/CTA 블록: 가격 숫자 제거, 구성 옵션(용량/중량)만 표시 + CTA 문구
- 카피 작성 시 가격 관련 문구 모두 제외
- 이미지 프롬프트에서 가격/숫자 관련 텍스트 제거

---

## ⚡ 빠른 제작 모드 (경량) — mode == "lite"

### Lite Phase 1: 상품 정보 수집

WebSearch 도구로 간단 검색 (1~2회):

```
검색 쿼리:
1. "{product_name} 쿠팡" — 가격, 스펙, 후기
```

수집 후 정리:

```markdown
| 항목 | 내용 |
|------|------|
| 상품명 | {product_name} |
| 카테고리 | (추정) |
| 가격대 | (검색 결과) |
| 셀링포인트 | 3개 |
| 배송 | 상온/냉장/냉동 |
```

> Phase 2(병렬 분석)는 **스킵**합니다.

### Lite Phase 2: 블록 5개 고정 + 카피

경량 모드는 농수산물에 최적화된 **5개 블록**만 사용합니다:

| # | 블록 | 설명 |
|---|------|------|
| 1 | 히어로 | 시즐컷 + 메인 카피 + 뱃지 |
| 2 | 셀링포인트 | 핵심 장점 3~4개 카드 |
| 3 | 원재료/산지 | 산지 스토리 + 재배 환경 |
| 4 | 소셜 프루프 | 후기 3개 + 재구매율 |
| 5 | 가격/CTA | 구성 옵션 + 구매 유도 |

블록별 카피를 작성:

```markdown
### 1. 히어로
- 메인 헤드라인: (15자 이내, 감각적)
- 서브 헤드라인: (25자 이내)
- 뱃지: 인증/무료배송/산지직송 등

### 2. 셀링포인트
- 포인트 1: [아이콘] 제목 — 설명
- 포인트 2: [아이콘] 제목 — 설명
- 포인트 3: [아이콘] 제목 — 설명

### 3. 원재료/산지
- 헤드: "왜 {산지}인가"
- 산지 설명 + 재배 특징

### 4. 소셜 프루프
- 헤드: "벌써 N번째 주문이에요"
- 후기 3개 (각 1줄)

### 5. 가격/CTA
- 옵션 2~3개 (용량별 가격)
- CTA: "딱 한 번만 드셔보세요"
```

카피를 `output/{product_name}/copy.md`에 저장.
사용자에게 카피를 보여주고 수정 여부 확인.

### Lite Phase 3: 이미지 5개 병렬 생성

5개 블록을 **Agent 도구로 동시에** 이미지 생성합니다.
각 블록마다 별도 Agent를 실행하여 병렬 처리:

```bash
# 각 블록을 개별 Agent에서 실행 (5개 동시)
python3 scripts/gemini-image.py \
  --product "{product_name}" \
  --block "{block_name}" \
  --block-num {N} \
  --style "{style}" \
  --copy "{copy_text}" \
  --output "output/{product_name}/images/" \
  --platform {platform}
```

생성 완료 후 각 이미지를 Read 도구로 사용자에게 표시.

### Lite Phase 4: 조립 + 완료

```
[AskUserQuestion]
산출물 형태를 선택해주세요:

① 개별 이미지 (기본) — 01_히어로.jpg ~ 05_CTA.jpg
② 합본 이미지 — 전체를 1장으로 합치기
③ 둘 다
```

② 또는 ③ 선택 시 Pillow로 합본:

```python
# 합본은 Python으로 직접 실행
from PIL import Image
# 5개 이미지 세로 이어붙이기
```

완료 안내:

```
✅ 상세페이지 제작 완료! (빠른 제작 모드)

📁 저장 위치: output/{product_name}/
🖼️ 이미지: 5개
📝 카피: output/{product_name}/copy.md

[업로드 방법]
images/ 폴더의 이미지를 번호 순서대로 업로드하세요.

💡 더 많은 블록이 필요하면 /detail-page 에서 "정밀 제작"을 선택하세요.
```

---

## 📦 표준 제작 모드 (중간) — mode == "standard"

### Standard Phase 1: 상품 정보 수집 + 간단 분석

WebSearch 도구로 정보 수집 (2~3회):

```
검색 쿼리:
1. "{product_name} 쿠팡" — 가격, 스펙, 후기
2. "{product_name} 효능 장점" — 셀링포인트 보강
```

수집된 정보를 정리하고 **에이전트 1개**로 간단 분석 실행:

```
Agent 도구로 1개 에이전트 실행:

[간단 분석 에이전트]

상품 정보:
- 상품명: {product_name}
- 수집된 정보: {검색 결과 요약}

분석 항목 (간결하게):

1. 타겟 고객 1~2줄 요약 (누가, 왜 사는지)
2. 핵심 셀링포인트 3~4개
3. 메인 헤드라인 1개 (15자 이내)
4. 서브 헤드라인 1개 (25자 이내)
5. 경쟁 대비 차별점 1~2개

출력: 간결한 분석 요약 (200자 이내)
```

### Standard Phase 2: 블록 7개 + 카피

표준 모드는 **7개 블록**을 사용합니다:

| # | 블록 | 설명 |
|---|------|------|
| 1 | 히어로 | 시즐컷 + 메인 카피 + 뱃지 |
| 2 | 셀링포인트 | 핵심 장점 3~4개 카드 |
| 3 | 원재료/산지 | 산지 스토리 + 재배 환경 |
| 4 | 시즐컷 갤러리 | 다양한 앵글 2~3컷 |
| 5 | 조리법/활용법 | 추천 조리법 2~3가지 |
| 6 | 소셜 프루프 | 후기 3개 + 재구매율 |
| 7 | 가격/CTA | 구성 옵션 + 구매 유도 |

간단 분석 결과를 반영하여 블록별 카피 작성:

```markdown
### 1. 히어로
- 메인 헤드라인: (분석에서 도출, 15자 이내)
- 서브 헤드라인: (25자 이내)
- 뱃지: 인증/무료배송/산지직송 등

### 2. 셀링포인트
- 포인트 1: [아이콘] 제목 — 설명
- 포인트 2: [아이콘] 제목 — 설명
- 포인트 3: [아이콘] 제목 — 설명
- 포인트 4: [아이콘] 제목 — 설명

### 3. 원재료/산지
- 헤드: "왜 {산지}인가"
- 산지 설명 + 재배 특징 + 인증

### 4. 시즐컷 갤러리
- 컷 1: (조리된 상태 클로즈업)
- 컷 2: (원물 정렬 / 포장 상태)
- 컷 3: (라이프스타일 — 먹는 장면)

### 5. 조리법/활용법
- 방법 1: (가장 인기 있는 조리법)
- 방법 2: (간편 조리법)
- 방법 3: (특별한 활용법)

### 6. 소셜 프루프
- 헤드: "벌써 N번째 주문이에요"
- 후기 3개 (각 1줄, 페르소나별)

### 7. 가격/CTA
- 옵션 2~3개 (용량별 가격)
- CTA: 감성적 문구 + 긴급성
```

카피를 `output/{product_name}/copy.md`에 저장.
사용자에게 카피를 보여주고 수정 여부 확인.

### Standard Phase 3: 이미지 7개 병렬 생성

7개 블록을 **Agent 도구로 동시에** 이미지 생성합니다.
각 블록마다 별도 Agent를 실행하여 병렬 처리:

```bash
# 각 블록을 개별 Agent에서 실행 (7개 동시)
python3 scripts/gemini-image.py \
  --product "{product_name}" \
  --block "{block_name}" \
  --block-num {N} \
  --style "{style}" \
  --copy "{copy_text}" \
  --output "output/{product_name}/images/" \
  --platform {platform}
```

생성 완료 후 각 이미지를 Read 도구로 사용자에게 표시.
수정 요청 시 해당 블록만 개별 재생성.

### Standard Phase 4: 조립 + 완료

```
[AskUserQuestion]
산출물 형태를 선택해주세요:

① 개별 이미지 (기본) — 01_히어로.jpg ~ 07_CTA.jpg
② 합본 이미지 — 전체를 1장으로 합치기
③ 둘 다
```

완료 안내:

```
✅ 상세페이지 제작 완료! (표준 제작 모드)

📁 저장 위치: output/{product_name}/
🖼️ 이미지: 7개
📝 카피: output/{product_name}/copy.md

[업로드 방법]
images/ 폴더의 이미지를 번호 순서대로 업로드하세요.
```

---

## 🔬 정밀 제작 모드 (풀) — mode == "full"

### Full Phase 1: 상품 정보 수집

입력 모드를 추가로 확인:

```
[AskUserQuestion]
상품 정보를 어떻게 수집할까요?

① 웹 검색으로 자동 수집 (상품명 기반)
② 상품 URL 입력 (페이지 크롤링)
③ 직접 입력 (질문-답변 인터뷰)
```

#### 모드 ①: 웹 검색

WebSearch 도구로 정보 수집:

```
검색 쿼리:
1. "{product_name} 쿠팡" — 상품 스펙, 가격, 후기
2. "{product_name} 상세페이지" — 경쟁사 구조
3. "{product_name} 후기 장점 단점" — 리뷰 분석
```

#### 모드 ②: URL 입력

WebFetch 도구로 페이지 크롤링 후 추가 WebSearch로 보충.

#### 모드 ③: 직접 인터뷰

한 번에 하나씩 질문:

```
Q1. 상품명과 카테고리
Q2. 판매 가격과 할인가
Q3. 주요 셀링포인트 3~5개
Q4. 타겟 고객
Q5. 경쟁 제품 대비 차별점
Q6. 인증/수상 이력
Q7. 배송 방식
```

상품 프로필 정리:

```markdown
| 항목 | 내용 |
|------|------|
| 상품명 | {product_name} |
| 카테고리 | {category} |
| 가격 | 정가 → 할인가 |
| 셀링포인트 | 1. ... 2. ... 3. ... |
| 타겟 | {target} |
| 차별점 | {differentiator} |
| 인증 | {certifications} |
| 배송 | {shipping} |
```

### Full Phase 2: 병렬 분석 (3개 에이전트 동시)

Agent 도구로 3개 동시 실행:

**에이전트 1: 타겟 고객 분석**
- 구매자 페르소나 2-3개 (이름, 나이, 고통점, 욕구)
- 구매 동기와 장벽
- 감정 트리거

**에이전트 2: 경쟁 상세페이지 분석**
- 상위 셀러 3-5개 블록 구성 벤치마크
- 카피/이미지 패턴
- 약점 & 기회

**에이전트 3: USP 추출 + 메시지 설계**
- USP 한 문장 정의
- 가치 방정식 (Hormozi)
- 헤드라인 후보 3개
- 신뢰 요소

3개 결과를 통합 표로 정리 → 사용자 확인.

### Full Phase 3: 블록 설계 + 카피라이팅

#### 필수 블록 (항상 포함)

| 블록 ID | 블록명 | 설명 |
|---------|-------|------|
| C1 | 히어로 | 시즐컷 + 핵심 카피 |
| C2 | 핵심 셀링포인트 | USP 3~5개 |
| C3 | 시즐컷 갤러리 | 다양한 앵글 |
| C4 | 소셜 프루프 | 리뷰 + 별점 |
| C5 | 가격/구성 옵션 | 가격표 |
| C6 | CTA | 구매 유도 |

#### 식품 특화 블록 (조건부 자동 선택)

| 블록 ID | 블록명 | 자동 선택 조건 |
|---------|-------|--------------|
| F1 | 원재료 스토리 | 산지직송, 유기농, 무농약 |
| F2 | 제조 공정 | HACCP, GMP, 전통 방식 |
| F3 | 비교 차트 | 경쟁 대비 수치 우위 |
| F4 | 조리법/레시피 | 냉동/냉장/밀키트 |
| F5 | 영양 하이라이트 | 건강/다이어트 강조 |
| F6 | 보관/해동 가이드 | 냉동/냉장 배송 |
| F7 | 선물/패키지 | 선물세트/명절 |
| F8 | 수상/미디어 | 수상/방송 이력 |

자동 선택 후 사용자에게 블록 목록 확인.
블록별 카피 작성 → `output/{product_name}/copy.md` 저장.

### Full Phase 4: 이미지 생성 (병렬)

모든 블록을 **Agent 도구로 동시에** 이미지 생성:

```bash
python3 scripts/gemini-image.py \
  --product "{product_name}" \
  --block "{block_name}" \
  --block-num {N} \
  --style "{style}" \
  --copy "{copy_text}" \
  --output "output/{product_name}/images/" \
  --platform {platform}
```

생성 완료 후 Read로 표시 → 수정 요청 시 개별 재생성.

### Full Phase 5: 조립 + 저장

산출물 선택:

```
① 개별 이미지 (기본)
② 합본 이미지
③ 둘 다
```

HTML 생성 여부 별도 확인:

```
HTML 버전도 함께 생성할까요? (예/아니요)
```

HTML 선택 시:
1. `templates/detail-base.html` 로드
2. 변수 치환 (PRODUCT_NAME, SECTIONS, CTA_LINK, CTA_TEXT)
3. `output/{product_name}/detail-page.html` 저장

---

## 📋 프롬프트 추출 모드 — mode == "prompt_only"

> 이미지를 생성하지 않고, 각 블록의 **Gemini 이미지 프롬프트만** 추출합니다.
> API 호출 없음 → 비용 0원. 프롬프트를 확인/수정 후 나중에 이미지를 생성할 수 있습니다.

### PromptOnly Phase 1: 상품 정보 수집 (간략)

WebSearch 1회로 핵심 정보만 수집:

```
검색 쿼리: "{product_name} 쿠팡"
```

정리:

```markdown
| 항목 | 내용 |
|------|------|
| 상품명 | {product_name} |
| 카테고리 | (추정) |
| 셀링포인트 | 3개 |
| 배송 | 상온/냉장/냉동 |
```

> 분석 에이전트는 **스킵**합니다.

### PromptOnly Phase 2: 블록 5개 + 간단 카피

경량 모드와 동일한 **5개 블록** 사용:

| # | 블록 | 설명 |
|---|------|------|
| 1 | 히어로 | 시즐컷 + 메인 카피 + 뱃지 |
| 2 | 셀링포인트 | 핵심 장점 3~4개 카드 |
| 3 | 원재료/산지 | 산지 스토리 + 재배 환경 |
| 4 | 소셜 프루프 | 후기 3개 + 재구매율 |
| 5 | 가격/CTA | 구성 옵션 + 구매 유도 |

각 블록의 카피를 **간결하게** 작성 (블록당 2~3줄).
카피를 `output/{product_name}/copy.md`에 저장.

### PromptOnly Phase 3: 프롬프트 추출

`--prompt-only` 플래그로 gemini-image.py 실행하여 프롬프트만 추출:

```bash
python3 scripts/gemini-image.py \
  --product "{product_name}" \
  --block "{block_name}" \
  --block-num {N} \
  --style "{style}" \
  --copy "{copy_text}" \
  --output "output/{product_name}/prompts/" \
  --platform {platform} \
  --prompt-only
```

5개 블록을 순차 또는 병렬로 실행합니다. (API 호출 없으므로 즉시 완료)

### PromptOnly Phase 4: 결과 출력 + 안내

추출된 프롬프트를 사용자에게 표시:

```markdown
## 📋 프롬프트 추출 결과

### [1] 히어로
{프롬프트 전문}

### [2] 셀링포인트
{프롬프트 전문}

... (5개 전부)
```

저장된 파일 안내:

```
📋 프롬프트 추출 완료!

📁 저장 위치: output/{product_name}/prompts/
📝 개별 파일: 01_히어로_prompt.txt ~ 05_CTA_prompt.txt
📝 전체 모음: all_prompts.md
📝 카피: output/{product_name}/copy.md

[활용 방법]
1. 프롬프트 수정 → /detail-page 에서 ① 빠른 제작으로 이미지 생성
2. 다른 AI 이미지 도구에 프롬프트 직접 사용 (Midjourney, DALL-E 등)
3. 프롬프트를 팀원과 공유하여 리뷰

💡 프롬프트가 마음에 들면, 같은 상품명으로 ① 빠른 제작을 실행하세요.
```

---

## 에러 처리

### Gemini API 에러

```
- API 키 없음 → Phase 0 API 키 설정으로 이동
- Rate limit → 30초 대기 후 재시도 (최대 3회)
- 이미지 생성 실패 → 해당 블록만 재시도, 3회 실패 시 스킵
```

### 파일 시스템 에러

```
- output 폴더 없음 → 자동 생성 (mkdir -p)
- 동일 상품명 폴더 존재 → "{product_name}_v2" 등 버전 추가
```

### 웹 크롤링 에러

```
- URL 접근 불가 → WebSearch 모드로 전환
- 정보 부족 → 인터뷰 모드로 보충 질문
```

---

## 🖼️ 썸네일 제작 모드 — task_type == "thumbnail"

> Phase 0에서 "② 썸네일"을 선택한 경우 이 섹션으로 이동합니다.

### Thumbnail Phase 0: 옵션 설정

상품명, 플랫폼, 가격 표시 여부는 이미 Phase 0에서 입력받음.
아래 질문을 **AskUserQuestion 1회**로 한번에 묻습니다:

```
[AskUserQuestion — 4개 질문 동시]

Q1. 이미지 비율을 선택해주세요:
  ① 1:1 정사각 (기본 — 플랫폼 대표이미지) ⭐
  ② 4:3 가로형 (배너, 프로모션)
  ③ 3:4 세로형 (SNS 피드)
  ④ 16:9 와이드 (상단 배너, 유튜브 썸네일)
  ⑤ 9:16 세로 풀 (릴스, 숏츠, 스토리)

Q2. 배경 스타일을 선택해주세요:
  ① 클린 흰색 — 순백 배경, 상품만 (#FFFFFF)
  ② 자연 배경 — 상품에 어울리는 자연스러운 배경 (AI 추천)
  ③ 직접 입력 — 원하는 배경 설명 (예: "나무 테이블 위", "해변")

Q3. 사람 등장 여부:
  ① 상품만 — 사람 없음
  ② 손만 — 상품을 잡고 있는 손 (먹는 장면, 들고 있는 장면)
  ③ 사람 전체 (여성) — 상품과 함께 여성 모델
  ④ 사람 전체 (남성) — 상품과 함께 남성 모델

Q4. 홍보 문구:
  ① AI 추천 — 상품에 맞는 문구 자동 생성
  ② 직접 입력 — 원하는 문구를 입력
  ③ 문구 없음 — 텍스트 없이 이미지만
```

변수 저장:
- `aspect_ratio`: "1:1" / "4:3" / "3:4" / "16:9" / "9:16"
- `bg_style`: "white" / "natural" / "{사용자 입력}"
- `person`: "none" / "hand" / "female" / "male"
- `copy_mode`: "auto" / "custom" / "none"

### 비율별 해상도 매핑

| 비율 | 해상도 | 용도 |
|------|--------|------|
| 1:1 | 1000x1000px | 플랫폼 대표이미지 |
| 4:3 | 1200x900px | 배너, 프로모션 |
| 3:4 | 900x1200px | SNS 피드 |
| 16:9 | 1280x720px | 배너, 유튜브 썸네일 |
| 9:16 | 720x1280px | 릴스, 숏츠, 스토리 |

### 문구 위치 선택 (copy_mode != "none"일 때만)

```
[AskUserQuestion]

Q1. 문구 위치:
  ① 상단 — 이미지 위쪽
  ② 하단 — 이미지 아래쪽
  ③ 좌측 — 왼쪽 정렬
  ④ 우측 — 오른쪽 정렬
  ⑤ 중앙 — 가운데
  ⑥ AI 추천 — 레이아웃 자동 배치
```

`text_position` 변수 저장: "top" / "bottom" / "left" / "right" / "center" / "auto"

### 문구 확인 (copy_mode == "auto"일 때)

상품 정보 기반으로 문구를 자동 생성하여 확인:

```
[AskUserQuestion]
생성된 홍보 문구를 확인해주세요:

메인: "{자동 생성 — 예: 해남 황토 꿀고구마}"
서브: "{자동 생성 — 예: GAP 인증 | 산지직송}"

수정할 부분이 있으면 말씀해주세요. OK면 "확인"
```

include_price == true인 경우에만 가격 문구 포함.

### Thumbnail Phase 1: 정보 수집 (간단)

WebSearch 1회로 상품 특징 파악:

```
검색 쿼리: "{product_name} 쿠팡"
```

정리:
- 상품 핵심 특징 1줄
- 뱃지 후보 (무농약/GAP/산지직송/무료배송 등)

### Thumbnail Phase 2: 썸네일 생성 (3장 병렬)

모든 옵션을 조합하여 **3장 변형**을 Agent 3개로 동시 생성.

#### 프롬프트 조립 규칙

```
[기본 구조]
{product_type} product {photography_style} of {product_name}.
{aspect_ratio_desc} format, {width}x{height}px.

[배경]
- white → "Pure white background (#FFFFFF). Professional studio lighting."
- natural → "Natural, contextual background suitable for {product_name}. {상품 카테고리에 맞는 배경 자동 추천}."
- 직접 입력 → "{사용자 입력 배경 설명}."

[사람]
- none → (사람 관련 지시 없음)
- hand → "A human hand naturally holding or presenting the product."
- female → "A Korean woman in her 30s naturally presenting the product, lifestyle feel."
- male → "A Korean man in his 30s naturally presenting the product, lifestyle feel."

[문구 — copy_mode != "none"일 때만]
- text_position에 따라:
  "Korean text overlay at {position}:"
  "- Main: \"{main_copy}\" (large, bold)"
  "- Sub: \"{sub_copy}\" (smaller)"

[문구 없음 — copy_mode == "none"일 때]
- "NO text, NO labels, NO watermarks, NO decorations."

[공통]
"High resolution, professional Korean e-commerce style."
"Appetizing, fresh, premium appearance."
```

#### 3장 변형 규칙

Agent 3개를 병렬로 실행. 각 변형은 앵글/구도를 다르게:

| 변형 | 앵글/구도 |
|------|----------|
| A | 정면 — 상품 중심, 안정적 구도 |
| B | 약간 위에서 (30~45도) — 입체감, 전체 모습 |
| C | 클로즈업 또는 측면 — 질감/디테일 강조 |

각 Agent에서 실행:

```bash
python3 scripts/gemini-image.py \
  --product "{product_name}" \
  --block "썸네일_{변형}" \
  --block-num {N} \
  --style "{style}" \
  --copy "{조립된 프롬프트}" \
  --output "output/{product_name}/thumbnails/" \
  --platform {platform}
```

### Thumbnail Phase 3: 확인 + 저장

3장 변형을 Read로 사용자에게 표시:

```
🖼️ 썸네일 3가지 변형:

A. 정면 구도
B. 위에서 (45도)
C. 클로즈업

어떤 것을 사용하시겠어요?
- 선택 (예: A)
- 수정 요청 (예: "A 배경 더 밝게", "B 손을 추가해줘")
- 전부 재생성
- 옵션 변경 후 재생성 (배경/사람/문구 등)
```

선택 완료 시:

```
✅ 썸네일 제작 완료!

📁 저장 위치: output/{product_name}/thumbnails/
🖼️ 파일: thumbnail_A.jpg, thumbnail_B.jpg, thumbnail_C.jpg

[업로드 방법]
마음에 드는 이미지를 플랫폼 대표 이미지에 등록하세요.
- 쿠팡: Wing → 상품 등록 → 대표이미지
- 스마트스토어: 상품 등록 → 대표이미지
- 올웨이즈: 셀러센터 → 상품 등록
- 토스: 입점 관리 → 상품 이미지
```

---

## 에러 처리

### Gemini API 에러

```
- API 키 없음 → Phase 0 API 키 설정으로 이동
- Rate limit → 30초 대기 후 재시도 (최대 3회)
- 이미지 생성 실패 → 해당 블록만 재시도, 3회 실패 시 스킵
```

### 파일 시스템 에러

```
- output 폴더 없음 → 자동 생성 (mkdir -p)
- 동일 상품명 폴더 존재 → "{product_name}_v2" 등 버전 추가
```

### 웹 크롤링 에러

```
- URL 접근 불가 → WebSearch 모드로 전환
- 정보 부족 → 인터뷰 모드로 보충 질문
```

---

## 📢 토스 게시물 광고 제작 모드 — task_type == "toss_ad"

> Phase 0에서 "③ 토스 게시물 광고"를 선택한 경우 이 섹션으로 이동합니다.
> 토스 쇼핑 피드에 노출되는 게시물 광고 이미지 + 문구를 제작합니다.

### 토스 게시물 규격

| 항목 | 규격 |
|------|------|
| 이미지 비율 | 16:9 ~ 9:16 사이 |
| 최소 해상도 | 가로/세로 중 한 면 1280px 이상 |
| 파일 형식 | jpg, png |
| 최대 용량 | 7MB 이하 |
| 하단 영역 | 180px은 게시물 문구로 가려질 수 있음 |
| 게시물 문구 | 최대 39자 |
| 상품 연결 | 게시물당 1개 상품(옵션) |

### TossAd Phase 0: 상품 정보 입력

```
[AskUserQuestion — 1회에 모두 질문]

Q1. 상품 정보를 어떻게 입력하시겠어요?
  ① 상품명 입력 — 이름만 입력하면 자동으로 검색해서 이미지 생성
  ② 상품 이미지 첨부 — 기존 상품 이미지를 기반으로 광고 이미지 생성
  ③ 상품명 + 이미지 둘 다

Q2. 이미지 비율을 선택해주세요:
  ① 1:1 정사각 (1280x1280) ⭐ 추천
  ② 4:3 가로형 (1280x960)
  ③ 3:4 세로형 (960x1280)
  ④ 16:9 와이드 (1280x720)
  ⑤ 9:16 세로 풀 (720x1280)

Q3. 셀러 관리용 게시물명:
  (예: "4월 꿀고구마 프로모션", "신상 감귤 광고")
```

변수 저장:
- `input_mode`: "name" / "image" / "both"
- `toss_ratio`: "square" / "landscape" / "portrait" / "landscape_wide" / "portrait_tall"
- `post_name`: 셀러 관리용 이름 (내부 관리용)

### TossAd Phase 1: 상품 정보 수집

#### input_mode == "name" 인 경우

WebSearch 1회로 정보 수집:

```
검색 쿼리: "{product_name} 토스 쇼핑" 또는 "{product_name} 쿠팡"
```

정리:

```markdown
| 항목 | 내용 |
|------|------|
| 상품명 | {product_name} |
| 카테고리 | (추정) |
| 핵심 특징 | 2~3개 |
| 비주얼 포인트 | (가장 맛있어 보이는 장면) |
```

#### input_mode == "image" 또는 "both" 인 경우

사용자가 첨부한 이미지를 Read 도구로 확인.
이미지에서 상품 특징, 색감, 분위기를 파악하여 프롬프트에 반영:

```markdown
| 항목 | 내용 |
|------|------|
| 상품 외형 | (이미지에서 파악) |
| 색상/톤 | (이미지의 주요 색감) |
| 분위기 | (라이프스타일 / 스튜디오 / 자연 등) |
| 참고 요소 | (유지할 구도, 배경, 소품 등) |
```

### TossAd Phase 2: 게시물 문구 작성

```
[AskUserQuestion]
게시물 문구를 어떻게 할까요? (유저에게 노출되는 문구, 최대 39자)

① AI 추천 — 상품에 맞는 문구 자동 생성 (3개 후보)
② 직접 입력 — 원하는 문구 입력
```

#### copy_mode == "auto" 인 경우

상품 특징 기반으로 **3개 문구 후보** 생성:

```
[사용자에게 표시]

게시물 문구 후보 (최대 39자):

A. "{문구1}" ({글자수}자)
B. "{문구2}" ({글자수}자)
C. "{문구3}" ({글자수}자)

어떤 것을 사용하시겠어요? (A/B/C 또는 직접 수정)
```

문구 작성 가이드라인:
- 최대 39자 엄수
- 상품의 핵심 매력을 한 문장으로
- "~해보세요", "~만나보세요" 등 행동 유도형 권장
- 가격/할인 정보보다는 감성적 어필 우선
- 예시: "해남 땅이 키운 꿀고구마, 한 입이면 반합니다"

`caption` 변수로 저장.

### TossAd Phase 3: 이미지 3장 병렬 생성

Agent 3개를 병렬로 실행하여 **3가지 변형** 생성:

| 변형 | 컨셉 |
|------|------|
| A | 클로즈업 시즐컷 — 상품의 맛있는 디테일 강조 |
| B | 라이프스타일 — 먹는 장면, 자연스러운 분위기 |
| C | 심플 스튜디오 — 깔끔한 배경에 상품 중심 |

각 Agent에서 실행:

```bash
python3 scripts/gemini-image.py \
  --product "{product_name}" \
  --style "{style}" \
  --output "output/{product_name}/toss_ad/" \
  --toss-ad \
  --toss-ratio {toss_ratio} \
  --toss-caption "{caption}" \
  --toss-variation {A/B/C} \
  --toss-context "{변형별 컨텍스트}"
```

**변형별 toss-context 예시:**

- A: `"Extreme close-up of the product. Show texture, juiciness, steam. Sizzle shot style. Dark moody background."`
- B: `"Lifestyle scene. Someone enjoying the product at a cozy table. Natural light, warm tones. Candid, inviting feel."`
- C: `"Clean studio shot. Simple solid background. Product neatly arranged. Minimal, premium aesthetic."`

input_mode가 "image" 또는 "both"인 경우:
- 사용자 이미지의 특징(색감, 구도, 분위기)을 toss-context에 포함
- 예: `"Reference the warm orange tones and rustic wooden table from the provided image. Keep similar composition."`

### TossAd Phase 4: 확인 + 저장

3장을 Read로 사용자에게 표시:

```
📢 토스 게시물 광고 3가지 변형:

A. 클로즈업 시즐컷
B. 라이프스타일
C. 심플 스튜디오

게시물 문구: "{caption}"
셀러 관리용 게시물명: "{post_name}"

어떤 것을 사용하시겠어요?
- 선택 (예: A)
- 수정 요청 (예: "B 배경 더 밝게", "A에 손을 추가해줘")
- 전부 재생성
```

선택 완료 시:

```
✅ 토스 게시물 광고 제작 완료!

📁 저장 위치: output/{product_name}/toss_ad/
🖼️ 이미지: toss_ad_A.jpg, toss_ad_B.jpg, toss_ad_C.jpg
📝 게시물 문구: "{caption}" ({글자수}자)
📋 게시물명: "{post_name}"

[토스 셀러센터 등록 방법]
1. 토스 셀러센터 → 게시물 관리 → 새 게시물
2. 게시물명 입력: {post_name}
3. 이미지 업로드: 선택한 변형 이미지
4. 게시물 문구 입력: {caption}
5. 상품 연결: 해당 상품 검색 후 연결
6. 검수 제출

⚠️ 주의사항:
- 하단 180px에 문구가 노출되어 이미지가 가려질 수 있음
- 게시물 검수 기준을 준수해주세요
- 이미지에 텍스트가 없는 것이 정상입니다 (문구는 플랫폼에서 표시)
```

---

*버전: 2.6*
*생성일: 2026-04-04*
*변경: 토스 게시물 광고 제작 모드 추가 (C 유형 — 피드 이미지 + 문구, 3장 변형 병렬)*
*의존성: scripts/gemini-image.py, prompts/style-*.txt, prompts/block-prompts.txt, templates/detail-base.html*

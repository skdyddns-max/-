# 상세페이지 AI 제작 에이전트

상품명만 입력하면 AI가 이커머스 상세페이지 이미지를 자동 제작합니다.

## 시작하기 (3분)

### 1. Gemini API 키 발급

1. [Google AI Studio](https://aistudio.google.com/apikey) 접속
2. Google 계정 로그인
3. **"Create API Key"** 클릭
4. 생성된 키 복사 (나중에 붙여넣기용)

> 무료로 사용 가능합니다.

### 2. 이 프로젝트 다운로드

```bash
git clone https://github.com/aisyncclub/detail-page-agent.git
cd detail-page-agent
```

### 3. 실행

Claude Code에서 이 폴더를 열고:

```
/detail-page
```

처음 실행하면 API 키를 물어봅니다 → 복사한 키를 붙여넣으면 자동 저장됩니다.

## 지원 플랫폼

| 플랫폼 | 이미지 가로폭 |
|--------|-------------|
| 쿠팡 | 780px |
| 네이버 스마트스토어 | 860px |
| 올웨이즈 | 720px |
| 토스 쇼핑 | 860px |
| 공통 호환 | 860px |

## 산출물

- **개별 이미지** — 블록별 이미지 (01_히어로.jpg, 02_셀링포인트.jpg...)
- **합본 이미지** — 전체를 1장으로 합치기 (선택)
- **HTML** — 브라우저에서 미리보기 가능 (선택)

## 문제 해결

| 증상 | 해결 |
|------|------|
| API 키 오류 | `.env` 파일을 삭제하고 `/detail-page` 다시 실행 |
| 이미지 생성 실패 | 잠시 후 재시도 (API 할당량 초과일 수 있음) |
| Python 없음 | `brew install python3` (Mac) |
| pip install 실패 | `pip3 install -r requirements.txt` 시도 |

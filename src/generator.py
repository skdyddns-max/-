import json
import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = """당신은 SNS 카드뉴스 전문 에디터입니다.
뉴스 기사를 읽기 쉽고 흥미로운 5장짜리 카드뉴스로 변환합니다.
각 카드는 핵심만 담아 간결하게 작성합니다."""

USER_PROMPT = """다음 뉴스 기사를 5장의 카드뉴스로 변환해주세요.

[기사 제목]
{title}

[기사 내용]
{content}

아래 JSON 형식으로만 출력하세요 (다른 텍스트 없이):
{{
  "cover": {{
    "headline": "메인 제목 (15자 이내, 핵심 키워드 포함)",
    "subtitle": "부제목 (25자 이내, 흥미 유발)"
  }},
  "cards": [
    {{
      "title": "카드 제목 (15자 이내)",
      "bullets": ["핵심 내용 1 (30자 이내)", "핵심 내용 2 (30자 이내)", "핵심 내용 3 (30자 이내)"]
    }},
    {{
      "title": "카드 제목 (15자 이내)",
      "bullets": ["핵심 내용 1 (30자 이내)", "핵심 내용 2 (30자 이내)", "핵심 내용 3 (30자 이내)"]
    }},
    {{
      "title": "카드 제목 (15자 이내)",
      "bullets": ["핵심 내용 1 (30자 이내)", "핵심 내용 2 (30자 이내)", "핵심 내용 3 (30자 이내)"]
    }}
  ],
  "closing": {{
    "summary": "핵심 요약 한 줄 (40자 이내)",
    "takeaway": "독자에게 전달할 메시지 (35자 이내)"
  }}
}}"""


def generate_card_content(article: dict) -> dict:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT.format(
                    title=article["title"],
                    content=article["content"][:2000],
                ),
            }
        ],
    )

    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)

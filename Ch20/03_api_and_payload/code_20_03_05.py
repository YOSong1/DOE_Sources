# code_20_03_05.py
# Chapter 20.03 코드 5: JSON 응답을 강제하는 두 가지 방법
#
# (1) OpenAI Responses API: text={"format": {"type": "json_object"}}
# (2) Anthropic Messages API: output_config 의 JSON 스키마 (structured outputs)
#     ※ 구형 assistant prefill 기법("{" 미리 채우기)은 Claude Sonnet 4.6 등
#       최신 모델에서 지원되지 않으며 400 오류가 발생합니다.
#
# 본 파일은 호출부만 보여주고 실제 호출 결과는 별도 검증 단계(코드 4)에서 검사합니다.

import json
import os


# 코드 3(code_20_03_03.py)에서 만든 것과 같은 분석 payload 를 포함한 프롬프트
anova_result = {
    "task": "one-way anova interpretation",
    "goal": "세 가지 처리 조건의 평균 차이를 설명하고 싶다",
    "group_means": {"A": 51.38, "B": 56.31, "C": 57.40},
    "anova_table": {"f_stat": 8.5007, "p_value": 0.0050, "alpha": 0.05},
}
PROMPT = (
    "당신은 통계 분석 리뷰어입니다. 반드시 다음 JSON 스키마로만 답하세요.\n"
    '{"summary": str, "risks": [str, ...], "next_steps": [str, ...]}\n\n'
    "분석 결과:\n"
    + json.dumps(anova_result, ensure_ascii=False, indent=2)
)
SYSTEM = "You are a careful statistical reviewer. Reply in Korean."

REVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "summary":    {"type": "string"},
        "risks":      {"type": "array", "items": {"type": "string"}},
        "next_steps": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["summary", "risks", "next_steps"],
    "additionalProperties": False,
}


def openai_json_call(user_prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI()
    resp = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5"),
        instructions=SYSTEM + " Output JSON only.",
        input=user_prompt,
        text={"format": {"type": "json_object"}},  # JSON 강제
    )
    return resp.output_text


def anthropic_json_call(user_prompt: str) -> str:
    import anthropic
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        max_tokens=800,
        temperature=0,
        system=SYSTEM,
        messages=[{"role": "user", "content": user_prompt}],
        # structured outputs — 키 구성까지 스키마로 보장
        output_config={"format": {"type": "json_schema", "schema": REVIEW_SCHEMA}},
    )
    return msg.content[0].text  # 스키마 준수가 보장된 JSON 문자열


def main():
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    if provider not in {"openai", "anthropic"}:
        raise SystemExit(f"unknown provider: {provider}")

    if not (os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")):
        print("⚠️  API 키가 설정되지 않음. 코드 4(검증) 흐름만 mock 으로 확인하세요.")
        return

    raw = openai_json_call(PROMPT) if provider == "openai" else anthropic_json_call(PROMPT)
    print("=== raw response ===")
    print(raw)
    print("=== parsed ===")
    print(json.dumps(json.loads(raw), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

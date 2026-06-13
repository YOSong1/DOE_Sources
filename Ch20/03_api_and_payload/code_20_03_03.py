# code_20_03_03.py
# Chapter 20.03 코드 3: JSON 구조화 응답을 요청하는 프롬프트 — LLM 호출 + 응답 활용

import json
import os

anova_result = {
    "task": "one-way anova interpretation",
    "goal": "세 가지 처리 조건의 평균 차이를 설명하고 싶다",
    "group_means": {"A": 51.38, "B": 56.31, "C": 57.40},
    "anova_table": {
        "f_stat": 8.5007,
        "p_value": 0.0050,
        "alpha": 0.05
    }
}

prompt = f"""
당신은 통계 분석 리뷰어입니다.

다음 ANOVA 결과를 읽고 반드시 JSON 형식으로만 답변하세요.
키는 summary, risks, next_steps 를 사용하세요.

분석 결과:
{json.dumps(anova_result, ensure_ascii=False, indent=2)}
"""


# ---------------------------------------------------------------------------
# 3) LLM 호출 — API 키 없으면 mock 응답 (흐름 시연용)
# ---------------------------------------------------------------------------
def call_llm(prompt: str, mock: dict) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return json.dumps(mock, ensure_ascii=False)
    from openai import OpenAI
    return OpenAI().responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5"),
        instructions="JSON 으로만 답하세요. 한국어.",
        input=prompt,
        text={"format": {"type": "json_object"}},
    ).output_text


mock_review = {
    "summary": "ANOVA 결과 검토 완료 — 통계적 유의성 확인.",
    "risks": [
        "사후 검정 필요"
    ],
    "next_steps": [
        "Tukey HSD 수행"
    ]
}

raw = call_llm(prompt, mock_review)


# ---------------------------------------------------------------------------
# 4) 응답 활용 — 요약·위험 신호·다음 단계 추출
# ---------------------------------------------------------------------------
review = json.loads(raw)

print("=== LLM 응답 (요약) ===")
print(review["summary"])

risks = review.get("risks", [])
print("\n=== 위험 신호 (" + str(len(risks)) + "건) ===")
for r in risks:
    print("  ⚠️  " + r)

steps = review.get("next_steps", [])
print("\n=== 다음 단계 (" + str(len(steps)) + "건) ===")
for s in steps:
    print("  → " + s)

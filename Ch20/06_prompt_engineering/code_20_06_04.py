# code_20_06_04.py
# Chapter 20.06 코드 4: 보고서 초안 작성용 템플릿 — LLM 호출 + 응답 활용




import json
import os

anova_result = {
    "task": "one-way anova interpretation",
    "design": "one-way ANOVA",
    "group_means": {"A": 51.38, "B": 56.31, "C": 57.40},
    "anova_table": {"f_stat": 8.5007, "p_value": 0.0050, "alpha": 0.05},
}

prompt = f"""
당신은 품질 보고서를 작성하는 기술 문서 도우미입니다.

다음 분석 결과를 바탕으로 Discussion 초안을 작성하세요.
다음 네 문단으로 구성하세요.

1. 결과 요약
2. 실무적 의미
3. 분석의 한계
4. 후속 실험 제안

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
        instructions="네 문단의 내용을 summary, risks, next_steps 키의 JSON 으로만 답하세요. 한국어.",
        input=prompt,
        text={"format": {"type": "json_object"}},
    ).output_text


mock_review = {
    "summary": "결과 요약 + 실무적 의미 정리 완료.",
    "risks": [
        "분석 한계가 보고서에 명시되어야 함"
    ],
    "next_steps": [
        "후속 실험 제안 추가"
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

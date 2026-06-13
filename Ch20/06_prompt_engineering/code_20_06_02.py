# code_20_06_02.py
# Chapter 20.06 코드 2: ANOVA 결과 해석용 템플릿 — LLM 호출 + 응답 활용




import json
import os

anova_result = {
    "task": "one-way anova interpretation",
    "design": "one-way ANOVA",
    "group_means": {"A": 51.38, "B": 56.31, "C": 57.40},
    "anova_table": {"f_stat": 8.5007, "p_value": 0.0050, "alpha": 0.05},
}

prompt = f"""
당신은 통계 분석 리뷰어입니다.

다음 ANOVA 결과를 읽고 아래 형식으로 답변하세요.

1. 핵심 결과 요약
2. 비전문가용 설명
3. 이 결과만으로 가능한 결론과 아직 불가능한 결론
4. 사후검정 또는 추가 분석 필요성

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
        instructions="번호 항목의 내용을 summary, risks, next_steps 키의 JSON 으로만 답하세요. 한국어.",
        input=prompt,
        text={"format": {"type": "json_object"}},
    ).output_text


mock_review = {
    "summary": "ANOVA 결과 검토 — 전체 차이는 유의, 쌍별 차이는 미확정.",
    "risks": [
        "사후 검정 없이 어느 집단이 다른지 단정 금지"
    ],
    "next_steps": [
        "Tukey HSD 사후 검정"
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

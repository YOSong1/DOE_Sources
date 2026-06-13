# code_20_04_02.py
# Chapter 20.04 코드 2: 일원 ANOVA 해석 프롬프트 — LLM 호출 + 응답 활용

import json
import os

anova_result = {
    "task": "one-way anova interpretation",
    "goal": "세 가지 처리 조건의 평균 차이를 설명",
    "design": "one-way ANOVA",
    "groups": ["A", "B", "C"],
    "group_means": {"A": 51.38, "B": 56.31, "C": 57.40},
    "anova_table": {"f_stat": 8.5007, "p_value": 0.0050, "alpha": 0.05},
    "posthoc_needed": True,
}

prompt = f"""
당신은 통계 분석 리뷰어입니다. 다음 ANOVA 결과를 읽고 JSON 으로 답하세요.
키: summary, risks, next_steps
risks 에는 이 결과만으로 내릴 수 없는 결론을, next_steps 에는 사후 검정 필요 여부를 포함하세요.

{json.dumps(anova_result, ensure_ascii=False, indent=2)}
"""


# ---------------------------------------------------------------------------
# LLM 호출 — API 키 없으면 mock 응답 (흐름 시연용)
# ---------------------------------------------------------------------------
def call_llm(prompt: str, mock: dict) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return json.dumps(mock, ensure_ascii=False)
    from openai import OpenAI
    return OpenAI().responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5"),
        instructions="summary, risks, next_steps 키의 JSON 으로만 답하세요. 한국어.",
        input=prompt,
        text={"format": {"type": "json_object"}},
    ).output_text


mock_review = {
    "summary": "세 처리 평균 차이 유의 (F=8.50, p=0.005). 단, 어느 쌍이 다른지는 미확정.",
    "risks": [
        "'모든 집단이 서로 다르다' 는 결론은 이 결과만으로 불가",
        "사후 검정 없이 우열 결정 불가",
    ],
    "next_steps": [
        "Tukey HSD 사후 검정 수행",
        "각 그룹 표본 크기·정규성 점검",
    ],
}

raw = call_llm(prompt, mock_review)


# ---------------------------------------------------------------------------
# 응답 활용 — 요약·위험 신호·다음 단계 추출 (책 20.4.8 검증 통과 응답 활용)
# ---------------------------------------------------------------------------
review = json.loads(raw)  # 또는 validate(raw, payload)["review"]

print("=== LLM 응답 (요약) ===")
print(review["summary"])

print("\n=== 위험 신호 (" + str(len(review["risks"])) + "건) ===")
for r in review["risks"]:
    print("  ⚠️  " + r)

print("\n=== 다음 단계 (" + str(len(review["next_steps"])) + "건) ===")
for s in review["next_steps"]:
    print("  → " + s)

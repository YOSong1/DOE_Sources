# code_20_05_05.py
# Chapter 20.05 코드 5: 해석 초안을 LLM 리뷰어에게 검토시키기

import json
import os

draft = {
    "analysis_type": "fractional factorial DOE",
    "interpretation_draft":
        "A, B, C가 모두 유의하므로 세 요인을 모두 높은 수준으로 설정하면 최적 조건이다.",
}

review_prompt = f"""
당신은 실험계획법 리뷰어입니다.
다음 해석 초안을 검토하고 JSON 으로 답하세요.
키: statistically_risky_parts, design_structure_concerns, safer_statement, confirmation_runs

{json.dumps(draft, ensure_ascii=False, indent=2)}
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
        instructions="statistically_risky_parts, design_structure_concerns, "
                     "safer_statement, confirmation_runs 키의 JSON 으로만 답하세요. 한국어.",
        input=prompt,
        text={"format": {"type": "json_object"}},
    ).output_text


mock_review = {
    "statistically_risky_parts": [
        "'모두 유의하므로 최적' — 유의성만으로 최적 조건을 단정",
    ],
    "design_structure_concerns": [
        "Resolution III 에서는 주효과가 2차 상호작용과 교락되어 순수 효과 보장 불가",
    ],
    "safer_statement": "A, B, C 가 유의하지만 교락 구조를 감안하면 확인 실험 후 최적 조건을 확정해야 한다.",
    "confirmation_runs": [
        "fold-over 설계 추가",
        "유력 조건 확인 실험 2~3건",
    ],
}

raw = call_llm(review_prompt, mock_review)


# ---------------------------------------------------------------------------
# 응답 활용 — 위험 부분·설계 우려·안전한 문장·확인 실험 추출
# ---------------------------------------------------------------------------
review = json.loads(raw)

risky = review.get("statistically_risky_parts", [])
print("=== 통계적으로 위험한 부분 (" + str(len(risky)) + "건) ===")
for p in risky:
    print("  ✗ " + p)

concerns = review.get("design_structure_concerns", [])
print("\n=== 설계 구조상 우려 (" + str(len(concerns)) + "건) ===")
for c in concerns:
    print("  ⚠️  " + c)

print("\n=== 더 안전한 해석 문장 ===")
print("  " + review["safer_statement"])

runs = review.get("confirmation_runs", [])
print("\n=== 확인 실험 제안 (" + str(len(runs)) + "건) ===")
for r in runs:
    print("  → " + r)

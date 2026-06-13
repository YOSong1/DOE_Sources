# code_20_04_05.py
# Chapter 20.04 코드 5: 해석 초안 검토용 프롬프트 — LLM 을 "실수 예방 리뷰어" 로 활용

import json
import os

draft = {
    "analysis_type": "ANOVA",
    "interpretation_draft": "p-value가 0.005이므로 세 집단은 모두 서로 다르다.",
}

review_prompt = f"""
당신은 통계 분석 리뷰어입니다.
다음 해석 초안을 검토하고 JSON 으로 답하세요.
키: incorrect_parts, safer_statement, additional_analysis_needed

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
        instructions="incorrect_parts, safer_statement, additional_analysis_needed 키의 JSON 으로만 답하세요. 한국어.",
        input=prompt,
        text={"format": {"type": "json_object"}},
    ).output_text


mock_review = {
    "incorrect_parts": [
        "'세 집단은 모두 서로 다르다' — 일원 ANOVA 의 p-value 만으로는 단정 불가",
    ],
    "safer_statement": "전체 평균 차이는 유의하지만(F 검정), 어느 쌍이 다른지는 사후 검정이 필요하다.",
    "additional_analysis_needed": [
        "Tukey HSD 또는 Bonferroni 사후 검정",
    ],
}

raw = call_llm(review_prompt, mock_review)


# ---------------------------------------------------------------------------
# 응답 활용 — 부정확한 부분·안전한 문장·추가 분석 추출
# ---------------------------------------------------------------------------
review = json.loads(raw)

incorrect = review.get("incorrect_parts", [])
print("=== 부정확한 부분 (" + str(len(incorrect)) + "건) ===")
for p in incorrect:
    print("  ✗ " + p)

print("\n=== 더 안전한 해석 문장 ===")
print("  " + review["safer_statement"])

needed = review.get("additional_analysis_needed", [])
print("\n=== 추가로 필요한 분석 (" + str(len(needed)) + "건) ===")
for a in needed:
    print("  → " + a)

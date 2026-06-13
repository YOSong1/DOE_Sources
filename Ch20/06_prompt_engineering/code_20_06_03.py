# code_20_06_03.py
# Chapter 20.06 코드 3: DOE 리뷰용 템플릿 — LLM 호출 + 응답 활용




import json
import os

doe_result = {
    "task": "fractional factorial review",
    "design": "2^(5-2)", "resolution": "III",
    "significant_effects": ["A", "B", "C"],
    "alias_note": "주효과가 일부 2차 상호작용과 교락될 수 있음",
    "interpretation_draft": "A, B, C가 모두 유의하므로 세 요인을 모두 높은 수준으로 설정하는 것이 최적이다.",
}

prompt = f"""
당신은 실험계획법 리뷰어입니다.

다음 DOE 결과와 해석 초안을 읽고 아래 형식으로 답변하세요.

1. 해석 초안의 위험한 부분
2. 설계 구조상 조심해야 할 점
3. 더 안전한 해석 문장
4. 확인 실험 또는 후속 설계 제안

분석 결과:
{json.dumps(doe_result, ensure_ascii=False, indent=2)}
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
    "summary": "DOE 결과 검토 — aliasing 위험 발견.",
    "risks": [
        "주효과 = 순수 효과 단정 위험",
        "확인 실험 없는 결론"
    ],
    "next_steps": [
        "fold-over 설계 추가"
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

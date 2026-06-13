# code_20_02_03.py
# Chapter 20.02 코드 3: 부분 요인 실험 결과 사전 구조

import json
import os

doe_result = {
    "task": "fractional factorial review",
    "goal": "부분 요인 실험 결과 해석 초안을 검토하고 싶다",
    "design": "2^(5-2) fractional factorial design",
    "resolution": "III",
    "factors": ["A", "B", "C", "D", "E"],
    "replication": False,
    "significant_effects": ["A", "B", "C"],
    "alias_note": "주효과가 일부 2차 상호작용과 교락될 수 있음",
    "interpretation_draft": "A, B, C가 모두 유의하므로 세 요인을 모두 높은 수준으로 설정하는 것이 최적이다.",
    "questions": [
        "이 해석이 통계적으로 과도한지 검토해줘",
        "aliasing 때문에 주의할 점이 있는지 설명해줘",
        "확인 실험이나 추가 설계를 제안해줘"
    ]
}
print(doe_result)

# 2-bis) 프롬프트 자동 생성 (위 dict 를 그대로 전달)
prompt = (
    "당신은 통계 분석 리뷰어입니다. 반드시 JSON 으로만 답하세요.\n"
    "키: summary, risks, next_steps\n\n"
    + json.dumps(doe_result, ensure_ascii=False, indent=2)
)


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
    "summary": "Resolution III 부분 요인 실험에서 A·B·C 가 유의. 그러나 주효과가 2차 상호작용과 교락될 수 있음.",
    "risks": [
        "aliasing 무시한 채 '모든 요인을 높은 수준' 으로 단정 위험",
        "확인 실험 없이 공정 적용 금지"
    ],
    "next_steps": [
        "fold-over 또는 Resolution IV 추가 설계 검토",
        "유력 조건 1~2개에 대한 확인 실험"
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

# code_20_04_03.py
# Chapter 20.04 코드 3: 이원 ANOVA 사전 (상호작용 포함)

import json
import os

two_way_result = {
    "task": "two-way anova interpretation",
    "goal": "온도와 압력이 수율에 미치는 영향을 해석하고 싶다",
    "main_effects": {
        "Temperature": {"p_value": 0.013},
        "Pressure": {"p_value": 0.041}
    },
    "interaction": {
        "Temperature:Pressure": {"p_value": 0.004}
    },
    "questions": [
        "상호작용이 유의한 경우 주효과 해석에서 주의할 점을 설명해줘",
        "두 요인의 조합 효과를 실무자용 문장으로 정리해줘"
    ]
}
print(two_way_result)

# 2-bis) 프롬프트 자동 생성 (위 dict 를 그대로 전달)
prompt = (
    "당신은 통계 분석 리뷰어입니다. 반드시 JSON 으로만 답하세요.\n"
    "키: summary, risks, next_steps\n\n"
    + json.dumps(two_way_result, ensure_ascii=False, indent=2)
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
    "summary": "Temperature·Pressure 주효과 + 상호작용 모두 유의. 상호작용 우선 해석 필요.",
    "risks": [
        "주효과만 보고 최적 조건 결정 금지",
        "상호작용이 있을 때 평균 효과만 일반화하면 위험"
    ],
    "next_steps": [
        "교호작용 플롯 작성",
        "단순 효과 분석"
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

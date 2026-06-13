# code_20_02_04.py
# Chapter 20.02 코드 4: 구조화된 입력을 만드는 함수

import json
import os

def build_anova_payload(goal, group_means, f_stat, p_value, alpha=0.05):
    return {
        "task": "one-way anova interpretation",
        "goal": goal,
        "group_means": group_means,
        "anova_table": {
            "f_stat": f_stat,
            "p_value": p_value,
            "alpha": alpha
        },
        "questions": [
            "결과를 비전문가에게 설명해줘",
            "과도한 해석이 있는지 검토해줘",
            "사후 검정이 필요한지 알려줘"
        ]
    }


payload = build_anova_payload(
    goal="세 가지 처리 조건의 평균 차이를 설명",
    group_means={"A": 51.38, "B": 56.31, "C": 57.40},
    f_stat=8.5007,
    p_value=0.0050
)

print(payload)

# 2-bis) 프롬프트 자동 생성 (위 dict 를 그대로 전달)
prompt = (
    "당신은 통계 분석 리뷰어입니다. 반드시 JSON 으로만 답하세요.\n"
    "키: summary, risks, next_steps\n\n"
    + json.dumps(payload, ensure_ascii=False, indent=2)
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
    "summary": "세 처리 조건의 평균 차이가 유의함 (F=8.50, p=0.005).",
    "risks": [
        "사후 검정 없이 어느 쌍이 다른지 단정 금지"
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

# code_20_02_01.py
# Chapter 20.02 코드 1: 다중 회귀 결과를 LLM에 전달하기 위한 사전 구조 (page 335295)

import json
import os

regression_result = {
    "task": "multiple regression interpretation",
    "goal": "공정 변수들이 수율에 미치는 영향을 설명하고 싶다",
    "dependent_variable": "Yield",
    "independent_variables": ["Temperature", "Pressure", "Time"],
    "coefficients": {
        "Intercept": 12.53,
        "Temperature": 1.82,
        "Pressure": -0.74,
        "Time": 0.31
    },
    "p_values": {
        "Temperature": 0.002,
        "Pressure": 0.041,
        "Time": 0.287
    },
    "model_fit": {
        "r_squared": 0.81,
        "adj_r_squared": 0.77
    },
    "residual_diagnostics": {
        "normality_ok": True,
        "heteroscedasticity_warning": False
    },
    "questions": [
        "유의한 변수와 유의하지 않은 변수를 구분해줘",
        "실무자에게 설명하는 문장으로 바꿔줘",
        "과도한 해석이 있으면 지적해줘"
    ]
}
print(regression_result)

# 2-bis) 프롬프트 자동 생성 (위 dict 를 그대로 전달)
prompt = (
    "당신은 통계 분석 리뷰어입니다. 반드시 JSON 으로만 답하세요.\n"
    "키: summary, risks, next_steps\n\n"
    + json.dumps(regression_result, ensure_ascii=False, indent=2)
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
    "summary": "Temperature(+1.82, p=0.002), Pressure(-0.74, p=0.041) 가 유의. Time(0.31, p=0.287) 은 유의하지 않음.",
    "risks": [
        "Time 변수에 대해 '효과 없음' 으로 단정 금지",
        "R²=0.81 은 비교적 높지만 잔차 진단을 함께 확인 필요"
    ],
    "next_steps": [
        "Time 의 효과 크기를 추가 표본으로 재검증",
        "이상치·잔차 정규성 시각화"
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

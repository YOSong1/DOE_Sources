# code_20_06_01.py
# Chapter 20.06 코드 1: 회귀 결과 해석용 템플릿 (page 329245) — LLM 호출 + 응답 활용

import json
import os

regression_result = {
    "task": "multiple regression interpretation",
    "goal": "공정 변수들이 수율에 미치는 영향을 설명하고 싶다",
    "coefficients": {"Intercept": 12.53, "Temperature": 1.82,
                     "Pressure": -0.74, "Time": 0.31},
    "p_values": {"Temperature": 0.002, "Pressure": 0.041, "Time": 0.287},
    "model_fit": {"r_squared": 0.81, "adj_r_squared": 0.77},
}

prompt = f"""
당신은 통계 분석 리뷰어입니다.

다음 회귀 분석 결과를 읽고 아래 형식으로 답변하세요.

1. 핵심 결과 요약
2. 유의한 변수와 유의하지 않은 변수 구분
3. 비전문가용 설명
4. 해석상 주의할 점

분석 결과:
{json.dumps(regression_result, ensure_ascii=False, indent=2)}
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
    "summary": "회귀 결과 검토 — 유의 변수와 미유의 변수 구분 완료.",
    "risks": [
        "미유의 변수의 '효과 없음' 단정 금지"
    ],
    "next_steps": [
        "효과 크기와 신뢰구간 함께 검토"
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

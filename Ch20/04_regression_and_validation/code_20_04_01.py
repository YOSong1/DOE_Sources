# code_20_04_01.py
# Chapter 20.04 코드 1: 회귀 결과 해석 프롬프트 — LLM 호출 + 응답 활용

import json
import os

regression_result = {
    "task": "multiple regression interpretation",
    "goal": "공정 변수들이 수율에 미치는 영향을 설명하고 싶다",
    "coefficients": {"Intercept": 12.53, "Temperature": 1.82, "Pressure": -0.74, "Time": 0.31},
    "p_values":     {"Temperature": 0.002, "Pressure": 0.041, "Time": 0.287},
    "model_fit":    {"r_squared": 0.81, "adj_r_squared": 0.77},
    "residual_diagnostics": {"normality_ok": True, "heteroscedasticity_warning": False},
}

prompt = f"""
당신은 통계 분석 리뷰어입니다.
다음 회귀 분석 결과를 읽고 반드시 JSON 형식으로만 답변하세요.
키는 summary, significant_vars, non_significant_vars, risks 를 사용하세요.

{json.dumps(regression_result, ensure_ascii=False, indent=2)}
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
        instructions="summary, significant_vars, non_significant_vars, risks 키의 JSON 으로만 답하세요. 한국어.",
        input=prompt,
        text={"format": {"type": "json_object"}},
    ).output_text


mock_review = {
    "summary": "Temperature(+1.82, p=0.002) 와 Pressure(-0.74, p=0.041) 는 유의, "
               "Time(+0.31, p=0.287) 은 유의하지 않음. R²=0.81 로 설명력 양호.",
    "significant_vars": ["Temperature", "Pressure"],
    "non_significant_vars": ["Time"],
    "risks": [
        "Time 변수를 '효과 없음' 으로 단정 금지 — 현재 데이터에서 충분한 근거를 찾지 못한 것",
        "잔차 진단 결과를 함께 확인 필요",
    ],
}

raw = call_llm(prompt, mock_review)


# ---------------------------------------------------------------------------
# 응답 활용 — 요약·유의/미유의 변수·위험 신호 추출
# ---------------------------------------------------------------------------
review = json.loads(raw)

print("=== LLM 응답 (요약) ===")
print(review["summary"])

print("\n=== 유의한 변수 ===")
for v in review.get("significant_vars", []):
    print("  ✓ " + v)

print("\n=== 유의하지 않은 변수 ===")
for v in review.get("non_significant_vars", []):
    print("  · " + v)

risks = review.get("risks", [])
print("\n=== 위험 신호 (" + str(len(risks)) + "건) ===")
for r in risks:
    print("  ⚠️  " + r)

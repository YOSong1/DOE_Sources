# code_20_03_04.py
# Chapter 20.03 코드 4 (참조 구현): statsmodels Two-way ANOVA → payload → 실제 LLM API 호출 → JSON 응답 검증
#
# 이 스크립트는 다음 흐름을 한 파일에 구현한 "참조 구현"입니다.
#   1) pandas + statsmodels 로 실제 이원 ANOVA 수행
#   2) ANOVA 표·모형 적합도를 JSON 직렬화 가능한 payload dict 로 변환
#   3) JSON 응답을 강제하는 프롬프트 구성
#   4) OpenAI 또는 Anthropic SDK 로 실제 API 호출 (LLM_PROVIDER 환경변수로 선택)
#   5) 응답 파싱 + 필수 키 검증 + payload 와 응답 숫자 일치 검사
#
# 실행 전 준비:
#   pip install pandas statsmodels openai anthropic
#   $env:OPENAI_API_KEY = "sk-..."           # PowerShell
#   $env:LLM_PROVIDER   = "openai"            # 또는 "anthropic"
#
# 키가 없으면 LLM 호출 부분만 mock 응답을 사용해 흐름을 시연합니다.

import json
import math
import os
from typing import Any

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols


# ---------------------------------------------------------------------------
# 1. 실제 분석 — statsmodels 로 이원 ANOVA 수행
# ---------------------------------------------------------------------------
def run_two_way_anova() -> tuple[pd.DataFrame, dict[str, float]]:
    """온도(2수준) × 압력(2수준) 반복 3회 실험 데이터를 분석."""
    df = pd.DataFrame({
        "Temperature": ["low", "low", "high", "high"] * 3,
        "Pressure":    ["low", "high", "low", "high"] * 3,
        "Yield":       [51.2, 54.1, 58.3, 62.0,
                        50.7, 53.8, 57.9, 61.4,
                        51.5, 54.4, 58.8, 62.5],
    })

    model = ols("Yield ~ C(Temperature) * C(Pressure)", data=df).fit()
    anova_df = sm.stats.anova_lm(model, typ=2).reset_index()

    fit = {
        "r_squared":      float(model.rsquared),
        "adj_r_squared":  float(model.rsquared_adj),
        "n_observations": int(model.nobs),
        "df_residual":    int(model.df_resid),
    }
    return anova_df, fit


# ---------------------------------------------------------------------------
# 2. payload 변환 — JSON 직렬화 가능한 형태로
# ---------------------------------------------------------------------------
def _safe(value: Any) -> Any:
    """NaN/Inf 를 None 으로 바꾸고, numpy 스칼라를 Python float 로 변환."""
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if hasattr(value, "item"):  # numpy scalar
        return _safe(value.item())
    return value


def anova_to_payload(anova_df: pd.DataFrame, fit: dict[str, float]) -> dict:
    records = []
    for _, row in anova_df.iterrows():
        records.append({
            "term":    str(row["index"]),
            "sum_sq":  _safe(row["sum_sq"]),
            "df":      _safe(row["df"]),
            "F":       _safe(row.get("F")),
            "p_value": _safe(row.get("PR(>F)")),
        })
    return {
        "task":         "two-way anova interpretation",
        "goal":         "온도와 압력이 수율에 미치는 영향과 상호작용을 검토",
        "anova_table":  records,
        "model_fit":    {k: _safe(v) for k, v in fit.items()},
        "questions": [
            "유의한 효과와 유의하지 않은 효과를 구분해 설명해줘",
            "상호작용이 있을 때 주효과 해석에서 주의할 점을 알려줘",
            "p-value만으로 단정한 부분이 있다면 지적해줘",
        ],
    }


# ---------------------------------------------------------------------------
# 3. 프롬프트 — JSON 응답을 강제
# ---------------------------------------------------------------------------
PROMPT_TEMPLATE = (
    "당신은 통계 분석 리뷰어입니다. 반드시 다음 JSON 스키마로만 답하세요.\n"
    "{{\n"
    "  \"summary\": str,\n"
    "  \"risks\": [str, ...],\n"
    "  \"next_steps\": [str, ...]\n"
    "}}\n\n"
    "분석 결과:\n{payload}\n"
)


def build_prompt(payload: dict) -> str:
    return PROMPT_TEMPLATE.format(
        payload=json.dumps(payload, ensure_ascii=False, indent=2)
    )


# ---------------------------------------------------------------------------
# 4. LLM 호출 — OpenAI / Anthropic 분기
# ---------------------------------------------------------------------------
def call_openai(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI()  # OPENAI_API_KEY 환경변수 자동 사용
    resp = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5"),
        instructions="You are a careful statistical reviewer. Reply in Korean.",
        input=prompt,
        text={"format": {"type": "json_object"}},
    )
    return resp.output_text


ANTHROPIC_REVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "summary":    {"type": "string"},
        "risks":      {"type": "array", "items": {"type": "string"}},
        "next_steps": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["summary", "risks", "next_steps"],
    "additionalProperties": False,
}


def call_anthropic(prompt: str) -> str:
    import anthropic
    client = anthropic.Anthropic()  # ANTHROPIC_API_KEY 환경변수 자동 사용
    msg = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        max_tokens=800,
        temperature=0,
        system="You are a careful statistical reviewer. Reply in Korean.",
        messages=[{"role": "user", "content": prompt}],
        # structured outputs — 스키마 준수가 보장된 JSON 응답
        # (구형 assistant prefill 기법은 Sonnet 4.6 등 최신 모델에서 미지원)
        output_config={"format": {"type": "json_schema",
                                  "schema": ANTHROPIC_REVIEW_SCHEMA}},
    )
    return msg.content[0].text


def call_llm(prompt: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    if provider == "anthropic":
        return call_anthropic(prompt)
    if provider == "openai":
        return call_openai(prompt)
    raise ValueError(f"unknown LLM_PROVIDER: {provider}")


def mock_response(payload: dict) -> str:
    """API 키 미설정 시 사용하는 교육용 mock — 흐름을 끊지 않도록."""
    sig = [r["term"] for r in payload["anova_table"]
           if r["p_value"] is not None and r["p_value"] < 0.05]
    return json.dumps({
        "summary":    f"유의한 효과: {', '.join(sig) if sig else '없음'}",
        "risks":      ["MOCK 응답 — 실제 LLM 검토가 아닙니다."],
        "next_steps": ["환경변수 OPENAI_API_KEY 또는 ANTHROPIC_API_KEY 를 설정해 재실행하세요."],
    }, ensure_ascii=False)


# ---------------------------------------------------------------------------
# 5. 응답 검증 — 필수 키, payload 와 숫자 일치
# ---------------------------------------------------------------------------
REQUIRED_KEYS = {"summary", "risks", "next_steps"}


def validate_response(raw: str, payload: dict) -> dict:
    try:
        review = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM 응답이 유효한 JSON 이 아님: {exc}\nRaw: {raw[:300]}") from exc

    missing = REQUIRED_KEYS - set(review)
    if missing:
        raise ValueError(f"필수 키 누락: {missing}")

    if not isinstance(review["risks"], list) or not isinstance(review["next_steps"], list):
        raise ValueError("'risks' 와 'next_steps' 는 리스트여야 함")

    # payload 의 p-value 가 응답 텍스트에서 다른 값으로 인용되지 않았는지 확인
    summary = str(review.get("summary", ""))
    for record in payload["anova_table"]:
        p = record.get("p_value")
        if p is None:
            continue
        # 예: "p=0.041" 식으로 인용한 값이 payload 와 다르면 경고
        # 여기서는 간단히 0.05 의 자릿수만 점검 (정밀 검증은 절 20.4 참고)
        if "p=" in summary and f"p={round(p, 3):.3f}" not in summary:
            print(f"⚠️  summary 에 인용된 p-value 가 payload({p}) 와 표기가 다를 수 있음")
            break

    return review


# ---------------------------------------------------------------------------
# 6. 메인
# ---------------------------------------------------------------------------
def main() -> None:
    print("[1] 이원 ANOVA 수행")
    anova_df, fit = run_two_way_anova()
    print(anova_df.to_string(index=False))
    print(f"R² = {fit['r_squared']:.4f},  adj R² = {fit['adj_r_squared']:.4f}\n")

    print("[2] payload 변환")
    payload = anova_to_payload(anova_df, fit)
    print(json.dumps(payload, ensure_ascii=False, indent=2)[:400] + " ...\n")

    print("[3] 프롬프트 구성")
    prompt = build_prompt(payload)

    print("[4] LLM 호출")
    has_key = bool(os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"))
    if has_key:
        raw = call_llm(prompt)
        print(f"  ← provider={os.getenv('LLM_PROVIDER', 'openai')} 응답 수신")
    else:
        raw = mock_response(payload)
        print("  ← API 키 미설정: MOCK 응답 사용")

    print("[5] 응답 검증")
    review = validate_response(raw, payload)
    print(json.dumps(review, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

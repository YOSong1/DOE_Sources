# code_20_04_04.py
# Chapter 20.04 코드 4: 응답 검증 — 스키마 + payload 일치 + 금지 표현
#
# LLM 응답을 받아 다음 4단계로 검증합니다.
#   1. JSON 파싱 가능?
#   2. 필수 키가 모두 있는가?
#   3. payload 의 p-value 등 숫자가 응답에서 변형되지 않았는가?
#   4. 과한 단정 표현("모든 집단이 다르다" 등) 이 포함되었는가?

import json
import re
from typing import Iterable


REQUIRED_KEYS = ("summary", "risks", "next_steps")
FORBIDDEN_PATTERNS = (
    re.compile(r"모든\s*집단(이|들)?\s*(서로\s*)?다르다"),
    re.compile(r"확실히\s*\S*\s*우수"),
    re.compile(r"항상\s*\S*\s*효과"),
    re.compile(r"인과(\s*관계)?\s*가\s*있"),  # 단순 회귀로 인과 단정 금지
)


def parse_json(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 파싱 실패: {e}\nraw[:200]={raw[:200]}") from e


def check_schema(review: dict) -> list[str]:
    errors = []
    for k in REQUIRED_KEYS:
        if k not in review:
            errors.append(f"필수 키 누락: {k}")
    if "risks" in review and not isinstance(review["risks"], list):
        errors.append("'risks' 는 리스트여야 함")
    if "next_steps" in review and not isinstance(review["next_steps"], list):
        errors.append("'next_steps' 는 리스트여야 함")
    return errors


def check_numbers(review: dict, payload: dict) -> list[str]:
    """payload 의 p-value 와 다른 값이 응답에 인용되면 경고."""
    text = json.dumps(review, ensure_ascii=False)
    warnings = []
    p_values = []
    for record in payload.get("anova_table", []) + payload.get("coefficients", []):
        p = record.get("p_value")
        if isinstance(p, float):
            p_values.append((record.get("term", "?"), p))

    # 응답에서 "p=0.XX" 또는 "p-value=0.XX" 같은 패턴을 추출
    quoted = re.findall(r"p[\s\-]*(?:value)?\s*[=:≈≒]\s*(\d+\.\d+)", text, re.IGNORECASE)
    for q in quoted:
        q_val = float(q)
        # 가장 가까운 payload p 값과 비교 (절대 오차 1e-3 허용)
        nearest = min(p_values, key=lambda kv: abs(kv[1] - q_val)) if p_values else None
        if nearest and abs(nearest[1] - q_val) > 1e-3:
            warnings.append(
                f"응답에 인용된 p={q_val} 가 payload({nearest[0]}={nearest[1]:.4f}) 와 다름"
            )
    return warnings


def check_forbidden(review: dict) -> list[str]:
    text = json.dumps(review, ensure_ascii=False)
    flags = []
    for pat in FORBIDDEN_PATTERNS:
        if pat.search(text):
            flags.append(f"금지 표현 감지: '{pat.pattern}'")
    return flags


def validate(raw: str, payload: dict) -> dict:
    review = parse_json(raw)
    errors = check_schema(review)
    warnings = check_numbers(review, payload) + check_forbidden(review)
    return {
        "review":   review,
        "errors":   errors,
        "warnings": warnings,
        "valid":    not errors,
    }


# 데모
if __name__ == "__main__":
    payload = {
        "anova_table": [
            {"term": "Treatment", "F": 8.5, "p_value": 0.005},
            {"term": "Residual",  "F": None, "p_value": None},
        ],
    }

    # 정상 응답
    raw_ok = json.dumps({
        "summary":    "처리 효과가 통계적으로 유의함 (p=0.005)",
        "risks":      ["사후 검정 없이 어느 그룹이 다른지 알 수 없음"],
        "next_steps": ["Tukey HSD 사후 검정 수행"],
    }, ensure_ascii=False)

    # 잘못된 응답: 숫자 변형 + 금지 표현
    raw_bad = json.dumps({
        "summary":    "모든 집단이 서로 다르다 (p=0.001)",  # 숫자도 0.001로 변형, 금지 표현
        "risks":      [],
        "next_steps": ["추가 실험"],
    }, ensure_ascii=False)

    print("[OK 응답]")
    print(json.dumps(validate(raw_ok, payload), ensure_ascii=False, indent=2))
    print("\n[Bad 응답]")
    print(json.dumps(validate(raw_bad, payload), ensure_ascii=False, indent=2))

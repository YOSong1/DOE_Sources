# code_20_07_01.py
# Chapter 20.07 코드 1: 변수명·범주명 일반화 + 마스킹
#
# 원본 변수명(`내부코드명_X1`, `고객사_A`)이 LLM 로그에 그대로 남으면
# 사내 IP 가 외부 서비스에 노출됩니다.
# 분석 결과를 LLM 으로 보내기 전에 변수명·범주명을 일반화하고,
# 매핑(역사전)은 로컬에만 저장하는 패턴입니다.

import json
import re


SENSITIVE_NAME = re.compile(r"^(?P<base>[A-Z]+_)?(?P<rest>.+)$")


def anonymize_columns(columns: list[str]) -> tuple[list[str], dict[str, str]]:
    """변수명을 X1, X2, ... Y1, Y2 형태로 치환, mapping 사전을 반환."""
    mapping: dict[str, str] = {}
    new_cols: list[str] = []
    factor_idx = 1
    response_idx = 1
    for col in columns:
        if col.lower().endswith(("yield", "response", "quality")):
            new_name = f"Y{response_idx}"
            response_idx += 1
        else:
            new_name = f"X{factor_idx}"
            factor_idx += 1
        mapping[new_name] = col
        new_cols.append(new_name)
    return new_cols, mapping


def anonymize_payload(payload: dict, column_map: dict[str, str]) -> dict:
    """payload 내부에 나타나는 원본 변수명을 일반화 이름으로 치환."""
    inverse = {v: k for k, v in column_map.items()}
    text = json.dumps(payload, ensure_ascii=False)
    for orig, anon in inverse.items():
        text = text.replace(orig, anon)
    return json.loads(text)


# 예시 — 사내 데이터 변수명
original_columns = ["내부코드_TempA", "내부코드_PressB", "공정수율"]
anon_cols, col_map = anonymize_columns(original_columns)
print("원본 →", original_columns)
print("익명 →", anon_cols)
print("매핑 →", col_map)

# 예시 payload 익명화
payload = {
    "task": "regression interpretation",
    "coefficients": [
        {"term": "내부코드_TempA",  "coef": 0.12, "p_value": 0.002},
        {"term": "내부코드_PressB", "coef": -0.08, "p_value": 0.041},
    ],
    "goal": "내부코드_TempA 가 공정수율에 미치는 영향 검토",
}

anon_payload = anonymize_payload(payload, col_map)
print("\n[익명화 후 payload — 이 버전을 외부 LLM 으로 전송]")
print(json.dumps(anon_payload, ensure_ascii=False, indent=2))

# 원복용 매핑은 로컬에만 저장
with open("variable_mapping.json", "w", encoding="utf-8") as f:
    json.dump(col_map, f, ensure_ascii=False, indent=2)
print("\nvariable_mapping.json 으로 매핑 저장 (외부 전송 금지)")

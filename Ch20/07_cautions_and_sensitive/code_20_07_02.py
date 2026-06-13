# code_20_07_02.py
# Chapter 20.07 코드 2: 원시 데이터 vs 요약 통계만 전송
#
# 외부 LLM API 에는 가능한 한 "이미 계산된 통계량"만 보내는 것이 안전합니다.
# 원시 행 단위 데이터를 보내면 PII·기밀 사양·고객 정보가 그대로 노출됩니다.

import json
import numpy as np
import pandas as pd


# 원시 데이터 (예: 사출 성형 라인 데이터)
rng = np.random.default_rng(0)
raw = pd.DataFrame({
    "lot_id":    [f"LOT_{i:04d}" for i in range(120)],
    "operator":  rng.choice(["김OO", "이OO", "박OO"], 120),
    "temp":      rng.normal(180, 5, 120),
    "pressure":  rng.normal(35, 2, 120),
    "shrinkage": rng.normal(0.5, 0.05, 120),
})


# 1) 위험한 패턴 — 원시 데이터를 그대로 LLM 에 전달
unsafe_payload = {
    "task": "outlier review",
    "raw_data": raw.to_dict("records"),   # ❌ PII (operator), lot_id, 모든 row
}
print(f"[위험] unsafe payload 크기 ≈ {len(json.dumps(unsafe_payload, ensure_ascii=False)):,} chars")


# 2) 안전한 패턴 — 요약 통계만 전달
summary = {
    "task": "outlier review",
    "n":    int(len(raw)),
    "variables": {
        "temp":      {
            "mean":   float(raw["temp"].mean()),
            "std":    float(raw["temp"].std(ddof=1)),
            "q1":     float(raw["temp"].quantile(0.25)),
            "median": float(raw["temp"].median()),
            "q3":     float(raw["temp"].quantile(0.75)),
            "out_of_3sigma": int(((raw["temp"] - raw["temp"].mean()).abs() > 3 * raw["temp"].std()).sum()),
        },
        "shrinkage": {
            "mean":   float(raw["shrinkage"].mean()),
            "std":    float(raw["shrinkage"].std(ddof=1)),
            "p_low":  float(raw["shrinkage"].quantile(0.05)),
            "p_high": float(raw["shrinkage"].quantile(0.95)),
        },
    },
    "questions": [
        "이상치 의심 구간에 대한 점검 방안을 제안해줘",
        "추가로 수집해야 할 보조 변수를 추천해줘",
    ],
    # operator(개인정보), lot_id 는 의도적으로 제외
}
print(f"[안전] summary payload 크기 ≈ {len(json.dumps(summary, ensure_ascii=False)):,} chars")
print(json.dumps(summary, ensure_ascii=False, indent=2))

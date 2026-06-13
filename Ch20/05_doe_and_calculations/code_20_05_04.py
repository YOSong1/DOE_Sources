# code_20_05_04.py
# Chapter 20.05 코드 4: 다구찌 S/N 비 계산 (3가지 특성)
#
# 동일 처리에서 반복 측정한 결과를 사용해 다음 3가지 S/N 비를 계산합니다.
#   - Larger-the-Better:  -10 * log10(mean(1/y^2))
#   - Smaller-the-Better: -10 * log10(mean(y^2))
#   - Nominal-the-Best:   10 * log10(mean^2 / variance)   (var > 0 가정)
# 그리고 각 처리의 S/N 비를 payload 로 만들어 LLM 에 검토 요청합니다.

import json
import numpy as np


def sn_larger(y: np.ndarray) -> float:
    return float(-10 * np.log10(np.mean(1.0 / np.square(y))))


def sn_smaller(y: np.ndarray) -> float:
    return float(-10 * np.log10(np.mean(np.square(y))))


def sn_nominal(y: np.ndarray) -> float:
    mu = np.mean(y)
    var = np.var(y, ddof=1)
    if var <= 0:
        return float("inf")
    return float(10 * np.log10(mu ** 2 / var))


# 예시: 9개 처리(L9 직교배열), 각 처리에서 3회 반복 측정한 응답값
rng = np.random.default_rng(42)
treatments = {
    f"T{i+1}": rng.normal(loc=50 + i * 2, scale=1.5, size=3)
    for i in range(9)
}

records = []
for name, y in treatments.items():
    records.append({
        "treatment": name,
        "responses": [float(v) for v in y],
        "mean":      float(np.mean(y)),
        "std":       float(np.std(y, ddof=1)),
        "sn_larger":  sn_larger(y),
        "sn_smaller": sn_smaller(y),
        "sn_nominal": sn_nominal(y),
    })


payload = {
    "task":  "taguchi S/N ratio review",
    "goal":  "L9 직교배열 9개 처리의 S/N 비 비교 및 최적 처리 식별",
    "characteristic": "larger-the-better (예시)",
    "treatments": records,
    "questions": [
        "Larger-the-Better 기준으로 어느 처리가 가장 우수한지 알려줘",
        "S/N 비 차이가 작아 우열을 단정하기 어려운 처리가 있다면 지적해줘",
        "확인 실험으로 검증해야 할 후보 조건을 추천해줘",
    ],
}
print(json.dumps(payload, ensure_ascii=False, indent=2))

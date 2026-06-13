# code_20_03_02.py
# Chapter 20.03 코드 2: ANOVA 표 → payload (NaN 안전 처리)
#
# statsmodels anova_lm 의 DataFrame 결과를 records 리스트로 변환합니다.
# Residual 행의 F·p_value 가 NaN 인 점에 주의해, None 으로 안전하게 직렬화합니다.

import json
import math

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols


def _safe(x):
    if isinstance(x, float):
        return x if math.isfinite(x) else None
    if hasattr(x, "item"):
        return _safe(x.item())
    return x


# 일원 ANOVA — 3개 처리 조건의 평균 비교
np.random.seed(0)
df = pd.DataFrame({
    "Treatment": np.repeat(["A", "B", "C"], 10),
    "Response":  np.concatenate([
        np.random.normal(50, 3, 10),
        np.random.normal(55, 3, 10),
        np.random.normal(57, 3, 10),
    ]),
})

model = ols("Response ~ C(Treatment)", data=df).fit()
anova_df = sm.stats.anova_lm(model, typ=2).reset_index()

records = []
for _, row in anova_df.iterrows():
    records.append({
        "term":    str(row["index"]),
        "sum_sq":  _safe(row["sum_sq"]),
        "df":      _safe(row["df"]),
        "F":       _safe(row.get("F")),
        "p_value": _safe(row.get("PR(>F)")),
    })

group_means = df.groupby("Treatment")["Response"].mean().round(3).to_dict()

payload = {
    "task":         "one-way anova interpretation",
    "goal":         "세 처리 조건의 평균 차이가 통계적으로 유의한지 검토",
    "factor":       "Treatment",
    "group_means":  {k: _safe(v) for k, v in group_means.items()},
    "anova_table":  records,
    "model_fit": {
        "r_squared":     _safe(model.rsquared),
        "n_observations": int(model.nobs),
    },
    "questions": [
        "어느 그룹 간 차이가 유의한지 사후 검정이 필요한지 알려줘",
        "표본 크기 10이 통계적 결론에 충분한지 의견을 줘",
    ],
}

print(json.dumps(payload, ensure_ascii=False, indent=2))

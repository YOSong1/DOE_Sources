# code_20_03_01.py
# Chapter 20.03 코드 1: OLS 회귀 결과 → LLM payload dict
#
# statsmodels OLS 결과를 JSON 직렬화 가능한 dict 로 변환합니다.
# - 계수, p-value, 95% 신뢰구간, 모형 적합도까지 한번에 묶어
#   LLM 검토용 payload 로 만드는 표준 패턴입니다.

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


# 1) 실제 회귀 분석
np.random.seed(42)
n = 30
df = pd.DataFrame({
    "Temperature": np.random.uniform(150, 250, n),
    "Pressure":    np.random.uniform(10, 50, n),
    "Time":        np.random.uniform(20, 60, n),
})
df["Yield"] = (12.5
               + 0.12 * df["Temperature"]
               - 0.08 * df["Pressure"]
               + 0.03 * df["Time"]
               + np.random.normal(0, 1.5, n))

model = ols("Yield ~ Temperature + Pressure + Time", data=df).fit()


# 2) payload 변환
ci = model.conf_int().rename(columns={0: "ci_low", 1: "ci_high"})
coef_records = []
for term in model.params.index:
    coef_records.append({
        "term":     term,
        "coef":     _safe(model.params[term]),
        "std_err":  _safe(model.bse[term]),
        "t_value":  _safe(model.tvalues[term]),
        "p_value":  _safe(model.pvalues[term]),
        "ci_low":   _safe(ci.loc[term, "ci_low"]),
        "ci_high":  _safe(ci.loc[term, "ci_high"]),
    })

payload = {
    "task":   "multiple regression interpretation",
    "goal":   "공정 변수가 수율에 미치는 영향을 통계적으로 검토",
    "model":  "Yield ~ Temperature + Pressure + Time",
    "coefficients": coef_records,
    "model_fit": {
        "r_squared":     _safe(model.rsquared),
        "adj_r_squared": _safe(model.rsquared_adj),
        "f_statistic":   _safe(model.fvalue),
        "f_p_value":     _safe(model.f_pvalue),
        "n_observations": int(model.nobs),
        "df_residual":   int(model.df_resid),
    },
    "questions": [
        "유의한 변수와 유의하지 않은 변수를 구분해줘",
        "신뢰구간이 0을 포함하는 변수가 있는지 알려줘",
        "이 모델의 한계와 추가 진단이 필요한 점을 지적해줘",
    ],
}

print(json.dumps(payload, ensure_ascii=False, indent=2))

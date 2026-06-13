# code_20_08_02.py
# Chapter 20.08 코드 2: 사출 성형 DOE 데이터로 ANOVA 수행
#
# Step 2(code_20_08_01)의 2^4 설계 행렬을 그대로 받아,
# 예시용 응답 변수(Shrinkage)를 생성한 뒤 책 본문과 동일한
# 모형식으로 회귀·ANOVA 를 수행합니다.

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from pyDOE3 import ff2n


# 1) 설계 행렬 — 4요인 2수준 완전 요인 설계
design = ff2n(4)
df = pd.DataFrame(
    design,
    columns=["Temperature", "Pressure", "CoolingTime", "InjectionSpeed"],
)

# 2) 응답 변수 — 예제용 가상 데이터 (실제 실험 시 df = pd.read_csv(...) 로 대체)
#    Temperature·Pressure 주효과와 상호작용을 포함하도록 설계
np.random.seed(42)
df["Shrinkage"] = (
    0.50
    - 0.06 * df["Temperature"]
    - 0.04 * df["Pressure"]
    - 0.03 * df["Temperature"] * df["Pressure"]
    + np.random.normal(0, 0.02, len(df))
)


# 3) 회귀 + ANOVA (책 본문과 동일한 모형식)
model = ols(
    "Shrinkage ~ Temperature * Pressure + CoolingTime + InjectionSpeed",
    data=df,
).fit()
print(model.summary())

anova = sm.stats.anova_lm(model, typ=2)
print(anova)

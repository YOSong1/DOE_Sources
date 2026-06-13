# code_09_02_01.py
# -*- coding: utf-8 -*-
"""
페이지: 9.2 이원배치 ANOVA — 비료 종류 × 관수 수준이 식물 높이에 미치는 영향.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

data = {
    'fertilizer': ['A','A','A','A','B','B','B','B','C','C','C','C'] * 2,
    'watering':   ['low']*12 + ['high']*12,
    'height': [20, 22, 21, 23, 25, 27, 26, 28, 24, 23, 25, 24,
               30, 32, 31, 33, 34, 35, 36, 33, 32, 31, 33, 34]
}
df = pd.DataFrame(data)

model = ols('height ~ C(fertilizer) + C(watering) + C(fertilizer):C(watering)',
            data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

# code_09_01_01.py
# -*- coding: utf-8 -*-
"""
페이지: 9.1 일원배치 ANOVA — 세 교수법 시험 점수 비교.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
from scipy.stats import f_oneway, levene
from statsmodels.formula.api import ols
import statsmodels.api as sm

scores = {
    'group': ['A']*8 + ['B']*8 + ['C']*8,
    'score': [85, 88, 90, 86, 87, 89, 90, 91,
              78, 80, 79, 77, 82, 81, 80, 79,
              92, 93, 94, 91, 95, 92, 93, 94]
}
df = pd.DataFrame(scores)

groups = [df[df['group'] == g]['score'].values for g in ['A', 'B', 'C']]
stat, p_lev = levene(*groups)
print(f"Levene 검정: W={stat:.3f}, p={p_lev:.3f}")

F_stat, p_val = f_oneway(*groups)
print(f"F통계량: {F_stat:.3f}, p값: {p_val:.4f}")

model = ols('score ~ C(group)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=1)
print(anova_table)

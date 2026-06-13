# code_09_04_03.py
# -*- coding: utf-8 -*-
"""
페이지: 9.4 MANOVA — 사후 단변량 ANOVA + Tukey HSD.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
from statsmodels.formula.api import ols
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

np.random.seed(42)
data = {
    'education': ['HS'] * 15 + ['BS'] * 15 + ['MS'] * 15,
    'math':    list(np.random.normal(70, 5, 15)) +
               list(np.random.normal(78, 5, 15)) +
               list(np.random.normal(86, 5, 15)),
    'reading': list(np.random.normal(74, 4, 15)) +
               list(np.random.normal(82, 4, 15)) +
               list(np.random.normal(90, 4, 15))
}
df = pd.DataFrame(data)

for dv in ['math', 'reading']:
    model = ols(f'{dv} ~ C(education)', data=df).fit()
    anova_t = sm.stats.anova_lm(model, typ=2)
    print(f"\n--- {dv} 단변량 ANOVA ---")
    print(anova_t)

tukey = pairwise_tukeyhsd(endog=df['math'], groups=df['education'], alpha=0.05)
print("\nTukey HSD (math):")
print(tukey)

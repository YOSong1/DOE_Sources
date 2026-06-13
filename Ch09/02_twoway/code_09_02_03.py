# code_09_02_03.py
# -*- coding: utf-8 -*-
"""
페이지: 9.2 이원배치 ANOVA — 비료에 대한 Tukey HSD 사후검정.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = {
    'fertilizer': ['A','A','A','A','B','B','B','B','C','C','C','C'] * 2,
    'watering':   ['low']*12 + ['high']*12,
    'height': [20, 22, 21, 23, 25, 27, 26, 28, 24, 23, 25, 24,
               30, 32, 31, 33, 34, 35, 36, 33, 32, 31, 33, 34]
}
df = pd.DataFrame(data)

tukey_fert = pairwise_tukeyhsd(endog=df['height'], groups=df['fertilizer'], alpha=0.05)
print(tukey_fert)

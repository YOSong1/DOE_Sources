# code_09_01_03.py
# -*- coding: utf-8 -*-
"""
페이지: 9.1 일원배치 ANOVA — Tukey HSD 사후검정.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

scores = {
    'group': ['A']*8 + ['B']*8 + ['C']*8,
    'score': [85, 88, 90, 86, 87, 89, 90, 91,
              78, 80, 79, 77, 82, 81, 80, 79,
              92, 93, 94, 91, 95, 92, 93, 94]
}
df = pd.DataFrame(scores)

tukey = pairwise_tukeyhsd(endog=df['score'], groups=df['group'], alpha=0.05)
print(tukey)
tukey.plot_simultaneous()
plt.title('Tukey HSD 95% 신뢰구간')
plt.show()

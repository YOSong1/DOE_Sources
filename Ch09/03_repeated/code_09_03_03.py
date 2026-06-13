# code_09_03_03.py
# -*- coding: utf-8 -*-
"""
페이지: 9.3 반복 측정 ANOVA — Bonferroni 보정 쌍별 t-검정.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import pandas as pd
import pingouin as pg

data = {
    'subject': [f'S{i+1}' for i in range(10) for _ in range(3)],
    'time':    ['t1', 't2', 't3'] * 10,
    'score':   [55, 60, 63, 50, 52, 55, 65, 66, 70, 58, 60, 64,
                62, 65, 67, 59, 61, 60, 70, 72, 75, 68, 70, 71,
                57, 59, 60, 52, 55, 58]
}
df = pd.DataFrame(data)

posthoc = pg.pairwise_tests(dv='score', within='time', subject='subject',
                            data=df, padjust='bonf')
print(posthoc[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr', 'p_adjust']])

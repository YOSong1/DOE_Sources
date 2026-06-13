# code_10_02_01.py
# -*- coding: utf-8 -*-
"""
페이지: 10.2 피어슨 상관계수 — 공부시간 vs 시험성적 상관 분석.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

np.random.seed(42)
study_hours = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
test_scores = study_hours * 7 + np.random.normal(0, 5, len(study_hours))

r, p_value = stats.pearsonr(study_hours, test_scores)
print(f"피어슨 상관계수: {r:.3f}")
print(f"p-value: {p_value:.4f}")

df = pd.DataFrame({'공부시간': study_hours, '시험성적': test_scores})
r_pandas = df.corr().loc['공부시간', '시험성적']
print(f"피어슨 상관계수 (pandas): {r_pandas:.3f}")

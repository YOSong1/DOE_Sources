# code_10_03_01.py
# -*- coding: utf-8 -*-
"""
페이지: 10.3 스피어만 순위 상관계수 — 이상치 포함 데이터에서 피어슨 vs 스피어만.
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
study_hours = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 50])  # 50은 이상치
test_scores = np.array([40, 50, 55, 60, 65, 70, 75, 80, 85, 90])

r_pearson, p_pearson = stats.pearsonr(study_hours, test_scores)
r_spearman, p_spearman = stats.spearmanr(study_hours, test_scores)

print(f"피어슨 상관계수: {r_pearson:.3f}  (p-value: {p_pearson:.4f})")
print(f"스피어만 상관계수: {r_spearman:.3f}  (p-value: {p_spearman:.4f})")

df = pd.DataFrame({'공부시간': study_hours, '성적': test_scores})
print(f"\nspearman (pandas): {df.corr(method='spearman').loc['공부시간','성적']:.3f}")

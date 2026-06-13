# code_10_04_02.py
# -*- coding: utf-8 -*-
"""
페이지: 10.4 켄달의 타우 — 평가자 순위 막대 비교 시각화.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

reviewer_A = [1, 2, 3, 4, 5, 6, 7, 8]
reviewer_B = [2, 1, 4, 3, 5, 7, 6, 8]
tau, _ = stats.kendalltau(reviewer_A, reviewer_B)

df = pd.DataFrame({
    '영화': [f'영화 {i}' for i in range(1, 9)],
    '평가자A': reviewer_A,
    '평가자B': reviewer_B
})

plt.figure(figsize=(9, 5))
x = np.arange(len(df))
width = 0.35

plt.bar(x - width/2, df['평가자A'], width, label='평가자 A', color='steelblue', alpha=0.8)
plt.bar(x + width/2, df['평가자B'], width, label='평가자 B', color='tomato', alpha=0.8)

plt.xlabel('영화')
plt.ylabel('순위 (낮을수록 높은 평가)')
plt.title(f'두 평가자의 영화 순위 비교 (τ = {tau:.3f})')
plt.xticks(x, df['영화'], rotation=45)
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

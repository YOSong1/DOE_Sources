# code_10_02_02.py
# -*- coding: utf-8 -*-
"""
페이지: 10.2 피어슨 상관계수 — 산점도와 추세선 시각화.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

np.random.seed(42)
study_hours = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
test_scores = study_hours * 7 + np.random.normal(0, 5, len(study_hours))
r, _ = stats.pearsonr(study_hours, test_scores)

plt.figure(figsize=(8, 5))
plt.scatter(study_hours, test_scores, color='steelblue', s=80, alpha=0.8, label='관측값')

m, b = np.polyfit(study_hours, test_scores, 1)
x_line = np.linspace(study_hours.min(), study_hours.max(), 100)
plt.plot(x_line, m * x_line + b, color='tomato', linewidth=2,
         label=f'추세선 (r={r:.3f})')

plt.xlabel('공부 시간 (시간)')
plt.ylabel('시험 성적 (점)')
plt.title('공부 시간과 시험 성적의 관계')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

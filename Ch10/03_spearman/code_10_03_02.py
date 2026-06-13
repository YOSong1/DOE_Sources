# code_10_03_02.py
# -*- coding: utf-8 -*-
"""
페이지: 10.3 스피어만 — 원본 산점도와 순위 변환 산점도 비교.
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

study_hours = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 50])
test_scores = np.array([40, 50, 55, 60, 65, 70, 75, 80, 85, 90])

r_pearson, _ = stats.pearsonr(study_hours, test_scores)
r_spearman, _ = stats.spearmanr(study_hours, test_scores)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].scatter(study_hours, test_scores, color='steelblue', s=80, alpha=0.8)
axes[0].set_title(f'원본 데이터\n피어슨 r={r_pearson:.3f}, 스피어만 ρ={r_spearman:.3f}')
axes[0].set_xlabel('공부 시간')
axes[0].set_ylabel('시험 성적')
axes[0].grid(alpha=0.3)

rank_hours = stats.rankdata(study_hours)
rank_scores = stats.rankdata(test_scores)
axes[1].scatter(rank_hours, rank_scores, color='tomato', s=80, alpha=0.8)
axes[1].set_title('순위 변환 후 산점도')
axes[1].set_xlabel('공부 시간 순위')
axes[1].set_ylabel('시험 성적 순위')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

# code_10_04_01.py
# -*- coding: utf-8 -*-
"""
페이지: 10.4 켄달의 타우 — 두 평가자의 영화 순위 일치도.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy import stats

np.random.seed(42)
reviewer_A = [1, 2, 3, 4, 5, 6, 7, 8]
reviewer_B = [2, 1, 4, 3, 5, 7, 6, 8]

tau, p_value = stats.kendalltau(reviewer_A, reviewer_B)
print(f"켄달의 타우: {tau:.3f}")
print(f"p-value: {p_value:.4f}")

rho, p_spearman = stats.spearmanr(reviewer_A, reviewer_B)
print(f"\n스피어만 상관계수: {rho:.3f}")
print(f"(켄달 타우가 스피어만보다 작은 것은 정상입니다)")

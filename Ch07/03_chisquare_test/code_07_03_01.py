# code_07_03_01.py
# -*- coding: utf-8 -*-
"""
페이지: 7.3 카이제곱 검정 — (1) 적합도 검정 (주사위의 공정성).
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy import stats

observed = np.array([18, 22, 19, 21, 15, 25])
expected = np.array([20, 20, 20, 20, 20, 20])

chi2_stat, p_value = stats.chisquare(f_obs=observed, f_exp=expected)
print(f"카이제곱 통계량: {chi2_stat:.4f}")
print(f"p-값: {p_value:.4f}")
print(f"자유도: {len(observed) - 1}")

if p_value < 0.05:
    print("결론: 주사위가 공정하지 않습니다. (H₀ 기각)")
else:
    print("결론: 주사위가 공정하지 않다는 근거가 없습니다.")

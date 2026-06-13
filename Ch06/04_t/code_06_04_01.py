# code_06_04_01.py
# -*- coding: utf-8 -*-
"""
페이지: 6.4 t 분포 — 신약 투여 후 환자 혈압이 기준값 120과 다른지 단일표본 t검정.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy.stats import t, ttest_1samp
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# 1. 데이터 준비
data = [118, 122, 120, 121, 119, 123, 117, 119, 121, 120]
mu0 = 120

# 2. 단일 표본 t 검정
t_stat, p_val = ttest_1samp(data, mu0)
nu = len(data) - 1

print(f"표본 평균: {np.mean(data):.2f}")
print(f"표본 표준편차: {np.std(data, ddof=1):.4f}")
print(f"t 통계량: {t_stat:.4f}")
print(f"p-value: {p_val:.4f}")
print(f"자유도: {nu}")

alpha = 0.05
if p_val < alpha:
    print("\n결론: 귀무가설 기각 — 신약은 기대 효과와 유의미하게 다릅니다.")
else:
    print("\n결론: 귀무가설 기각 실패.")

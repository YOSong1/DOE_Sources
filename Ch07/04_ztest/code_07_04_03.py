# code_07_04_03.py
# -*- coding: utf-8 -*-
"""
페이지: 7.4 Z-검정 — (3) 두 비율 Z검정 (양측): A광고 vs B광고 클릭률.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

count = np.array([120, 95])
nobs = np.array([1000, 1000])

z_stat, p_value = proportions_ztest(count=count, nobs=nobs)

print(f"광고 A 클릭률: {count[0]/nobs[0]:.4f}")
print(f"광고 B 클릭률: {count[1]/nobs[1]:.4f}")
print(f"Z-통계량: {z_stat:.4f}")
print(f"p-값 (양측): {p_value:.4f}")

if p_value < 0.05:
    print("결론: 두 광고 전략의 클릭률이 유의미하게 다릅니다.")
else:
    print("결론: 두 광고 전략의 클릭률이 같다는 가설을 기각하지 못합니다.")

# code_07_04_01.py
# -*- coding: utf-8 -*-
"""
페이지: 7.4 Z-검정 — (1) 단일표본 Z검정: 지역 성인 평균 수면 시간이 전국 평균 7시간과 다른가?
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy import stats

np.random.seed(42)
sample = np.random.normal(loc=6.7, scale=1.5, size=50)

sigma = 1.5
mu_0 = 7.0

z_stat = (np.mean(sample) - mu_0) / (sigma / np.sqrt(len(sample)))
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

print(f"표본 평균: {np.mean(sample):.4f}시간")
print(f"Z-통계량: {z_stat:.4f}")
print(f"p-값 (양측): {p_value:.4f}")

if p_value < 0.05:
    print("결론: 이 지역 성인의 평균 수면 시간이 전국 평균과 유의미하게 다릅니다.")
else:
    print("결론: 이 지역 성인의 평균 수면 시간이 전국 평균과 다르다고 할 수 없습니다.")

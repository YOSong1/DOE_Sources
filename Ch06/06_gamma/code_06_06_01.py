# code_06_06_01.py
# -*- coding: utf-8 -*-
"""
페이지: 6.6 감마 분포 — α=3, β=2 보험 청구 대기시간 예제.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy.stats import gamma

alpha = 3
beta = 2
scale = 1 / beta

mean_val = alpha / beta
var_val = alpha / beta**2
print(f"평균 대기 시간: {mean_val:.2f}일")
print(f"분산: {var_val:.4f}")
print(f"표준편차: {var_val**0.5:.4f}일")

prob = gamma.cdf(2, a=alpha, scale=scale)
print(f"2일 이내 3번째 청구 확률: {prob:.4f}")

p90 = gamma.ppf(0.90, a=alpha, scale=scale)
print(f"90번째 백분위수: {p90:.4f}일")

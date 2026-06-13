# code_07_04_02.py
# -*- coding: utf-8 -*-
"""
페이지: 7.4 Z-검정 — (2) 단일비율 Z검정 (단측): 캠페인 후 전환율이 20%보다 높아졌는가?
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

n = 300
count = 75
p_0 = 0.20

z_stat, p_value = proportions_ztest(count=count, nobs=n, value=p_0, alternative='larger')

print(f"표본 전환율: {count/n:.4f}")
print(f"Z-통계량: {z_stat:.4f}")
print(f"p-값 (단측): {p_value:.4f}")

if p_value < 0.05:
    print("결론: 마케팅 캠페인이 전환율을 유의미하게 향상시켰습니다.")
else:
    print("결론: 마케팅 캠페인의 전환율 향상 효과가 유의미하지 않습니다.")

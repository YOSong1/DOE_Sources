# code_07_01_03.py
# -*- coding: utf-8 -*-
"""
페이지: 7.1 t-검정 — (3) 대응표본 t검정: 운동 전후 혈압 비교.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy import stats

np.random.seed(42)
before = np.random.normal(loc=130, scale=10, size=20)
after = before - np.random.normal(loc=8, scale=5, size=20)

t_stat, p_value = stats.ttest_rel(before, after)
print(f"t-통계량: {t_stat:.4f}")
print(f"p-값: {p_value:.4f}")
print(f"평균 혈압 변화: {np.mean(before - after):.2f} mmHg")

if p_value < 0.05:
    print("결론: 운동 전후 혈압이 유의미하게 달라졌습니다.")
else:
    print("결론: 운동 전후 혈압 차이가 유의미하지 않습니다.")

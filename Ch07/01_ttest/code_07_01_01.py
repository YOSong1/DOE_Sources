# code_07_01_01.py
# -*- coding: utf-8 -*-
"""
페이지: 7.1 t-검정 — (1) 단일표본 t검정: 부품 길이 평균이 50mm와 같은가?
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy import stats

np.random.seed(42)
measurements = np.random.normal(loc=50.5, scale=1.2, size=25)

t_stat, p_value = stats.ttest_1samp(measurements, popmean=50)
print(f"t-통계량: {t_stat:.4f}")
print(f"p-값: {p_value:.4f}")

if p_value < 0.05:
    print("결론: 부품 평균 길이가 50mm와 유의미하게 다릅니다. (H₀ 기각)")
else:
    print("결론: 부품 평균 길이가 50mm와 다르다고 할 수 없습니다.")

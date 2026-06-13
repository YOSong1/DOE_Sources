# code_07_02_01.py
# -*- coding: utf-8 -*-
"""
페이지: 7.2 F-검정 — (1) 분산 비교 F검정 (두 생산 라인).
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy import stats

np.random.seed(42)
line_a = np.random.normal(loc=50, scale=2, size=30)
line_b = np.random.normal(loc=50, scale=3, size=30)

var_a = np.var(line_a, ddof=1)
var_b = np.var(line_b, ddof=1)
print(f"Var(A): {var_a:.4f}")
print(f"Var(B): {var_b:.4f}")

if var_a >= var_b:
    f_stat = var_a / var_b
    dfn, dfd = len(line_a) - 1, len(line_b) - 1
else:
    f_stat = var_b / var_a
    dfn, dfd = len(line_b) - 1, len(line_a) - 1

cdf_val = stats.f.cdf(f_stat, dfn, dfd)
p_value = 2 * min(cdf_val, 1 - cdf_val)

print(f"F-통계량: {f_stat:.4f} (자유도: {dfn}, {dfd})")
print(f"p-값 (양측): {p_value:.4f}")

if p_value < 0.05:
    print("결론: 두 생산 라인의 분산이 유의미하게 다릅니다.")
else:
    print("결론: 두 생산 라인의 분산이 같다는 가설을 기각하지 못합니다.")

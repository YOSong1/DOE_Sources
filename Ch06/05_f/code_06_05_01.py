# code_06_05_01.py
# -*- coding: utf-8 -*-
"""
페이지: 6.5 F 분포 — 두 생산 라인의 품질 점수 등분산성 양측 F검정.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy.stats import f

line_a = [85, 87, 90, 88, 86, 89, 91, 92, 88, 87]
line_b = [82, 83, 85, 84, 86, 87, 85, 86, 84, 83]

var_a = np.var(line_a, ddof=1)
var_b = np.var(line_b, ddof=1)
f_stat = var_a / var_b
df1 = len(line_a) - 1
df2 = len(line_b) - 1

cdf_val = f.cdf(f_stat, df1, df2)
p_val = 2 * min(cdf_val, 1 - cdf_val)

print(f"Line A 분산: {var_a:.4f}")
print(f"Line B 분산: {var_b:.4f}")
print(f"F 통계량: {f_stat:.4f}  (df1={df1}, df2={df2})")
print(f"p-value (양측): {p_val:.4f}")

alpha = 0.05
if p_val < alpha:
    print("→ 두 집단의 분산이 통계적으로 유의미하게 다릅니다.")
else:
    print("→ 두 집단의 분산이 다르다는 충분한 근거를 찾지 못했습니다.")

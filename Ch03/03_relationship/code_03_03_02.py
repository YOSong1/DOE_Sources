# code_03_03_02.py
"""
3.3 데이터 관계 분석 - 원본 코드 #2
========================================
공분산과 상관계수 계산 (numpy / scipy)
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy import stats

# 기온(°C)과 아이스크림 판매량(개) 데이터
temperature = np.array([25, 28, 30, 23, 29, 33, 35, 27, 31, 26])
sales       = np.array([100, 120, 130, 95, 125, 150, 160, 110, 140, 105])

# 1. 공분산 계산 (표본 공분산, ddof=1)
cov_matrix = np.cov(temperature, sales, ddof=1)
cov_val    = cov_matrix[0, 1]
print(f"공분산: {cov_val:.2f}")

# 2. 상관계수 계산 (numpy)
corr_matrix = np.corrcoef(temperature, sales)
corr_val    = corr_matrix[0, 1]
print(f"상관계수 (np.corrcoef): {corr_val:.4f}")

# 3. 상관계수 계산 (scipy - p-value 포함)
r, p_value = stats.pearsonr(temperature, sales)
print(f"상관계수 (pearsonr):    {r:.4f}")
print(f"p-value:               {p_value:.4f}")

# 4. 결과 해석
if abs(r) >= 0.7:
    strength = "강한"
elif abs(r) >= 0.3:
    strength = "보통"
else:
    strength = "약한"

direction = "양" if r > 0 else "음"
print(f"\n해석: {strength} {direction}의 상관관계 (r = {r:.4f})")

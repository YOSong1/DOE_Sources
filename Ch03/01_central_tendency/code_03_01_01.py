# code_03_01_01.py
"""
3.1 데이터 중심 척도 - 원본 코드 #1
========================================
책 페이지의 첫 번째 코드 블록 (평균/중앙값/최빈값 계산)
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# 1. 데이터 정의
data = np.array([5, 2, 3, 6, 4, 8, 9, 1, 4, 3, 6, 5, 3, 9, 8, 3, 4, 5, 6, 6, 1])

# 2. 중심 척도 계산
mean_val = np.mean(data)
median_val = np.median(data)
mode_result = stats.mode(data, keepdims=True)
mode_val = mode_result.mode[0]

print(f"평균 (Mean):    {mean_val:.2f}")
print(f"중앙값 (Median): {median_val:.2f}")
print(f"최빈값 (Mode):  {mode_val}")

# code_01_02_10.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.2 Python 기본 문법 - 실습: 평균/분산 직접 계산
# =============================================================================
# 페이지: 324206 - 1.2 Python 기본 문법
# 설명: 평균과 모분산을 직접 구현하고 NumPy 결과와 비교.
# =============================================================================

import numpy as np


def mean(data):
    """평균 계산"""
    return sum(data) / len(data)


def variance(data):
    """분산 계산 (모분산)"""
    m = mean(data)
    return sum((x - m) ** 2 for x in data) / len(data)


data = [4, 8, 6, 5, 3, 2, 8, 9, 2, 5]

my_mean = mean(data)
my_var = variance(data)

np_mean = np.mean(data)
np_var = np.var(data)

print(f"평균  - 직접 계산: {my_mean:.4f}, NumPy: {np_mean:.4f}")
print(f"분산  - 직접 계산: {my_var:.4f}, NumPy: {np_var:.4f}")
print(f"일치 여부: {abs(my_mean - np_mean) < 1e-10 and abs(my_var - np_var) < 1e-10}")

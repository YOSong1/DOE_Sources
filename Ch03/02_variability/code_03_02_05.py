# code_03_02_05.py
"""
3.2 데이터 변동성 - 원본 코드 #5: 사분위수 / IQR / 이상치 탐지
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

data = np.array([3, 7, 8, 12, 13, 14, 18, 21, 25, 30])

Q1  = np.percentile(data, 25)
Q2  = np.percentile(data, 50)
Q3  = np.percentile(data, 75)
IQR = Q3 - Q1

print(f"Q1: {Q1}, Q2: {Q2}, Q3: {Q3}, IQR: {IQR}")

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
print(f"이상치 범위: [{lower_bound}, {upper_bound}]")

outliers = data[(data < lower_bound) | (data > upper_bound)]
print(f"이상치: {outliers if len(outliers) > 0 else '없음'}")

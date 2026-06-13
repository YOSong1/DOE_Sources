# code_03_02_08.py
"""
3.2 데이터 변동성 - 원본 코드 #8: 종합 예제 (일별 매출액)
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

# 일별 매출액 데이터 (만원)
sales = np.array([150, 200, 180, 220, 170, 190, 210, 160, 250, 185])

mean_val   = np.mean(sales)
range_val  = np.ptp(sales)
pop_var    = np.var(sales, ddof=0)
sample_var = np.var(sales, ddof=1)
pop_std    = np.std(sales, ddof=0)
sample_std = np.std(sales, ddof=1)
Q1         = np.percentile(sales, 25)
Q3         = np.percentile(sales, 75)
IQR        = Q3 - Q1
cv         = (sample_std / mean_val) * 100

print(f"평균:         {mean_val:.2f} 만원")
print(f"범위:         {range_val} 만원")
print(f"모분산:       {pop_var:.2f}")
print(f"표본분산:     {sample_var:.2f}")
print(f"모표준편차:   {pop_std:.2f} 만원")
print(f"표본표준편차: {sample_std:.2f} 만원")
print(f"IQR:          {IQR} 만원")
print(f"변동계수:     {cv:.2f}%")

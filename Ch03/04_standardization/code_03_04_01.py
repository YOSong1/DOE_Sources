# code_03_04_01.py
"""
3.4 데이터의 표준화 - 원본 코드 #1
========================================
StandardScaler를 이용한 Z-점수 표준화
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from sklearn.preprocessing import StandardScaler

# 일별 매출(만원)과 방문자 수(명)
sales    = np.array([300, 320, 310, 330, 305, 400, 310, 320, 315, 310]).reshape(-1, 1)
visitors = np.array([1500, 1600, 1550, 1300, 1580, 2500, 1550, 1600, 1530, 1550]).reshape(-1, 1)

# StandardScaler로 Z-점수 표준화
scaler_std = StandardScaler()

sales_scaled    = scaler_std.fit_transform(sales)
visitors_scaled = StandardScaler().fit_transform(visitors)

print("=== Z-점수 표준화 결과 ===")
print(f"매출 — 평균: {sales_scaled.mean():.4f}, 표준편차: {sales_scaled.std():.4f}")
print(f"방문자 — 평균: {visitors_scaled.mean():.4f}, 표준편차: {visitors_scaled.std():.4f}")
print(f"\n표준화된 매출 (처음 5개): {sales_scaled.flatten()[:5].round(3)}")

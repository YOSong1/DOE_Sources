# code_03_04_02.py
"""
3.4 데이터의 표준화 - 원본 코드 #2
========================================
MinMaxScaler를 이용한 정규화
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# 일별 생산량(개)과 불량률(%)
production  = np.array([150, 200, 180, 220, 210, 250, 190, 205, 195, 180]).reshape(-1, 1)
defect_rate = np.array([2.5, 3.0, 2.8, 3.5, 3.2, 4.0, 3.0, 3.1, 2.9, 2.8]).reshape(-1, 1)

# MinMaxScaler로 정규화
scaler_mm = MinMaxScaler()

production_scaled   = scaler_mm.fit_transform(production)
defect_scaled       = MinMaxScaler().fit_transform(defect_rate)

print("=== Min-Max 스케일링 결과 ===")
print(f"생산량 — 최솟값: {production_scaled.min():.2f}, 최댓값: {production_scaled.max():.2f}")
print(f"불량률 — 최솟값: {defect_scaled.min():.2f}, 최댓값: {defect_scaled.max():.2f}")
print(f"\n스케일링된 생산량 (처음 5개): {production_scaled.flatten()[:5].round(3)}")

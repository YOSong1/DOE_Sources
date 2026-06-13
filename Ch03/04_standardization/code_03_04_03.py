# code_03_04_03.py
"""
3.4 데이터의 표준화 - 원본 코드 #3
========================================
표준화 전후 히스토그램 비교 (키 vs 체중)
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 평균과 범위가 다른 두 변수
np.random.seed(42)
height = np.random.normal(170, 10, 200)   # 키 (cm), 평균 170
weight = np.random.normal(65,  8, 200)    # 체중 (kg), 평균 65

# 표준화 적용
scaler = StandardScaler()
data_combined = np.column_stack([height, weight])
data_scaled   = scaler.fit_transform(data_combined)

height_scaled = data_scaled[:, 0]
weight_scaled = data_scaled[:, 1]

# 시각화
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 표준화 전
axes[0].hist(height, bins=25, alpha=0.6, color='steelblue', label='키 (cm)')
axes[0].hist(weight, bins=25, alpha=0.6, color='tomato',    label='체중 (kg)')
axes[0].set_title('표준화 전 (원래 단위)')
axes[0].set_xlabel('값')
axes[0].set_ylabel('빈도')
axes[0].legend()

# 표준화 후
axes[1].hist(height_scaled, bins=25, alpha=0.6, color='steelblue', label='키 (표준화)')
axes[1].hist(weight_scaled, bins=25, alpha=0.6, color='tomato',    label='체중 (표준화)')
axes[1].set_title('Z-점수 표준화 후 (평균=0, σ=1)')
axes[1].set_xlabel('Z-점수')
axes[1].set_ylabel('빈도')
axes[1].legend()

plt.tight_layout()
plt.show()

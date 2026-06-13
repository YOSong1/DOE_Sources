# code_03_02_07.py
"""
3.2 데이터 변동성 - 원본 코드 #7: 히스토그램 + 박스플롯
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 평균은 같지만 변동성이 다른 두 데이터 집합
np.random.seed(42)
data_low  = np.random.normal(loc=50, scale=3,  size=200)  # 낮은 변동성
data_high = np.random.normal(loc=50, scale=10, size=200)  # 높은 변동성

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 히스토그램
axes[0].hist(data_low,  bins=20, alpha=0.6, color='steelblue', label='낮은 변동성 (σ≈3)')
axes[0].hist(data_high, bins=20, alpha=0.6, color='tomato',    label='높은 변동성 (σ≈10)')
axes[0].axvline(50, color='black', linestyle='--', linewidth=1.5, label='평균=50')
axes[0].set_title('히스토그램: 변동성 비교')
axes[0].set_xlabel('값')
axes[0].set_ylabel('빈도')
axes[0].legend()

# 박스플롯
axes[1].boxplot([data_low, data_high],
                tick_labels=['낮은 변동성', '높은 변동성'],
                patch_artist=True,
                boxprops=dict(facecolor='lightblue'),
                medianprops=dict(color='red', linewidth=2))
axes[1].set_title('박스플롯: IQR과 이상치 비교')
axes[1].set_ylabel('값')

plt.tight_layout()
plt.show()

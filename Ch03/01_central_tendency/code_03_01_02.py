# code_03_01_02.py
"""
3.1 데이터 중심 척도 - 원본 코드 #2
========================================
책 페이지의 두 번째 코드 블록 (히스토그램 위에 세 척도 시각화)
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

data = np.array([5, 2, 3, 6, 4, 8, 9, 1, 4, 3, 6, 5, 3, 9, 8, 3, 4, 5, 6, 6, 1])

mean_val   = np.mean(data)
median_val = np.median(data)
mode_val   = stats.mode(data, keepdims=True).mode[0]

plt.figure(figsize=(8, 4))
plt.hist(data, bins=range(1, 11), edgecolor='black', alpha=0.7, color='steelblue')
plt.axvline(mean_val,   color='red',    linestyle='--', linewidth=2, label=f'평균: {mean_val:.2f}')
plt.axvline(median_val, color='green',  linestyle='-.', linewidth=2, label=f'중앙값: {median_val:.2f}')
plt.axvline(mode_val,   color='orange', linestyle=':',  linewidth=2, label=f'최빈값: {mode_val}')
plt.xlabel('값')
plt.ylabel('빈도')
plt.title('평균 · 중앙값 · 최빈값 비교')
plt.legend()
plt.tight_layout()
plt.show()

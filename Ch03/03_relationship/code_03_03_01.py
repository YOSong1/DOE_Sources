# code_03_03_01.py
"""
3.3 데이터 관계 분석 - 원본 코드 #1
========================================
산점도 + 추세선 (기온 vs 아이스크림 판매량)
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

# 기온(°C)과 아이스크림 판매량(개) 데이터
temperature = np.array([25, 28, 30, 23, 29, 33, 35, 27, 31, 26])
sales       = np.array([100, 120, 130, 95, 125, 150, 160, 110, 140, 105])

# 추세선 계산 (1차 다항식 피팅)
coeffs = np.polyfit(temperature, sales, 1)
trend  = np.poly1d(coeffs)
x_line = np.linspace(temperature.min(), temperature.max(), 100)

# 산점도 + 추세선
plt.figure(figsize=(7, 5))
plt.scatter(temperature, sales, color='steelblue', s=80, label='관측값')
plt.plot(x_line, trend(x_line), color='red', linewidth=2, label='추세선')
plt.xlabel('기온 (°C)')
plt.ylabel('아이스크림 판매량 (개)')
plt.title('기온 vs 아이스크림 판매량 산점도')
plt.legend()
plt.tight_layout()
plt.show()

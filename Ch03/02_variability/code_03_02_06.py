# code_03_02_06.py
"""
3.2 데이터 변동성 - 원본 코드 #6: 변동계수(CV) - 단위 다른 변수 비교
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

data_A = np.array([165, 170, 175, 180, 160])  # 키 (cm)
data_B = np.array([60, 65, 70, 75, 55])        # 체중 (kg)

cv_A = (np.std(data_A, ddof=1) / np.mean(data_A)) * 100
cv_B = (np.std(data_B, ddof=1) / np.mean(data_B)) * 100

print(f"키 변동계수:   {cv_A:.2f}%")
print(f"체중 변동계수: {cv_B:.2f}%")

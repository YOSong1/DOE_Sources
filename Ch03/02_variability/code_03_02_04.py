# code_03_02_04.py
"""
3.2 데이터 변동성 - 원본 코드 #4: A/B 공장 품질 비교
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

# A 공장과 B 공장의 부품 길이 (mm)
factory_A = np.array([100.2, 99.8, 100.1, 100.0, 99.9, 100.3, 99.7, 100.0])
factory_B = np.array([98.5, 101.5, 97.0, 103.0, 99.0, 101.0, 98.0, 102.0])

mean_A = np.mean(factory_A)
mean_B = np.mean(factory_B)
std_A  = np.std(factory_A, ddof=1)
std_B  = np.std(factory_B, ddof=1)

print(f"A 공장 — 평균: {mean_A:.2f} mm, 표준편차: {std_A:.4f} mm")
print(f"B 공장 — 평균: {mean_B:.2f} mm, 표준편차: {std_B:.4f} mm")

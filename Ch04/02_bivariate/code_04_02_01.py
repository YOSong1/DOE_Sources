# code_04_02_01.py
"""
4.2 2차원 확률 변수 - 원본 코드 #1
========================================
이산형 결합 분포에서 E[X], E[Y], Cov(X,Y), 상관계수 계산
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

# 1. 결합 확률 행렬 (행: Y값, 열: X값)
joint = np.array([[0.1, 0.2],
                  [0.3, 0.4]])

x_values = np.array([0, 1])
y_values = np.array([0, 1])

# 2. 주변 확률
p_x = joint.sum(axis=0)  # 열 합산 → X의 주변 확률
p_y = joint.sum(axis=1)  # 행 합산 → Y의 주변 확률

# 3. 기댓값
E_X = np.sum(x_values * p_x)
E_Y = np.sum(y_values * p_y)

# 4. E[XY] 계산
E_XY = 0.0
for i, xi in enumerate(x_values):
    for j, yj in enumerate(y_values):
        E_XY += xi * yj * joint[j, i]

# 5. 공분산
cov = E_XY - E_X * E_Y

# 6. 분산과 표준편차
var_X = np.sum((x_values - E_X)**2 * p_x)
var_Y = np.sum((y_values - E_Y)**2 * p_y)
std_X = np.sqrt(var_X)
std_Y = np.sqrt(var_Y)

# 7. 상관계수
rho = cov / (std_X * std_Y)

print(f"E[X] = {E_X:.4f}, E[Y] = {E_Y:.4f}")
print(f"Cov(X,Y) = {cov:.4f}")
print(f"Correlation coefficient = {rho:.4f}")

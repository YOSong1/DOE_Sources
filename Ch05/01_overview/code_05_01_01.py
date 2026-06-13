# code_05_01_01.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.1 이산형 확률 분포의 개요
# 출처: WikiDocs book 1914, page 324300
# 설명: 주사위 한 개의 PMF로부터 기댓값, 분산, 표준편차를 직접 계산하는 예제

import numpy as np

# 주사위 1개를 던지는 확률 변수
k = np.array([1, 2, 3, 4, 5, 6])          # 가능한 값
p = np.array([1/6, 1/6, 1/6, 1/6, 1/6, 1/6])  # 각 값의 확률

# 기댓값 계산
E_X = np.sum(k * p)
print(f"기댓값 E[X] = {E_X:.4f}")  # 3.5

# 분산 계산
Var_X = np.sum((k - E_X)**2 * p)
print(f"분산 Var(X) = {Var_X:.4f}")  # 2.9167

# 표준편차 계산
SD_X = np.sqrt(Var_X)
print(f"표준편차 SD(X) = {SD_X:.4f}")  # 1.7078

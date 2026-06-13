# code_04_01_01.py
"""
4.1 1차원 확률 변수 - 원본 코드 #1
========================================
이산형: 주사위 PMF와 CDF
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import randint

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 주사위: 1부터 6까지 균등 이산 분포
# randint(low, high)는 [low, high) 범위 → low=1, high=7
rv = randint(1, 7)
x = np.arange(1, 7)

# 2. PMF와 CDF 계산
pmf = rv.pmf(x)
cdf = rv.cdf(x)

# 3. 기댓값과 분산
mean, var = rv.mean(), rv.var()
print(f"E[X] = {mean:.4f}")   # 3.5
print(f"Var(X) = {var:.4f}")  # 2.9167

# 4. 시각화
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].bar(x, pmf, color='steelblue', edgecolor='black', alpha=0.8)
axes[0].set_title("주사위 PMF")
axes[0].set_xlabel("눈의 수 x")
axes[0].set_ylabel("P(X = x)")

axes[1].step(x, cdf, where='post', color='tomato', linewidth=2)
axes[1].set_title("주사위 CDF")
axes[1].set_xlabel("눈의 수 x")
axes[1].set_ylabel("F(x) = P(X ≤ x)")

plt.tight_layout()
plt.show()

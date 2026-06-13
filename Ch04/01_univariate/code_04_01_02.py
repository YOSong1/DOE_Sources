# code_04_01_02.py
"""
4.1 1차원 확률 변수 - 원본 코드 #2
========================================
연속형: 표준 정규 분포 PDF와 CDF
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 표준 정규 분포
rv = norm(loc=0, scale=1)
x = np.linspace(-4, 4, 300)

# 2. PDF와 CDF 계산
pdf = rv.pdf(x)
cdf = rv.cdf(x)

# 3. 기댓값과 분산
print(f"E[X] = {rv.mean():.4f}")   # 0.0
print(f"Var(X) = {rv.var():.4f}")  # 1.0

# 4. 시각화
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].plot(x, pdf, color='steelblue', linewidth=2)
axes[0].fill_between(x, pdf, alpha=0.2, color='steelblue')
axes[0].set_title("표준 정규 분포 PDF")
axes[0].set_xlabel("x")
axes[0].set_ylabel("f(x)")

axes[1].plot(x, cdf, color='tomato', linewidth=2)
axes[1].set_title("표준 정규 분포 CDF")
axes[1].set_xlabel("x")
axes[1].set_ylabel("F(x) = P(X ≤ x)")

plt.tight_layout()
plt.show()

# code_04_02_02.py
"""
4.2 2차원 확률 변수 - 원본 코드 #2
========================================
2차원 정규 분포 시뮬레이션과 결합 PDF 등고선
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 2차원 정규 분포 파라미터
mu = [0, 0]
rho = 0.8
cov_matrix = [[1, rho],
              [rho, 1]]

# 2. 난수 생성
np.random.seed(42)
samples = np.random.multivariate_normal(mu, cov_matrix, size=1000)
X_samples, Y_samples = samples[:, 0], samples[:, 1]

# 3. 시각화
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 산점도
axes[0].scatter(X_samples, Y_samples, alpha=0.3, s=10, color='steelblue')
axes[0].set_title(f"2차원 정규 분포 산점도 (ρ = {rho})")
axes[0].set_xlabel("X")
axes[0].set_ylabel("Y")

# 컨투어(등고선) 플롯
x_grid = np.linspace(-3, 3, 100)
y_grid = np.linspace(-3, 3, 100)
X_grid, Y_grid = np.meshgrid(x_grid, y_grid)
pos = np.dstack((X_grid, Y_grid))
rv = multivariate_normal(mu, cov_matrix)
Z = rv.pdf(pos)

axes[1].contourf(X_grid, Y_grid, Z, levels=15, cmap='Blues')
axes[1].contour(X_grid, Y_grid, Z, levels=15, colors='navy', linewidths=0.5)
axes[1].set_title(f"결합 PDF 등고선 (ρ = {rho})")
axes[1].set_xlabel("X")
axes[1].set_ylabel("Y")

plt.tight_layout()
plt.show()

# 4. 공분산과 상관계수 확인
print(f"표본 공분산 행렬:\n{np.cov(X_samples, Y_samples)}")
print(f"표본 상관계수: {np.corrcoef(X_samples, Y_samples)[0, 1]:.4f}")

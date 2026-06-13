# code_16_03_02.py
# Chapter 16.3 예제로 이해: 커피 머신 조건의 Box-Behnken 최적화
# 원본 코드 2: scipy.optimize로 경계 제약 하의 최적 조건 탐색
#
# 무제약 정상점이 설계 영역 [-1, 1]^3 밖에 있으므로
# bounds=[(-1,1),(-1,1),(-1,1)] 제약을 두고 수치 최적화를 수행해
# 실제 운영 가능한 최적의 (온도, 시간, 원두량) 조합을 찾습니다.

import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# 1. Box-Behnken 설계 데이터 생성
data = {
    "X1": [-1, 1, -1, 1, -1, 1, -1, 1, 0, 0, 0, 0, 0, 0, 0],
    "X2": [-1, -1, 1, 1, 0, 0, 0, 0, -1, 1, -1, 1, 0, 0, 0],
    "X3": [0, 0, 0, 0, -1, -1, 1, 1, -1, -1, 1, 1, 0, 0, 0],
    "Y": [70, 80, 75, 85, 60, 65, 78, 88, 55, 60, 72, 82, 80, 82, 81]
}
df = pd.DataFrame(data)

# 2. 설계 행렬 (X) 생성
X = np.ones((df.shape[0], 10))
X[:, 1] = df["X1"]
X[:, 2] = df["X2"]
X[:, 3] = df["X3"]
X[:, 4] = df["X1"] * df["X2"]
X[:, 5] = df["X1"] * df["X3"]
X[:, 6] = df["X2"] * df["X3"]
X[:, 7] = df["X1"] ** 2
X[:, 8] = df["X2"] ** 2
X[:, 9] = df["X3"] ** 2
Y = df["Y"].values

# 3. 회귀 계수 계산
beta = np.linalg.inv(X.T @ X) @ X.T @ Y
print("회귀 계수 (Beta):")
print(beta)

# 4. 최적화 - 음의 예측값을 최소화 = 예측값 최대화
def objective(x):
    X_opt = np.array([
        1,
        x[0], x[1], x[2],
        x[0] * x[1], x[0] * x[2], x[1] * x[2],
        x[0] ** 2, x[1] ** 2, x[2] ** 2
    ])
    return -(X_opt @ beta)

bounds = [(-1, 1), (-1, 1), (-1, 1)]
result = minimize(objective, x0=[0, 0, 0], bounds=bounds)

optimal_conditions = result.x
optimal_score = -result.fun

print("\n최적 조건:")
print(f"물의 온도 (X1): {85 + (95 - 85) * (optimal_conditions[0] + 1) / 2:.2f} °C")
print(f"추출 시간 (X2): {20 + (30 - 20) * (optimal_conditions[1] + 1) / 2:.2f} 초")
print(f"원두의 양 (X3): {10 + (20 - 10) * (optimal_conditions[2] + 1) / 2:.2f} g")
print(f"최적 맛 점수 (Y): {optimal_score:.2f}")

# 5. 3D 시각화
X1_vals = np.linspace(-1, 1, 50)
X2_vals = np.linspace(-1, 1, 50)
X1_grid, X2_grid = np.meshgrid(X1_vals, X2_vals)
X3_fixed = 0

Y_vals = np.zeros_like(X1_grid)
for i in range(X1_grid.shape[0]):
    for j in range(X1_grid.shape[1]):
        x1, x2 = X1_grid[i, j], X2_grid[i, j]
        X_eval = np.array([
            1, x1, x2, X3_fixed,
            x1 * x2, x1 * X3_fixed, x2 * X3_fixed,
            x1 ** 2, x2 ** 2, X3_fixed ** 2
        ])
        Y_vals[i, j] = X_eval @ beta

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
surface = ax.plot_surface(
    85 + (95 - 85) * (X1_grid + 1) / 2,
    20 + (30 - 20) * (X2_grid + 1) / 2,
    Y_vals,
    cmap="viridis",
    alpha=0.8
)
ax.set_xlabel("물의 온도 (°C)")
ax.set_ylabel("추출 시간 (초)")
ax.set_zlabel("맛 점수 (Y)")
fig.colorbar(surface, shrink=0.5, aspect=10)
plt.title("물의 온도와 추출 시간에 따른 맛 점수")
plt.show()

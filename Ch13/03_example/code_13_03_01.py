# code_13_03_01.py
# -*- coding: utf-8 -*-
"""
페이지: 13.3 예제로 이해: 2요인 공정의 응답 표면 분석
설명: 5x5 격자 실험점 생성 → 가상 2차 식으로 반응값 시뮬레이션
      → 2차 다항 회귀 적합 → 3D 표면 시각화의 전체 코드.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# 1. 임의의 실험점 생성 (CCD, Box-Behnken이 아닌 단순 예시)
# 여기서는 x1, x2를 -2 ~ 2 범위에서 균일하게 샘플링
# ---------------------------------------------------------------------
np.random.seed(123)
n_points = 25
x1 = np.linspace(-2, 2, int(np.sqrt(n_points)))  # 예: -2부터 2까지
x2 = np.linspace(-2, 2, int(np.sqrt(n_points)))
X1, X2 = np.meshgrid(x1, x2)
X1 = X1.ravel()
X2 = X2.ravel()

# ---------------------------------------------------------------------
# 2. 실제 반응값(Y) 생성 (가상의 2차 식 + 오차)
# ---------------------------------------------------------------------
epsilon = np.random.normal(0, 0.5, len(X1))  # 오차항
Y_true = 5 + 2*X1 + 3*X2 + 1.5*X1**2 + 1.0*X2**2 + 1.2*X1*X2
Y = Y_true + epsilon

# ---------------------------------------------------------------------
# 3. 회귀모형 적합
# 2차 모형: 1, x1, x2, x1^2, x2^2, x1x2
# ---------------------------------------------------------------------
# 디자인 행렬(모형 행렬) 생성
data = pd.DataFrame({
    'x1': X1,
    'x2': X2,
    'x1^2': X1**2,
    'x2^2': X2**2,
    'x1x2': X1*X2
})
data['Intercept'] = 1.0  # 절편항

# OLS 모델 적합
model = sm.OLS(Y, data[['Intercept', 'x1', 'x2', 'x1^2', 'x2^2', 'x1x2']])
results = model.fit()

# 적합 결과 요약
print(results.summary())

# ---------------------------------------------------------------------
# 4. 시각화 (3D 응답 표면)
# 예측값에 대해 3D 서피스 플롯을 그려본다.
# ---------------------------------------------------------------------
# 예측 값 계산
Y_pred = results.predict(data[['Intercept', 'x1', 'x2', 'x1^2', 'x2^2', 'x1x2']])

# 3D 플롯을 위해 메쉬 형태로 변환
X1_mesh = X1.reshape(int(np.sqrt(n_points)), int(np.sqrt(n_points)))
X2_mesh = X2.reshape(int(np.sqrt(n_points)), int(np.sqrt(n_points)))
Y_pred_mesh = Y_pred.values.reshape(int(np.sqrt(n_points)), int(np.sqrt(n_points)))

from mpl_toolkits.mplot3d import Axes3D  # 3D 그래프

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(X1_mesh, X2_mesh, Y_pred_mesh, alpha=0.5)  # 예측면
ax.scatter(X1, X2, Y, c='red', marker='o')  # 실제 관측값
ax.set_xlabel('X1')
ax.set_ylabel('X2')
ax.set_zlabel('Y')
plt.title('Response Surface')
plt.show()

# -*- coding: utf-8 -*-
"""
페이지: 8.2 다중 회귀
Excel 활용 버전: sample_car_price.xlsx의 실측 자동차 데이터로 다중 회귀를 적합하고
- 행렬식 β̂ = (X'X)⁻¹X'y로 직접 계산해 sklearn 결과와 비교
- VIF로 다중공선성 진단
- 조정된 R² 계산
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_car_price.xlsx'))
print(f"[Excel] n = {len(df)}\n", df.head(), '\n')

features = ['마력', '연비_mpg', '연식']
X = df[features].values
y = df['가격_달러'].values

# 1) 행렬식으로 β̂ 직접 계산: β̂ = (X'X)⁻¹X'y
X_design = np.column_stack([np.ones(len(X)), X])
beta_hat = np.linalg.inv(X_design.T @ X_design) @ X_design.T @ y
print("β̂ (행렬식 직접 계산):")
print(f"  절편 = {beta_hat[0]:.2f}")
for name, b in zip(features, beta_hat[1:]):
    print(f"  {name}: {b:.4f}")

# 2) sklearn 결과와 비교
X_train, X_test, y_train, y_test = train_test_split(df[features], y, test_size=0.2, random_state=42)
model = LinearRegression().fit(X_train, y_train)
print(f"\nsklearn 절편: {model.intercept_:.2f}")
for name, c in zip(features, model.coef_):
    print(f"  {name}: {c:.4f}")

# 3) 평가 지표
y_pred = model.predict(X_test)
print(f"\nMSE = {mean_squared_error(y_test, y_pred):.2f}")
print(f"R² (테스트) = {r2_score(y_test, y_pred):.4f}")

# 4) statsmodels 요약 + 조정된 R²
X_sm = sm.add_constant(df[features])
sm_m = sm.OLS(y, X_sm).fit()
print(f"\nR² (전체) = {sm_m.rsquared:.4f}")
print(f"조정된 R² = {sm_m.rsquared_adj:.4f}  ← 변수 수 보정")
print(f"F 통계 p-값 = {sm_m.f_pvalue:.4e}")

# 5) VIF 진단
vif = pd.DataFrame({
    '변수': X_sm.columns,
    'VIF': [variance_inflation_factor(X_sm.values, i) for i in range(X_sm.shape[1])]
})
print("\nVIF:")
print(vif.to_string(index=False))
print("  (VIF<5 OK, 5~10 주의, >=10 다중공선성 심각)")

# 6) 실제 vs 예측 시각화
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].scatter(y_test, y_pred, alpha=0.7)
mn, mx = y_test.min(), y_test.max()
axes[0].plot([mn, mx], [mn, mx], 'r--')
axes[0].set_xlabel('실제 가격'); axes[0].set_ylabel('예측 가격')
axes[0].set_title('실제 vs 예측'); axes[0].grid(alpha=0.3)

# 잔차 vs 예측
resid = y_test - y_pred
axes[1].scatter(y_pred, resid, alpha=0.7)
axes[1].axhline(0, color='red', linestyle='--')
axes[1].set_xlabel('예측값'); axes[1].set_ylabel('잔차')
axes[1].set_title('잔차 진단'); axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.show()

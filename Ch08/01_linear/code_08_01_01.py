# code_08_01_01.py
# -*- coding: utf-8 -*-
"""
페이지: 8.1 선형 회귀 — 광고비(독립) vs 매출(종속) 단순 선형 회귀 분석.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# 1. 가상 데이터 생성
np.random.seed(42)
ad_budget = np.random.uniform(10, 100, 50)
sales = 2.5 * ad_budget + np.random.normal(0, 10, 50)
data = pd.DataFrame({'Ad_Budget': ad_budget, 'Sales': sales})

# 2. 산점도 + 회귀선 시각화
X = data[['Ad_Budget']]
y = data['Sales']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

sk_model = LinearRegression()
sk_model.fit(X_train, y_train)

x_line = np.linspace(10, 100, 100)
y_line = sk_model.intercept_ + sk_model.coef_[0] * x_line

plt.figure(figsize=(8, 5))
plt.scatter(data['Ad_Budget'], data['Sales'], alpha=0.7, label='관측값')
plt.plot(x_line, y_line, color='red', label='회귀선')
plt.xlabel('광고비 (천 달러)')
plt.ylabel('매출 (천 달러)')
plt.title('광고비 vs 매출 — 단순 선형 회귀')
plt.legend()
plt.grid(True)
plt.show()

# 3. scikit-learn으로 모형 평가
y_pred = sk_model.predict(X_test)
print(f"기울기 β₁ : {sk_model.coef_[0]:.4f}")
print(f"절편   β₀ : {sk_model.intercept_:.4f}")
print(f"MSE        : {mean_squared_error(y_test, y_pred):.4f}")
print(f"R²         : {r2_score(y_test, y_pred):.4f}")

# 4. statsmodels로 통계 요약 (p-값 확인)
X_sm = sm.add_constant(data['Ad_Budget'])
sm_model = sm.OLS(data['Sales'], X_sm).fit()
print(sm_model.summary())

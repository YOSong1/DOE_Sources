# code_08_02_01.py
# -*- coding: utf-8 -*-
"""
페이지: 8.2 다중 회귀 — 마력, 연비, 연식으로 자동차 가격 예측.
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
from statsmodels.stats.outliers_influence import variance_inflation_factor

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# 1. 가상 데이터 생성
np.random.seed(42)
n = 100
horsepower = np.random.uniform(50, 300, n)
mpg = np.random.uniform(10, 40, n)
year = np.random.uniform(2000, 2022, n)
price = 20000 + 50 * horsepower - 1000 * mpg + 200 * (year - 2000) + np.random.normal(0, 5000, n)

data = pd.DataFrame({'Horsepower': horsepower, 'MPG': mpg, 'Year': year, 'Price': price})

# 2. 학습/테스트 분리 및 모형 적합
X = data[['Horsepower', 'MPG', 'Year']]
y = data['Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

sk_model = LinearRegression()
sk_model.fit(X_train, y_train)

# 3. 회귀 계수 출력
coef_df = pd.DataFrame({'변수': X.columns, '계수': sk_model.coef_})
print(coef_df.to_string(index=False))
print(f"절편: {sk_model.intercept_:.2f}")

# 4. 모형 평가
y_pred = sk_model.predict(X_test)
print(f"\nMSE : {mean_squared_error(y_test, y_pred):.2f}")
print(f"R²  : {r2_score(y_test, y_pred):.4f}")

# 5. VIF 계산
X_vif = sm.add_constant(X)
vif_data = pd.DataFrame({
    '변수': X_vif.columns,
    'VIF': [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
})
print("\nVIF 결과:")
print(vif_data.to_string(index=False))

# 6. 실제값 vs 예측값 시각화
plt.figure(figsize=(7, 5))
plt.scatter(y_test, y_pred, alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('실제 가격')
plt.ylabel('예측 가격')
plt.title('실제값 vs 예측값 — 다중 회귀')
plt.grid(True)
plt.show()

# 7. statsmodels 요약
X_sm = sm.add_constant(X)
sm_model = sm.OLS(y, X_sm).fit()
print(sm_model.summary())

# -*- coding: utf-8 -*-
"""
페이지: 8.1 선형 회귀
Excel 활용 버전: sample_ad_sales.xlsx를 읽어 단순 선형 회귀를 적합하고,
β₀, β₁을 정규 방정식(공분산/분산)으로 직접 계산해 OLS 결과와 일치하는지 확인,
잔차 진단(잔차 산점도, Q-Q)까지 수행한다.
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
from scipy import stats

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_ad_sales.xlsx'))
print(f"[Excel] n = {len(df)}\n", df.head(), '\n')

x = df['광고비_천달러'].values
y = df['매출_천달러'].values

# 1) OLS 공식 직접 풀이: β₁ = Σ(x-x̄)(y-ȳ) / Σ(x-x̄)², β₀ = ȳ - β₁x̄
x_bar, y_bar = x.mean(), y.mean()
beta1 = ((x - x_bar) * (y - y_bar)).sum() / ((x - x_bar)**2).sum()
beta0 = y_bar - beta1 * x_bar
print(f"수동 OLS: β₀ = {beta0:.4f}, β₁ = {beta1:.4f}")

# 2) statsmodels로 동일하게 적합 + p-value, R² 등 통계량
X = sm.add_constant(x)
model = sm.OLS(y, X).fit()
print(f"\nstatsmodels: β₀ = {model.params[0]:.4f}, β₁ = {model.params[1]:.4f}")
print(f"R² = {model.rsquared:.4f}, F p-value = {model.f_pvalue:.4e}")
print(f"β₁ t={model.tvalues[1]:.3f}, p={model.pvalues[1]:.4e}")

# 3) 예측값 / 잔차
y_hat = model.fittedvalues
resid = model.resid
print(f"\n잔차 평균 = {resid.mean():.4e} (≈0이어야 함)")
print(f"잔차 표준편차 = {resid.std(ddof=1):.4f}")

# 4) 잔차 진단 시각화
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# (a) 산점도 + 회귀선
xs = np.linspace(x.min(), x.max(), 100)
axes[0,0].scatter(x, y, alpha=0.7, label='관측치')
axes[0,0].plot(xs, beta0 + beta1 * xs, 'r-', linewidth=2, label=f'ŷ={beta0:.1f}+{beta1:.2f}x')
axes[0,0].set_title('회귀 적합')
axes[0,0].set_xlabel('광고비'); axes[0,0].set_ylabel('매출')
axes[0,0].legend(); axes[0,0].grid(alpha=0.3)

# (b) 잔차 vs 예측값
axes[0,1].scatter(y_hat, resid, alpha=0.7)
axes[0,1].axhline(0, color='red', linestyle='--')
axes[0,1].set_title('잔차 vs 예측값 (등분산성)')
axes[0,1].set_xlabel('예측 ŷ'); axes[0,1].set_ylabel('잔차')
axes[0,1].grid(alpha=0.3)

# (c) Q-Q plot
sm.qqplot(resid, line='45', fit=True, ax=axes[1,0])
axes[1,0].set_title('Q-Q plot (정규성)')

# (d) 잔차 히스토그램
axes[1,1].hist(resid, bins=15, color='steelblue', alpha=0.7, edgecolor='white')
axes[1,1].set_title('잔차 히스토그램')
axes[1,1].set_xlabel('잔차')
plt.tight_layout()
plt.show()

# 5) 결과 해석
print(f"\n[해석] 광고비가 1천 달러 증가하면 매출이 평균 {beta1:.2f}천 달러 증가합니다.")
print(f"      R²={model.rsquared:.3f} → 모델이 매출 변동의 {model.rsquared*100:.1f}%를 설명합니다.")

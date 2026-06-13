# -*- coding: utf-8 -*-
"""
페이지: 6.2 지수 분포
Excel 활용 버전: sample_call_intervals.xlsx의 콜센터 대기시간 데이터를 읽어
λ̂ = 1/평균을 적률추정량으로 계산하고, 6.2절의 확률을 재계산한다.
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
from scipy.stats import expon

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_call_intervals.xlsx'))
print(f"[Excel] 표본 크기 n = {len(df)}")
print(df.describe(), '\n')

# 1) 적률추정: E[X] = 1/λ → λ̂ = 1/x̄
x_bar = df['대기시간_분'].mean()
lambda_hat = 1 / x_bar
scale_hat = x_bar  # SciPy의 scale = 1/λ
print(f"표본평균 x̄ = {x_bar:.4f}분")
print(f"λ̂ = 1/x̄ = {lambda_hat:.4f} (분당 평균 사건 수)")

# 2) PDF 공식의 각 항 의미 (x = 1분에서)
x = 1.0
pdf_val = lambda_hat * np.exp(-lambda_hat * x)
print(f"\n--- f(x={x}) = λ·exp(-λx) 직접 계산 ---")
print(f"  λ̂·exp(-λ̂·x) = {lambda_hat:.4f} × exp({-lambda_hat*x:.4f}) = {pdf_val:.6f}")
print(f"  scipy 계산값  = {expon.pdf(x, scale=scale_hat):.6f}")

# 3) 핵심 확률 재계산
p_within_1 = expon.cdf(1, scale=scale_hat)
p_over_2 = expon.sf(2, scale=scale_hat)
median = expon.ppf(0.5, scale=scale_hat)
print(f"\nP(X<=1) = {p_within_1:.4f}  (1 - exp(-λ·1) = {1 - np.exp(-lambda_hat):.4f})")
print(f"P(X>2)  = {p_over_2:.4f}")
print(f"중앙값  = {median:.4f}분  (이론값: ln2/λ = {np.log(2)/lambda_hat:.4f})")

# 4) 실측 대 이론 비교
obs_under_1 = (df['대기시간_분'] <= 1).mean()
print(f"\n[해석] 실제 표본에서 1분 이내 비율 = {obs_under_1:.4f}")
print(f"       이론(지수분포) 예측치        = {p_within_1:.4f}")

# 5) 히스토그램 + 추정 PDF
xs = np.linspace(0, df['대기시간_분'].max(), 200)
plt.figure(figsize=(8, 5))
plt.hist(df['대기시간_분'], bins=30, density=True, alpha=0.5,
         color='steelblue', edgecolor='white', label='관측치')
plt.plot(xs, expon.pdf(xs, scale=scale_hat), 'r-', linewidth=2,
         label=rf'$\hat\lambda$={lambda_hat:.2f} 지수분포 PDF')
plt.title('콜센터 대기시간 분포')
plt.xlabel('대기시간 (분)')
plt.ylabel('밀도')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# -*- coding: utf-8 -*-
"""
페이지: 6.6 감마 분포
Excel 활용 버전: sample_insurance_claims.xlsx의 청구 간격 데이터로
적률추정(MoM)을 통해 α, β를 추정하고 PDF를 적합한다.
적률추정: x̄ = α/β,  s² = α/β²  →  β̂ = x̄/s²,  α̂ = x̄·β̂
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
from scipy.stats import gamma

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_insurance_claims.xlsx'))
print(f"[Excel] n = {len(df)}\n", df.describe(), '\n')

x = df['청구간격_일'].values
x_bar = x.mean()
s2 = x.var(ddof=1)

# 1) 적률추정
beta_hat = x_bar / s2
alpha_hat = x_bar * beta_hat
scale_hat = 1 / beta_hat
print(f"표본평균 x̄ = {x_bar:.4f}, 표본분산 s² = {s2:.4f}")
print(f"적률추정: β̂ = x̄/s² = {beta_hat:.4f}")
print(f"          α̂ = x̄·β̂ = {alpha_hat:.4f}")

# 2) MLE도 비교 (scipy.stats.gamma.fit)
shape_mle, loc_mle, scale_mle = gamma.fit(x, floc=0)
print(f"\n최대우도(MLE): α̂={shape_mle:.4f}, scale={scale_mle:.4f} (β̂={1/scale_mle:.4f})")

# 3) 추정된 모수로 핵심 확률 재계산
p_2days = gamma.cdf(2, a=alpha_hat, scale=scale_hat)
p90 = gamma.ppf(0.90, a=alpha_hat, scale=scale_hat)
print(f"\nP(X<=2일) = {p_2days:.4f}")
print(f"90번째 백분위수 = {p90:.4f}일")

# 4) 히스토그램 + 적합 PDF
xs = np.linspace(0.01, x.max(), 300)
plt.figure(figsize=(8, 5))
plt.hist(x, bins=30, density=True, alpha=0.5, color='steelblue',
         edgecolor='white', label='관측치')
plt.plot(xs, gamma.pdf(xs, a=alpha_hat, scale=scale_hat),
         'r-', linewidth=2, label=f'MoM: α̂={alpha_hat:.2f}, β̂={beta_hat:.2f}')
plt.plot(xs, gamma.pdf(xs, a=shape_mle, scale=scale_mle),
         'g--', linewidth=2, label=f'MLE: α̂={shape_mle:.2f}')
plt.title('보험 청구 간격 — 감마 분포 적합')
plt.xlabel('간격(일)')
plt.ylabel('밀도')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# 5) 결과 해석
print("\n[해석] MoM과 MLE 추정치가 비슷하다면 감마 분포가 잘 맞는 모형입니다.")

# -*- coding: utf-8 -*-
"""
페이지: 6.1 정규 분포
Excel 활용 버전: sample_scores.xlsx의 실제 시험 점수 데이터를 읽어
표본 평균/표준편차를 추정한 뒤, 그 추정치로 정규 분포 N(μ̂, σ̂²)을 가정해
6.1절의 확률 계산 절차를 재현한다.
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
from scipy.stats import norm

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_scores.xlsx'))
print(f"[Excel] 표본 크기 n = {len(df)}")
print(df.head(), '\n')

# 1) 표본 통계량으로 모수 추정 (μ̂ = 표본평균, σ̂ = 표본표준편차)
mu_hat = df['시험점수'].mean()
sigma_hat = df['시험점수'].std(ddof=1)
print(f"표본평균 μ̂ = {mu_hat:.4f}")
print(f"표본표준편차 σ̂ = {sigma_hat:.4f}")

# 2) 6.1절 수식의 각 항을 명시적으로 풀어 출력
print("\n--- 정규분포 PDF 공식의 각 항 (x=80에서 확인) ---")
x = 80
z = (x - mu_hat) / sigma_hat
print(f"표준화 z = (x - μ̂) / σ̂ = ({x} - {mu_hat:.2f}) / {sigma_hat:.2f} = {z:.4f}")
pdf_val = (1 / (sigma_hat * np.sqrt(2*np.pi))) * np.exp(-z**2 / 2)
print(f"f(x={x}) 직접 계산 = {pdf_val:.6f}")
print(f"f(x={x}) scipy 계산 = {norm.pdf(x, mu_hat, sigma_hat):.6f}")

# 3) 책 본문과 동일한 확률 계산을 표본 추정치로 재수행
p_over_80 = norm.sf(80, loc=mu_hat, scale=sigma_hat)
p_60_80 = norm.cdf(80, loc=mu_hat, scale=sigma_hat) - norm.cdf(60, loc=mu_hat, scale=sigma_hat)
cutoff = norm.ppf(0.90, loc=mu_hat, scale=sigma_hat)
ci = norm.interval(0.95, loc=mu_hat, scale=sigma_hat)
print(f"\nP(X>=80) = {p_over_80:.4f}  ({p_over_80*100:.2f}%)")
print(f"P(60<=X<=80) = {p_60_80:.4f}  ({p_60_80*100:.2f}%)")
print(f"상위 10% 컷오프 = {cutoff:.2f}점")
print(f"95% 신뢰구간 = [{ci[0]:.2f}, {ci[1]:.2f}]")

# 4) 결과 해석 (실데이터와의 비교)
obs_over_80 = (df['시험점수'] >= 80).mean()
print(f"\n[해석] 실제 표본에서 80점 이상 비율 = {obs_over_80:.4f}")
print(f"       정규근사 예측치 = {p_over_80:.4f}")
print("       표본 비율과 정규근사 확률이 비슷할수록 정규분포 가정이 타당합니다.")

# 5) 히스토그램 + 추정 정규 PDF
xs = np.linspace(df['시험점수'].min(), df['시험점수'].max(), 200)
plt.figure(figsize=(8, 5))
plt.hist(df['시험점수'], bins=20, density=True, alpha=0.5, color='steelblue',
         edgecolor='white', label='관측치 히스토그램')
plt.plot(xs, norm.pdf(xs, mu_hat, sigma_hat), 'r-', linewidth=2,
         label=f'N(μ̂={mu_hat:.1f}, σ̂={sigma_hat:.1f})')
plt.title('시험 점수: 관측 분포 vs 추정 정규 분포')
plt.xlabel('점수')
plt.ylabel('밀도')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

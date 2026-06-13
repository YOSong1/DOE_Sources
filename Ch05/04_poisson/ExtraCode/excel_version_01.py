import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.4 포아송 — Excel 버전
# 시간당 콜센터 전화 수 데이터로부터 lambda를 추정하고
# "평균=분산" 특성과 PMF 적합도를 평가한다.

import os
import numpy as np
import pandas as pd
from scipy.stats import poisson

HERE = os.path.dirname(os.path.abspath(__file__))
xlsx = os.path.join(HERE, "sample_data.xlsx")

df = pd.read_excel(xlsx, sheet_name="callcenter")
print("=== [1] 데이터 구조 ===")
print(df.head())
print(f"... 총 {len(df)} 시간 관측")

calls = df["calls"].values
N = len(calls)

# λ MLE = 표본 평균
lam_hat = calls.mean()
print(f"\n=== [2] λ 추정 (MLE = 표본평균) ===")
print(f"  λ_hat = sum(X)/N = {calls.sum()}/{N} = {lam_hat:.4f}")

# 평균=분산 진단
mean_obs = calls.mean()
var_obs = calls.var(ddof=0)
ratio = var_obs / mean_obs if mean_obs > 0 else float('nan')
print(f"\n=== [3] 평균 vs 분산 (포아송이면 둘이 같아야 함) ===")
print(f"  표본 평균   = {mean_obs:.4f}")
print(f"  표본 분산   = {var_obs:.4f}")
print(f"  분산/평균   = {ratio:.4f}  (1에 가까우면 포아송 적합)")
if ratio > 1.3:
    print("  -> 과산포(overdispersion) 의심 (음이항 분포 고려)")
elif ratio < 0.7:
    print("  -> 과소산포(underdispersion) 의심")
else:
    print("  -> 포아송 모형 적합")

# PMF 적합도
print(f"\n=== [4] 관측 빈도 vs 기대 빈도 (총 {N}시간) ===")
max_k = int(calls.max()) + 2
chi2 = 0.0
print(f"  {'k':>3} | {'관측':>5} | {'기대':>7} | {'P(X=k)':>8}")
for k in range(max_k+1):
    obs = int((calls == k).sum())
    pk = poisson.pmf(k, lam_hat)
    exp = N * pk
    if exp > 1:
        chi2 += (obs - exp)**2 / exp
    print(f"  {k:>3} | {obs:>5} | {exp:>7.2f} | {pk:>8.4f}")
print(f"  카이제곱 = {chi2:.3f}")

# 운영 의사결정 예: 시간당 8건 초과 확률
print(f"\n=== [5] 운영 의사결정 ===")
print(f"  P(X > 8) = {poisson.sf(8, lam_hat):.4f}")
print(f"  P(X > 10) = {poisson.sf(10, lam_hat):.4f}")
print(f"  95% 분위수 = {poisson.ppf(0.95, lam_hat):.0f}건/시간")

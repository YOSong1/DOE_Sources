import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.3 이항 — Excel 버전
# 100배치(각 n=10)의 불량 개수 데이터로부터 p_hat을 추정하고
# 이항 분포 PMF 적합도를 평가한다.

import os
import numpy as np
import pandas as pd
from scipy.stats import binom

HERE = os.path.dirname(os.path.abspath(__file__))
xlsx = os.path.join(HERE, "sample_data.xlsx")

df = pd.read_excel(xlsx, sheet_name="inspections")
print("=== [1] 데이터 구조 ===")
print(df.head())
print(f"... 총 {len(df)} 배치")

n = int(df["n_inspected"].iloc[0])
NB = len(df)

# 1) p 추정: 전체 검사 중 불량 비율
total_inspected = NB * n
total_defects = int(df["defects"].sum())
p_hat = total_defects / total_inspected
print(f"\n=== [2] 모수 추정 ===")
print(f"  총 검사 수 = {NB} * {n} = {total_inspected}")
print(f"  총 불량 수 = {total_defects}")
print(f"  p_hat = {total_defects}/{total_inspected} = {p_hat:.4f}")

# 2) 표본 평균/분산
mean_obs = df["defects"].mean()
var_obs = df["defects"].var(ddof=0)
print(f"\n=== [3] 표본 통계량 vs 이항 이론값 (n={n}, p_hat={p_hat:.4f}) ===")
print(f"  표본 평균 = {mean_obs:.4f},   이론 np    = {n*p_hat:.4f}")
print(f"  표본 분산 = {var_obs:.4f},   이론 np(1-p) = {n*p_hat*(1-p_hat):.4f}")

# 3) 관측 빈도 vs 기대 빈도
print(f"\n=== [4] 관측 빈도 vs 기대 빈도 (배치 {NB}개) ===")
print(f"  {'k':>3} | {'관측':>5} | {'기대':>7} | {'P(X=k)':>8}")
print("  " + "-"*36)
chi2 = 0.0
for k in range(n+1):
    obs = int((df["defects"] == k).sum())
    pk = binom.pmf(k, n, p_hat)
    exp = NB * pk
    if exp > 0:
        chi2 += (obs - exp)**2 / exp
    print(f"  {k:>3} | {obs:>5} | {exp:>7.2f} | {pk:>8.4f}")
print(f"\n  카이제곱 통계량 = {chi2:.3f} (자유도={n})")

# 4) 누적 확률 예시
print(f"\n=== [5] 누적 확률 ===")
print(f"  P(X <= 1) = {binom.cdf(1, n, p_hat):.4f}")
print(f"  P(X >= 3) = {binom.sf(2, n, p_hat):.4f}")

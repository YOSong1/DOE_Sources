import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.6 초기하 — Excel 버전
# 비복원 추출 데이터(부품 검사 200회)로부터 표본 통계량을 계산하고
# 이항 근사와 비교, 유한 모집단 보정계수의 효과를 확인한다.

import os
import numpy as np
import pandas as pd
from scipy.stats import hypergeom, binom

HERE = os.path.dirname(os.path.abspath(__file__))
xlsx = os.path.join(HERE, "sample_data.xlsx")

df = pd.read_excel(xlsx, sheet_name="hyper_inspect")
print("=== [1] 데이터 구조 ===")
print(df.head())
print(f"... 라운드 {len(df)}")

M = int(df["M_population"].iloc[0])
n = int(df["n_defects_in_pop"].iloc[0])
N = int(df["N_sample_size"].iloc[0])
samples = df["k_defects_in_sample"].values
R = len(samples)

print(f"\n=== [2] 모수 ===")
print(f"  M={M}, n={n}, N={N}, 표본 비율 N/M = {N/M:.3f}")
p_pop = n / M
print(f"  모집단 불량률 p = n/M = {p_pop:.3f}")

# 표본 통계량
mean_obs = samples.mean()
var_obs = samples.var(ddof=0)
print(f"\n=== [3] 표본 통계량 ===")
print(f"  표본 평균 = {mean_obs:.4f}")
print(f"  표본 분산 = {var_obs:.4f}")

# 이론 (초기하)
mean_h = hypergeom.mean(M, n, N)
var_h = hypergeom.var(M, n, N)
# 이론 (이항: 복원 추출 가정)
mean_b = N * p_pop
var_b = N * p_pop * (1 - p_pop)
fpc = (M - N) / (M - 1)
print(f"\n=== [4] 이론값 비교 ===")
print(f"  초기하 E[X]   = {mean_h:.4f}     이항 E[X] = {mean_b:.4f}")
print(f"  초기하 Var(X) = {var_h:.4f}     이항 Var(X) = {var_b:.4f}")
print(f"  유한 모집단 보정 (M-N)/(M-1) = {fpc:.4f}")
print(f"  이항 Var * FPC = {var_b * fpc:.4f} (=초기하 Var)")

# PMF 비교 표
print(f"\n=== [5] 관측 빈도 vs 기대 빈도 (초기하 vs 이항) ===")
print(f"  {'k':>3} | {'관측':>4} | {'기대(초기하)':>12} | {'기대(이항)':>10}")
for k in range(N+1):
    obs = int((samples == k).sum())
    exp_h = R * hypergeom.pmf(k, M, n, N)
    exp_b = R * binom.pmf(k, N, p_pop)
    print(f"  {k:>3} | {obs:>4} | {exp_h:>12.2f} | {exp_b:>10.2f}")

# 표본 비율이 5% 미만이면 이항 근사 OK
if N / M < 0.05:
    print("\n  (N/M < 5%) -> 이항 근사 충분")
else:
    print("\n  (N/M >= 5%) -> 이항 근사 부적합. 초기하 사용 권장")

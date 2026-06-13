import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.8 포아송-이항 — Excel 버전
# 30경기 각 경기별 승률 p_i를 읽어 시즌 총 승수 분포(포아송-이항)를 계산하고
# 이항/포아송 근사와 비교한다.

import os
import numpy as np
import pandas as pd
from scipy.stats import binom, poisson

HERE = os.path.dirname(os.path.abspath(__file__))
xlsx = os.path.join(HERE, "sample_data.xlsx")

df = pd.read_excel(xlsx, sheet_name="season")
print("=== [1] 시즌 일정 ===")
print(df.head(10))
print(f"... 총 {len(df)} 경기")

probs = df["p_i_win_prob"].values
n = len(probs)
realized_wins = int(df["win"].sum())

# DP로 PMF 계산
def poibin_pmf(probs):
    n = len(probs)
    dp = np.zeros(n+1); dp[0] = 1.0
    for i, p in enumerate(probs):
        for k in range(i+1, 0, -1):
            dp[k] = dp[k] * (1-p) + dp[k-1] * p
        dp[0] *= (1-p)
    return dp

pmf = poibin_pmf(probs)

# 평균/분산
mean_pb = probs.sum()
var_pb = np.sum(probs * (1 - probs))
print(f"\n=== [2] 포아송-이항 모멘트 ===")
print(f"  E[X] = Σ p_i = {mean_pb:.4f}")
print(f"  Var(X) = Σ p_i(1-p_i) = {var_pb:.4f}")
print(f"  실현 승수(이번 시즌) = {realized_wins}")

# 이항 근사: p_bar = mean(p_i)
p_bar = probs.mean()
mean_bin = n * p_bar
var_bin = n * p_bar * (1 - p_bar)
print(f"\n=== [3] 이항 근사 B(n, p_bar) ===")
print(f"  p_bar = {p_bar:.4f}")
print(f"  E_bin = n*p_bar = {mean_bin:.4f}  (포아송-이항 평균과 동일)")
print(f"  Var_bin = n*p_bar*(1-p_bar) = {var_bin:.4f}")
print(f"  Var 차이(이항-PB) = {var_bin - var_pb:.4f} (이항이 약간 크다: p_i 분산만큼)")

# 포아송 근사 (Le Cam): λ = Σp_i
lam = mean_pb
print(f"\n=== [4] 포아송 근사 Poisson(λ=Σp_i) ===")
print(f"  λ = {lam:.4f}")
le_cam_bound = 2 * np.sum(probs ** 2)
print(f"  Le Cam 상한 (총변동) = 2*Σp_i^2 = {le_cam_bound:.4f}")

# PMF 비교 표
print(f"\n=== [5] PMF 비교 (k, 포아송-이항, 이항, 포아송) ===")
for k in range(n+1):
    p_pb = pmf[k]
    p_bn = binom.pmf(k, n, p_bar)
    p_po = poisson.pmf(k, lam)
    if p_pb > 1e-5 or p_bn > 1e-5 or p_po > 1e-5:
        print(f"  k={k:>2}  PB={p_pb:.4f}  Bin={p_bn:.4f}  Poi={p_po:.4f}")

# 의사결정 예: 시즌 18승 이상 확률
THR = 18
prob_ge = pmf[THR:].sum()
print(f"\n=== [6] 의사결정 ===")
print(f"  P(X >= {THR}) = {prob_ge:.4f}  (시즌 {THR}승 이상 확률)")

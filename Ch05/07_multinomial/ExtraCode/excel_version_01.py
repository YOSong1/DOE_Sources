import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.7 다항 — Excel 버전
# 500명 객관식 응답으로부터 p_i를 추정하고
# 다항 PMF 평가, 카이제곱 적합도 검정을 수행한다.

import os
import numpy as np
import pandas as pd
from scipy.stats import multinomial, chisquare

HERE = os.path.dirname(os.path.abspath(__file__))
xlsx = os.path.join(HERE, "sample_data.xlsx")

# 1) 응답 로드
df = pd.read_excel(xlsx, sheet_name="frequency")
print("=== [1] 빈도 데이터 ===")
print(df)

choices = df["choice"].tolist()
obs = df["observed"].values.astype(int)
N = int(obs.sum())
print(f"\n총 응답 수 N = {N}")

# 2) p_i 추정
p_hat = obs / N
print(f"\n=== [2] 카테고리별 p_i 추정 ===")
for c, o, p in zip(choices, obs, p_hat):
    print(f"  {c}: 관측={o}, p_hat={p:.4f}")
assert abs(p_hat.sum() - 1.0) < 1e-9, "p_hat 합은 1이어야 함"

# 3) 기댓값, 분산, 공분산 일부
print(f"\n=== [3] 다항 분포 모멘트 ===")
for c, p in zip(choices, p_hat):
    print(f"  {c}: E[X]={N*p:.2f}, Var(X)={N*p*(1-p):.3f}")
print(f"  Cov(A,B) = -N*p_A*p_B = {-N*p_hat[0]*p_hat[1]:.4f}")

# 4) 다항 PMF 값 (관측 결과 자체의 확률)
pmf_obs = multinomial.pmf(obs.tolist(), N, p_hat.tolist())
print(f"\n=== [4] 관측 결과의 다항 PMF 값 ===")
print(f"  P(X = observed | p_hat) = {pmf_obs:.6e}")
# logpmf for stable
log_pmf = multinomial.logpmf(obs.tolist(), N, p_hat.tolist())
print(f"  logP = {log_pmf:.4f}")

# 5) 카이제곱 적합도: 균등 분포(귀무가설) vs 관측
print(f"\n=== [5] 카이제곱 적합도 (귀무 H0: 균등 0.2씩) ===")
exp_uniform = np.full_like(obs, fill_value=N/len(choices), dtype=float)
chi2, pval = chisquare(obs, f_exp=exp_uniform)
print(f"  관측 = {obs.tolist()}")
print(f"  기대 = {exp_uniform.tolist()}")
print(f"  χ² = {chi2:.3f}, p-value = {pval:.4f}")
if pval < 0.05:
    print("  -> H0 기각: 균등 분포가 아닐 가능성 높음")
else:
    print("  -> H0 기각 못함")

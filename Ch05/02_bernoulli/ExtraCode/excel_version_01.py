import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.2 베르누이 — Excel 버전
# 광고 클릭 0/1 데이터를 읽어 p_hat을 추정하고, 이론 분포와 비교한다.

import os
import numpy as np
import pandas as pd
from scipy.stats import bernoulli

HERE = os.path.dirname(os.path.abspath(__file__))
xlsx = os.path.join(HERE, "sample_data.xlsx")

print("=== [1] Excel 데이터 구조 ===")
df = pd.read_excel(xlsx, sheet_name="ad_clicks")
print(f"행 수={len(df)}, 컬럼={list(df.columns)}")
print(df.head())

# 베르누이 시행 데이터로부터 p 추정
N = len(df)
S = int(df["clicked"].sum())
p_hat = S / N
print(f"\n=== [2] 성공 확률 p 추정 (MLE) ===")
print(f"  N = {N}, 성공(클릭) 수 S = {S}")
print(f"  p_hat = S/N = {S}/{N} = {p_hat:.4f}")

# 이론 기댓값/분산을 추정 p로 평가
print("\n=== [3] 추정 분포의 모수 ===")
print(f"  E[X] = p_hat       = {bernoulli.mean(p_hat):.4f}")
print(f"  Var[X] = p_hat(1-p_hat) = {bernoulli.var(p_hat):.4f}")

# 표본평균/표본분산
sample_mean = df["clicked"].mean()
sample_var = df["clicked"].var(ddof=0)
print("\n=== [4] 표본 통계량과 비교 ===")
print(f"  표본 평균 = {sample_mean:.4f}  (이론 E와 동일해야 함)")
print(f"  표본 분산 = {sample_var:.4f}  (이론 Var과 거의 동일)")

# Wald 95% CI
se = np.sqrt(p_hat * (1 - p_hat) / N)
ci = (p_hat - 1.96 * se, p_hat + 1.96 * se)
print(f"\n=== [5] p의 95% Wald 신뢰구간 ===")
print(f"  SE = sqrt(p(1-p)/N) = {se:.5f}")
print(f"  95% CI = [{ci[0]:.4f}, {ci[1]:.4f}]")

# 베르누이 모형 적합도 (성공/실패 빈도 vs 기대)
print("\n=== [6] 적합도 (관측 vs 기대) ===")
obs1, obs0 = S, N - S
exp1, exp0 = N * p_hat, N * (1 - p_hat)
print(f"  성공: 관측={obs1}, 기대={exp1:.1f}")
print(f"  실패: 관측={obs0}, 기대={exp0:.1f}")

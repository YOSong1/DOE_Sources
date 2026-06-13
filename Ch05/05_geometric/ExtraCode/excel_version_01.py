import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.5 기하 — Excel 버전
# 가챠 유저별 첫 SSR까지 시도 횟수를 읽어 p_hat을 추정하고
# 기하 분포의 PMF 적합도, 무기억성 점검을 한다.

import os
import numpy as np
import pandas as pd
from scipy.stats import geom

HERE = os.path.dirname(os.path.abspath(__file__))
xlsx = os.path.join(HERE, "sample_data.xlsx")

df = pd.read_excel(xlsx, sheet_name="gacha")
print("=== [1] 데이터 구조 ===")
print(df.head())
print(f"... N = {len(df)} 유저")

trials = df["trials_to_first_SSR"].values
N = len(trials)

# 1) p MLE = 1 / mean(X)
mean_trials = trials.mean()
p_hat = 1.0 / mean_trials
print(f"\n=== [2] p 추정 (MLE = 1/평균시도) ===")
print(f"  평균 시도 횟수 = {mean_trials:.4f}")
print(f"  p_hat = 1/mean = {p_hat:.4f}")

# 이론 평균 1/p, 분산 (1-p)/p^2
print(f"\n=== [3] 표본 vs 이론 ===")
print(f"  표본 평균 = {trials.mean():.3f}, 이론 1/p = {1/p_hat:.3f}")
print(f"  표본 분산 = {trials.var(ddof=0):.3f}, 이론 (1-p)/p^2 = {(1-p_hat)/p_hat**2:.3f}")

# 2) 빈도 vs 기대 (k=1..15)
print(f"\n=== [4] 관측 빈도 vs 기대 빈도 ===")
print(f"  {'k':>3} | {'관측':>5} | {'기대':>7} | {'P(X=k)':>8}")
for k in range(1, 16):
    obs = int((trials == k).sum())
    pk = geom.pmf(k, p_hat)
    exp = N * pk
    print(f"  {k:>3} | {obs:>5} | {exp:>7.2f} | {pk:>8.4f}")

# 3) 무기억성 점검: P(X > s+t | X > s) ≈ P(X > t)
print(f"\n=== [5] 무기억성 점검 (메모리리스) ===")
s, t = 10, 5
# 경험적 조건부 확률
emp_cond = ((trials > s + t).sum()) / max(1, (trials > s).sum())
emp_uncon = (trials > t).sum() / N
theo = (1 - p_hat) ** t
print(f"  경험 P(X > {s+t} | X > {s}) = {emp_cond:.4f}")
print(f"  경험 P(X > {t})            = {emp_uncon:.4f}")
print(f"  이론 (1-p)^{t}            = {theo:.4f}")

# 4) 운영 지표
print(f"\n=== [6] 운영 지표 ===")
print(f"  50% 유저가 첫 SSR 뽑는 시도수 (메디안 분위수) = {geom.ppf(0.5, p_hat):.0f}")
print(f"  90% 유저가 도달하는 시도수 = {geom.ppf(0.9, p_hat):.0f}")

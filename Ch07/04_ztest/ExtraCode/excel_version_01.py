# -*- coding: utf-8 -*-
"""
페이지: 7.4 Z-검정
Excel 활용 버전: sample_ztest.xlsx의 두 시트로 단일 표본 평균 Z검정,
두 비율 Z검정(A/B광고)을 raw 클릭 로그에서 직접 집계해 수행한다.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'sample_ztest.xlsx')

# === (1) 평균 Z검정: 수면 시간 ===
print("=" * 60)
print("(1) 단일표본 Z검정 — 평균 수면 시간 vs 7시간")
print("=" * 60)
df_s = pd.read_excel(XLSX, sheet_name='수면시간')
x = df_s['수면시간_h'].values
n = len(x)
sigma = 1.5  # 모표준편차 알려진 것으로 가정
mu_0 = 7.0
x_bar = x.mean()
SE = sigma / np.sqrt(n)
Z = (x_bar - mu_0) / SE
p_two = 2 * (1 - stats.norm.cdf(abs(Z)))
print(f"n={n}, x̄={x_bar:.4f}, σ={sigma}, SE=σ/√n={SE:.4f}")
print(f"Z = (x̄-μ₀)/SE = {Z:.4f}")
print(f"p-값(양측) = {p_two:.4f}")
print(f"95% 신뢰구간: [{x_bar - 1.96*SE:.3f}, {x_bar + 1.96*SE:.3f}]시간")

# === (2) 두 비율 Z검정: A광고 vs B광고 클릭률 (raw 로그에서 집계) ===
print("\n" + "=" * 60)
print("(2) 두 비율 Z검정 — A/B 광고 클릭률")
print("=" * 60)
df_ab = pd.read_excel(XLSX, sheet_name='AB광고전환')
clicks_a = df_ab['광고A_클릭'].sum()
clicks_b = df_ab['광고B_클릭'].sum()
n_a = n_b = len(df_ab)
print(f"광고A: {clicks_a}/{n_a} 클릭 = {clicks_a/n_a:.4f}")
print(f"광고B: {clicks_b}/{n_b} 클릭 = {clicks_b/n_b:.4f}")

z_stat, p_val = proportions_ztest([clicks_a, clicks_b], [n_a, n_b])
print(f"\nZ = {z_stat:.4f}, p(양측) = {p_val:.4f}")

# 수동 검산
p1, p2 = clicks_a/n_a, clicks_b/n_b
p_pool = (clicks_a + clicks_b) / (n_a + n_b)
se_pool = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
Z_manual = (p1 - p2) / se_pool
print(f"수동: p_pool={p_pool:.4f}, SE_pool={se_pool:.5f}, Z={Z_manual:.4f}")

# 효과 크기: 두 비율의 절대 차이
diff = p1 - p2
diff_ci = (diff - 1.96 * np.sqrt(p1*(1-p1)/n_a + p2*(1-p2)/n_b),
           diff + 1.96 * np.sqrt(p1*(1-p1)/n_a + p2*(1-p2)/n_b))
print(f"\n비율 차이 = {diff:.4f}, 95% CI = [{diff_ci[0]:.4f}, {diff_ci[1]:.4f}]")
if p_val < 0.05:
    print(f"[해석] 광고 A의 클릭률이 통계적으로 더 높음 (차이 {diff*100:.2f}%p)")
else:
    print("[해석] 두 광고의 클릭률 차이가 통계적으로 유의하지 않음")

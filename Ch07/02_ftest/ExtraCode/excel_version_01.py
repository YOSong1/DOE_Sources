# -*- coding: utf-8 -*-
"""
페이지: 7.2 F-검정
Excel 활용 버전: sample_variance_anova.xlsx의 두 시트를 활용해
분산비 F검정과 일원 ANOVA를 모두 수행하고, F = MS_between/MS_within 분해를 직접 검산.
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

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'sample_variance_anova.xlsx')

# === (1) 분산비 F검정 ===
print("=" * 60)
print("(1) 분산비 F검정 — Line A vs Line B")
print("=" * 60)
df_line = pd.read_excel(XLSX, sheet_name='생산라인')
a = df_line['LineA'].values
b = df_line['LineB'].values
va, vb = a.var(ddof=1), b.var(ddof=1)
print(f"Var(A)={va:.4f}, Var(B)={vb:.4f}")
F = max(va, vb) / min(va, vb)
dfn, dfd = (len(a)-1, len(b)-1) if va >= vb else (len(b)-1, len(a)-1)
cdf = stats.f.cdf(F, dfn, dfd)
p_two = 2 * min(cdf, 1 - cdf)
print(f"F = {F:.4f} (df1={dfn}, df2={dfd}), p(양측) = {p_two:.4f}")
# Levene 권장 검정도 보고
lev = stats.levene(a, b)
print(f"Levene (정규성에 덜 민감): W={lev.statistic:.4f}, p={lev.pvalue:.4f}")

# === (2) 일원 ANOVA: 세 비료 ===
print("\n" + "=" * 60)
print("(2) 일원 ANOVA — 비료 A/B/C")
print("=" * 60)
df_fer = pd.read_excel(XLSX, sheet_name='비료성장')
groups = [df_fer['비료A'].dropna().values,
          df_fer['비료B'].dropna().values,
          df_fer['비료C'].dropna().values]
labels = ['A', 'B', 'C']
for lab, g in zip(labels, groups):
    print(f"  비료 {lab}: n={len(g)}, 평균={g.mean():.3f}, sd={g.std(ddof=1):.3f}")

# scipy ANOVA
F_stat, p_val = stats.f_oneway(*groups)
print(f"\nscipy ANOVA: F = {F_stat:.4f}, p = {p_val:.4f}")

# 직접 분해: SS_between, SS_within
N = sum(len(g) for g in groups)
k = len(groups)
grand = np.concatenate(groups).mean()
SS_between = sum(len(g) * (g.mean() - grand)**2 for g in groups)
SS_within = sum(((g - g.mean())**2).sum() for g in groups)
MS_between = SS_between / (k - 1)
MS_within = SS_within / (N - k)
F_manual = MS_between / MS_within
print(f"\n--- ANOVA 분해 검산 ---")
print(f"SS_between = Σ nᵢ(ȳᵢ - ȳ)² = {SS_between:.4f}")
print(f"SS_within  = ΣΣ (yᵢⱼ - ȳᵢ)² = {SS_within:.4f}")
print(f"MS_between = SS_b / (k-1) = {MS_between:.4f}")
print(f"MS_within  = SS_w / (N-k) = {MS_within:.4f}")
print(f"F = MS_between / MS_within = {F_manual:.4f}  (scipy: {F_stat:.4f})")

if p_val < 0.05:
    print("\n[해석] 세 비료 중 적어도 하나의 평균이 다름 → 사후검정 Tukey HSD 필요")
else:
    print("\n[해석] 비료 간 평균 차이가 통계적으로 유의하지 않음")

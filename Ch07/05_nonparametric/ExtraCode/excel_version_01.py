# -*- coding: utf-8 -*-
"""
페이지: 7.5 비모수 검정
Excel 활용 버전: sample_nonparam.xlsx의 세 시트로 세 가지 비모수 검정을 모두 수행.
- 정규성 검정(Shapiro-Wilk)으로 비모수 사용을 정당화
- 동일 데이터에 모수 검정(t/ANOVA)도 적용해 결과 차이를 비교
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
XLSX = os.path.join(HERE, 'sample_nonparam.xlsx')

# === (1) 만-위트니 U vs 독립표본 t ===
print("=" * 60)
print("(1) 만-위트니 U — A/B 그룹 클릭시간")
print("=" * 60)
df_ab = pd.read_excel(XLSX, sheet_name='클릭시간')
gA = df_ab['GroupA'].dropna().values
gB = df_ab['GroupB'].dropna().values
for label, g in [('A', gA), ('B', gB)]:
    sw = stats.shapiro(g)
    print(f"  Group{label}: n={len(g)}, 중앙값={np.median(g):.3f}, "
          f"Shapiro p={sw.pvalue:.4f}")

u_stat, p_u = stats.mannwhitneyu(gA, gB, alternative='two-sided')
t_stat, p_t = stats.ttest_ind(gA, gB, equal_var=False)
print(f"\nMann-Whitney U: {u_stat:.4f}, p = {p_u:.4f}")
print(f"독립 t-검정   : t = {t_stat:.4f}, p = {p_t:.4f}")
print(f"[해석] 정규성 위반 → Mann-Whitney 결과를 우선 보고")

# === (2) 윌콕슨 부호 순위 vs 대응 t ===
print("\n" + "=" * 60)
print("(2) Wilcoxon 부호 순위 — 명상 전후 스트레스")
print("=" * 60)
df_w = pd.read_excel(XLSX, sheet_name='명상스트레스')
before = df_w['전'].values
after = df_w['후'].values
diff = before - after
print(f"n={len(diff)}, 차이 중앙값={np.median(diff):.3f}")
w_stat, p_w = stats.wilcoxon(before, after, alternative='two-sided')
t_p_stat, t_p_p = stats.ttest_rel(before, after)
print(f"Wilcoxon W = {w_stat:.4f}, p = {p_w:.4f}")
print(f"대응 t     : t = {t_p_stat:.4f}, p = {t_p_p:.4f}")

# === (3) 크루스칼-왈리스 vs ANOVA ===
print("\n" + "=" * 60)
print("(3) Kruskal-Wallis — 세 식단의 체중 감량")
print("=" * 60)
df_d = pd.read_excel(XLSX, sheet_name='식단감량')
groups = [df_d['식단A'].values, df_d['식단B'].values, df_d['식단C'].values]
for i, g in enumerate(groups):
    print(f"  식단 {chr(65+i)}: 중앙값={np.median(g):.3f}, 평균={g.mean():.3f}")
h_stat, p_h = stats.kruskal(*groups)
f_stat, p_f = stats.f_oneway(*groups)
print(f"\nKruskal-Wallis H = {h_stat:.4f}, p = {p_h:.4f}")
print(f"일원 ANOVA    F  = {f_stat:.4f}, p = {p_f:.4f}")
if p_h < 0.05:
    print("[해석] 적어도 한 식단의 분포가 다름. Dunn 검정으로 쌍별 비교 필요.")

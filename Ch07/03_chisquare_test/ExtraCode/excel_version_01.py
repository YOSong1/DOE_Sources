# -*- coding: utf-8 -*-
"""
페이지: 7.3 카이제곱 검정
Excel 활용 버전: sample_categorical.xlsx의 raw 데이터를 읽어
적합도 검정(주사위)과 독립성 검정(광고-구매)을 모두 수행.
기대빈도 < 5 셀 경고 처리도 포함.
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
XLSX = os.path.join(HERE, 'sample_categorical.xlsx')

# === (1) 적합도 검정 ===
print("=" * 60)
print("(1) 적합도 검정 — 주사위가 균등분포를 따르는가?")
print("=" * 60)
df_dice = pd.read_excel(XLSX, sheet_name='주사위')
observed = df_dice['결과'].value_counts().sort_index().values
expected = np.full(6, len(df_dice) / 6)
print(f"총 시행 횟수: {len(df_dice)}")
print(f"관측 빈도: {observed}")
print(f"기대 빈도: {expected}")

chi2_stat, p_val = stats.chisquare(observed, expected)
print(f"\nχ² = Σ(O-E)²/E = {chi2_stat:.4f}, df = 5, p = {p_val:.4f}")
# 수동 검산
manual = ((observed - expected)**2 / expected).sum()
print(f"수동 계산 χ² = {manual:.4f}")
print(f"결론: {'주사위가 공정하지 않음' if p_val<0.05 else '공정성 가정 유지'}")

# === (2) 독립성 검정 ===
print("\n" + "=" * 60)
print("(2) 독립성 검정 — 광고 유형과 구매 여부")
print("=" * 60)
df_ad = pd.read_excel(XLSX, sheet_name='광고구매')
ct = pd.crosstab(df_ad['광고유형'], df_ad['구매여부'])
print("교차표:")
print(ct)

chi2_s, p, dof, exp = stats.chi2_contingency(ct.values)
exp_df = pd.DataFrame(exp, index=ct.index, columns=ct.columns)
print(f"\nχ² = {chi2_s:.4f}, df = {dof}, p = {p:.4f}")
print("기대빈도:")
print(exp_df.round(2))

# 기대빈도 < 5 셀이 있는지 체크
low_cells = (exp < 5).sum()
if low_cells > 0:
    print(f"\n⚠️ 기대빈도 < 5인 셀 {low_cells}개 — 결과 신뢰성 주의")

# Cramer's V (효과 크기)
n_total = ct.values.sum()
phi2 = chi2_s / n_total
r, c = ct.shape
cramers_v = np.sqrt(phi2 / min(r-1, c-1))
print(f"\nCramer's V (효과 크기): {cramers_v:.4f}")
print("  (0.1=작음, 0.3=중간, 0.5=큼)")

if p < 0.05:
    print(f"\n[해석] 광고 유형과 구매 여부 간 연관 존재 (Cramer's V = {cramers_v:.3f})")
else:
    print("\n[해석] 광고 유형과 구매 여부 독립 가정 유지")

# -*- coding: utf-8 -*-
"""
페이지: 6.3 카이제곱 분포
Excel 활용 버전: sample_infection.xlsx의 raw 환자 데이터를 읽어
pandas.crosstab으로 교차표를 만들고, 카이제곱 통계량을 손계산으로도 확인한다.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, chi2

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_infection.xlsx'))
print(f"[Excel] 표본 크기 n = {len(df)}")
print(df.head(), '\n')

# 1) 교차표 (raw → contingency table)
ct = pd.crosstab(df['성별'], df['감염여부'])
print("교차표:")
print(ct)

# 2) chi2_contingency 적용
chi2_stat, p_val, dof, expected = chi2_contingency(ct.values)
exp_df = pd.DataFrame(expected, index=ct.index, columns=ct.columns)
print(f"\n카이제곱 통계량: {chi2_stat:.4f}")
print(f"p-value: {p_val:.4f}, 자유도: {dof}")
print("기대빈도표:")
print(exp_df.round(2))

# 3) 수식 직접 풀이: chi^2 = sum (O - E)^2 / E
print("\n--- 검정 통계량 수식 직접 검산 ---")
total_chi2 = 0
for i in ct.index:
    for j in ct.columns:
        O = ct.loc[i, j]
        E = exp_df.loc[i, j]
        contrib = (O - E) ** 2 / E
        total_chi2 += contrib
        print(f"  셀({i},{j}): O={O}, E={E:.2f}, (O-E)^2/E = {contrib:.4f}")
print(f"합계 = {total_chi2:.4f}  ← chi2_contingency 결과와 비교: {chi2_stat:.4f}")

# 4) 자유도와 임계값
crit = chi2.ppf(0.95, dof)
print(f"\n자유도 {dof}, α=0.05 임계값: {crit:.4f}")

# 5) 결과 해석
print("\n[해석]")
if p_val < 0.05:
    print("  p < 0.05 → 성별과 감염 여부는 통계적으로 독립이 아님 (연관 존재).")
else:
    print("  p >= 0.05 → 독립성 가정을 기각할 충분한 근거가 없음.")

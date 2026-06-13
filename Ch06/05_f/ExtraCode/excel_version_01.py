# -*- coding: utf-8 -*-
"""
페이지: 6.5 F 분포
Excel 활용 버전: sample_quality.xlsx의 두 생산라인 시트를 읽어
각 표본분산을 계산하고 양측 F검정의 p-value를 비대칭성에 주의해 계산한다.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import numpy as np
import pandas as pd
from scipy.stats import f

HERE = os.path.dirname(os.path.abspath(__file__))
xlsx = os.path.join(HERE, 'sample_quality.xlsx')
df_a = pd.read_excel(xlsx, sheet_name='Line_A')
df_b = pd.read_excel(xlsx, sheet_name='Line_B')
print(f"[Excel] Line A n={len(df_a)}, Line B n={len(df_b)}\n")

a = df_a['품질점수'].values
b = df_b['품질점수'].values

# 1) 표본분산 (자유도 보정 ddof=1)
var_a = np.var(a, ddof=1)
var_b = np.var(b, ddof=1)
print(f"Var(A) = {var_a:.4f},  Var(B) = {var_b:.4f}")

# 2) F 통계량 (관례상 큰 분산을 분자로)
if var_a >= var_b:
    F = var_a / var_b
    df1, df2 = len(a) - 1, len(b) - 1
else:
    F = var_b / var_a
    df1, df2 = len(b) - 1, len(a) - 1
print(f"F = {F:.4f}  (df1={df1}, df2={df2})")

# 3) 양측 p-value: F 분포가 비대칭이므로 min(CDF, 1-CDF) * 2
cdf = f.cdf(F, df1, df2)
p_two = 2 * min(cdf, 1 - cdf)
print(f"CDF(F) = {cdf:.4f}  →  p(양측) = 2·min(CDF, 1-CDF) = {p_two:.4f}")

# 4) 신뢰구간으로 σ_a²/σ_b² 추정
lower = (var_a / var_b) / f.ppf(0.975, len(a)-1, len(b)-1)
upper = (var_a / var_b) / f.ppf(0.025, len(a)-1, len(b)-1)
print(f"\n95% CI for Var(A)/Var(B) ≈ [{lower:.4f}, {upper:.4f}]")
if not (lower <= 1 <= upper):
    print("  → 신뢰구간이 1을 포함하지 않음 → 두 분산이 유의미하게 다름")
else:
    print("  → 신뢰구간이 1을 포함 → 등분산 가정 유지 가능")

# 5) 결과 해석
print("\n[해석]")
if p_two < 0.05:
    print("  두 생산 라인의 분산이 통계적으로 다릅니다 (품질 변동성 차이).")
else:
    print("  두 라인의 분산이 다르다는 충분한 근거가 없습니다.")

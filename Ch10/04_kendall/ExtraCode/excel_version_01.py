# -*- coding: utf-8 -*-
"""
페이지: 10.4 켄달의 타우
Excel 활용 버전: sample_movie_ranks.xlsx로 일치쌍/불일치쌍을 모두 enumerate하여
τ = (C - D)/(n(n-1)/2)을 손으로 계산하고 scipy 결과와 일치하는지 검증.
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
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_movie_ranks.xlsx'))
print(f"[Excel] n = {len(df)}\n", df, '\n')

A = df['평가자A_순위'].values
B = df['평가자B_순위'].values
n = len(A)

# 1) 모든 쌍을 enumerate해서 일치/불일치 판별
C = 0  # concordant
D = 0  # discordant
T = 0  # tied
for i, j in combinations(range(n), 2):
    da = A[j] - A[i]
    db = B[j] - B[i]
    if da * db > 0:
        C += 1
    elif da * db < 0:
        D += 1
    else:
        T += 1
total_pairs = n * (n - 1) // 2
print(f"총 쌍 수 = n(n-1)/2 = {total_pairs}")
print(f"일치쌍 C = {C}")
print(f"불일치쌍 D = {D}")
print(f"동점쌍 T = {T}")

# 2) Tau-a 직접 계산
tau_a = (C - D) / total_pairs
print(f"\nτ_a = (C - D) / 총쌍수 = ({C} - {D}) / {total_pairs} = {tau_a:.4f}")

# 3) scipy의 Tau-b (동점 보정 포함)
tau_b, p_val = stats.kendalltau(A, B)
print(f"scipy τ_b = {tau_b:.4f}, p = {p_val:.4f}")

# 4) 스피어만과 비교
rho, _ = stats.spearmanr(A, B)
print(f"\n참고: 스피어만 ρ = {rho:.4f}")
print("일반적으로 τ < ρ. 두 계수는 측정 척도가 달라 직접 비교 불가.")

# 5) 해석
print(f"\n[해석] 두 평가자의 순위 일치 비율 ≈ {(C/(C+D))*100:.1f}%")
if p_val < 0.05:
    print("       순위 간 관련성이 통계적으로 유의합니다.")
else:
    print("       유의한 관련성을 확인할 수 없습니다.")

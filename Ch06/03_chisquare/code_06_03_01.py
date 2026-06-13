# code_06_03_01.py
# -*- coding: utf-8 -*-
"""
페이지: 6.3 카이제곱 분포 — 성별 x 감염 여부 독립성 검정 예제.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, chi2
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# 1. 데이터 준비 (행: 성별, 열: 감염 여부)
data = np.array([[20, 30],   # 남성: 감염 20명, 비감염 30명
                 [15, 35]])  # 여성: 감염 15명, 비감염 35명

index = ['남성', '여성']
columns = ['감염', '비감염']
df_table = pd.DataFrame(data, index=index, columns=columns)
print("교차표:")
print(df_table)

# 2. 카이제곱 독립성 검정
chi2_stat, p_val, dof, expected = chi2_contingency(data)
print(f"\n카이제곱 통계량: {chi2_stat:.4f}")
print(f"p-value: {p_val:.4f}")
print(f"자유도: {dof}")
print("기대빈도표:")
print(pd.DataFrame(expected, index=index, columns=columns))

# 3. 결과 해석
alpha = 0.05
if p_val < alpha:
    print("\n결론: 귀무가설을 기각합니다 — 성별과 감염 여부는 독립적이지 않습니다.")
else:
    print("\n결론: 유의수준 0.05에서 귀무가설 기각 실패.")

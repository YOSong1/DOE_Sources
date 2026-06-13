# -*- coding: utf-8 -*-
"""
페이지: 9.4 MANOVA
Excel 활용 버전: sample_education_scores.xlsx의 데이터로 MANOVA를 수행하고
- 종속변수 간 상관관계 (MANOVA의 전제) 확인
- 4가지 다변량 통계량 출력
- 단변량 ANOVA 비교
- 산점도 + 평균 벡터 시각화
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.multivariate.manova import MANOVA
from statsmodels.formula.api import ols
import statsmodels.api as sm
import matplotlib
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_education_scores.xlsx'))
print(f"[Excel] n = {len(df)}, 집단: {df['education'].unique()}\n")
print(df.groupby('education').agg({'math':['mean','std'], 'reading':['mean','std']}))

# 1) 종속변수 간 상관 (MANOVA가 의미를 가지려면 상관 필요)
print(f"\n수학-읽기 상관계수: {df[['math','reading']].corr().iloc[0,1]:.4f}")

# 2) MANOVA
maov = MANOVA.from_formula('math + reading ~ education', data=df)
result = maov.mv_test()
print("\n=== MANOVA 결과 ===")
print(result)

# 3) 단변량 ANOVA로 어느 종속변수가 기여하는지 확인
print("\n=== 사후 단변량 ANOVA ===")
for dv in ['math', 'reading']:
    m = ols(f'{dv} ~ C(education)', data=df).fit()
    t = sm.stats.anova_lm(m, typ=2)
    print(f"\n--- {dv} ---")
    print(t)
    eta = t['sum_sq'].iloc[0] / t['sum_sq'].sum()
    print(f"  η² = {eta:.4f}")

# 4) 시각화: 산점도 + 집단 평균
colors = {'HS': '#4C72B0', 'BS': '#DD8452', 'MS': '#55A868'}
fig, ax = plt.subplots(figsize=(8, 6))
for edu, grp in df.groupby('education'):
    ax.scatter(grp['math'], grp['reading'],
               label=edu, color=colors.get(edu, 'gray'),
               alpha=0.6, s=80)
    ax.scatter(grp['math'].mean(), grp['reading'].mean(),
               color=colors.get(edu, 'gray'), marker='*',
               s=300, edgecolors='black', linewidth=1.5)
ax.set_xlabel('수학 점수')
ax.set_ylabel('읽기 점수')
ax.set_title('교육 수준별 수학·읽기 결합 분포 (★: 집단 평균 벡터)')
ax.legend(title='학력')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

print("\n[해석] MANOVA가 유의하면 두 종속변수의 결합 평균 벡터가 집단마다 다름.")
print("       단변량 ANOVA 결과를 함께 보고 어느 변수가 차이를 만드는지 파악.")

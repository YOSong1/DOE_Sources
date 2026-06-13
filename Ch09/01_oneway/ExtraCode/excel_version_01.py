# -*- coding: utf-8 -*-
"""
페이지: 9.1 일원배치 ANOVA
Excel 활용 버전: sample_teaching_methods.xlsx의 데이터로
- Levene 등분산 검정
- 일원 ANOVA (scipy + statsmodels ANOVA table)
- Tukey HSD 사후 검정
- 효과 크기 η² (eta-squared) 계산
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import numpy as np
import pandas as pd
from scipy.stats import f_oneway, levene
from statsmodels.formula.api import ols
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_teaching_methods.xlsx'))
print(f"[Excel] n = {len(df)}")
print(df.groupby('교수법')['시험점수'].agg(['count', 'mean', 'std']))

groups = [df[df['교수법'] == g]['시험점수'].values for g in df['교수법'].unique()]

# 1) 등분산성 검정
W, p_lev = levene(*groups)
print(f"\nLevene: W={W:.4f}, p={p_lev:.4f}")
print(f"  {'등분산 가정 위배' if p_lev<0.05 else '등분산 가정 유지'}")

# 2) ANOVA
F, p_F = f_oneway(*groups)
print(f"\nF통계량 = {F:.4f}, p = {p_F:.6f}")

# 3) ANOVA 표
model = ols('시험점수 ~ C(교수법)', data=df).fit()
table = sm.stats.anova_lm(model, typ=2)
print("\nANOVA 표 (Type II):")
print(table)

# 4) 효과 크기 η²
ss_between = table['sum_sq'].iloc[0]
ss_total = table['sum_sq'].sum()
eta_sq = ss_between / ss_total
print(f"\n효과 크기 η² = SS_between/SS_total = {eta_sq:.4f}")
print("  (0.01=작음, 0.06=중간, 0.14=큼)")

# 5) Tukey HSD
print("\nTukey HSD 사후검정:")
tukey = pairwise_tukeyhsd(df['시험점수'], df['교수법'], alpha=0.05)
print(tukey)

# 6) 시각화
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
df.boxplot(column='시험점수', by='교수법', ax=axes[0])
axes[0].set_title('교수법별 점수 분포')
axes[0].get_figure().suptitle('')

means = df.groupby('교수법')['시험점수'].mean()
sems = df.groupby('교수법')['시험점수'].sem()
axes[1].bar(means.index, means.values, yerr=sems.values, capsize=5)
axes[1].set_title(f'집단 평균 (F={F:.2f}, p={p_F:.4f})')
plt.tight_layout()
plt.show()

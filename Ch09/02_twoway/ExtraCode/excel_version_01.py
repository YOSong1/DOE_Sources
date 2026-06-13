# -*- coding: utf-8 -*-
"""
페이지: 9.2 이원배치 ANOVA
Excel 활용 버전: sample_fertilizer_watering.xlsx의 데이터를 읽어
- Type II ANOVA 표
- 상호작용 도표
- 주효과 + 상호작용 효과 크기(부분 η²) 계산
- 비료 × 관수 셀별 평균 표
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_fertilizer_watering.xlsx'))
print(f"[Excel] n = {len(df)}")
print("\n셀별 평균:")
cell_means = df.groupby(['fertilizer', 'watering'])['height'].agg(['mean', 'std', 'count'])
print(cell_means)

# 1) Type II ANOVA
model = ols('height ~ C(fertilizer) + C(watering) + C(fertilizer):C(watering)',
            data=df).fit()
table = sm.stats.anova_lm(model, typ=2)
print("\nANOVA 표:")
print(table)

# 2) 부분 η² (각 효과 / (해당 효과 + 잔차))
ss_res = table.loc['Residual', 'sum_sq']
print("\n부분 η² (Partial Eta-Squared):")
for name in ['C(fertilizer)', 'C(watering)', 'C(fertilizer):C(watering)']:
    ss = table.loc[name, 'sum_sq']
    p_eta = ss / (ss + ss_res)
    p = table.loc[name, 'PR(>F)']
    print(f"  {name}: η²_p = {p_eta:.4f}, p = {p:.4f}")

# 3) 상호작용 도표
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
cm = df.groupby(['fertilizer', 'watering'])['height'].mean().unstack()
cm.plot(marker='o', ax=axes[0])
axes[0].set_title('상호작용 도표')
axes[0].set_xlabel('비료 종류')
axes[0].set_ylabel('평균 높이')
axes[0].legend(title='관수')
axes[0].grid(alpha=0.3)

# 박스플롯
df.boxplot(column='height', by=['fertilizer', 'watering'], ax=axes[1])
axes[1].set_title('셀별 분포')
axes[1].get_figure().suptitle('')
plt.tight_layout()
plt.show()

# 4) 주효과 사후검정 (비료)
print("\nTukey HSD (비료):")
tukey_f = pairwise_tukeyhsd(df['height'], df['fertilizer'], alpha=0.05)
print(tukey_f)

# 5) 해석
inter_p = table.loc['C(fertilizer):C(watering)', 'PR(>F)']
if inter_p < 0.05:
    print("\n[해석] 상호작용이 유의 → 주효과 단독 해석 주의, 도표로 결합 효과 확인")
else:
    print("\n[해석] 상호작용 비유의 → 주효과 독립 해석 가능")

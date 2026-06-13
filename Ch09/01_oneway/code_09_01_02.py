# code_09_01_02.py
# -*- coding: utf-8 -*-
"""
페이지: 9.1 일원배치 ANOVA — 박스플롯 + 집단별 평균 막대 시각화.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

scores = {
    'group': ['A']*8 + ['B']*8 + ['C']*8,
    'score': [85, 88, 90, 86, 87, 89, 90, 91,
              78, 80, 79, 77, 82, 81, 80, 79,
              92, 93, 94, 91, 95, 92, 93, 94]
}
df = pd.DataFrame(scores)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

df.boxplot(column='score', by='group', ax=axes[0])
axes[0].set_title('교수법별 시험 점수 분포')
axes[0].set_xlabel('교수법')
axes[0].set_ylabel('점수')
axes[0].get_figure().suptitle('')

means = df.groupby('group')['score'].mean()
sems = df.groupby('group')['score'].sem()
axes[1].bar(means.index, means.values, yerr=sems.values,
            capsize=5, color=['#4C72B0', '#DD8452', '#55A868'])
axes[1].set_title('집단별 평균 (±SE)')
axes[1].set_xlabel('교수법')
axes[1].set_ylabel('평균 점수')

plt.tight_layout()
plt.show()

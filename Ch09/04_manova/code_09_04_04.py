# code_09_04_04.py
# -*- coding: utf-8 -*-
"""
페이지: 9.4 MANOVA — 두 종속변수 결합 공간의 집단별 산점도.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

np.random.seed(42)
data = {
    'education': ['HS'] * 15 + ['BS'] * 15 + ['MS'] * 15,
    'math':    list(np.random.normal(70, 5, 15)) +
               list(np.random.normal(78, 5, 15)) +
               list(np.random.normal(86, 5, 15)),
    'reading': list(np.random.normal(74, 4, 15)) +
               list(np.random.normal(82, 4, 15)) +
               list(np.random.normal(90, 4, 15))
}
df = pd.DataFrame(data)

colors = {'HS': '#4C72B0', 'BS': '#DD8452', 'MS': '#55A868'}
fig, ax = plt.subplots(figsize=(7, 5))

for edu, grp in df.groupby('education'):
    ax.scatter(grp['math'], grp['reading'],
               label=edu, color=colors[edu], alpha=0.7, s=60)
    ax.scatter(grp['math'].mean(), grp['reading'].mean(),
               color=colors[edu], marker='*', s=200, edgecolors='black')

ax.set_title('교육 수준별 수학·읽기 점수 분포\n(★: 집단 평균)')
ax.set_xlabel('수학 점수')
ax.set_ylabel('읽기 점수')
ax.legend(title='교육 수준')
plt.tight_layout()
plt.show()

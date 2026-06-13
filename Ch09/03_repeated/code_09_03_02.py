# code_09_03_02.py
# -*- coding: utf-8 -*-
"""
페이지: 9.3 반복 측정 ANOVA — 스파게티 플롯 + 박스플롯 시각화.
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

data = {
    'subject': [f'S{i+1}' for i in range(10) for _ in range(3)],
    'time':    ['t1', 't2', 't3'] * 10,
    'score':   [55, 60, 63, 50, 52, 55, 65, 66, 70, 58, 60, 64,
                62, 65, 67, 59, 61, 60, 70, 72, 75, 68, 70, 71,
                57, 59, 60, 52, 55, 58]
}
df = pd.DataFrame(data)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for subj in df['subject'].unique():
    subj_data = df[df['subject'] == subj]
    axes[0].plot(subj_data['time'], subj_data['score'],
                 marker='o', alpha=0.4, color='steelblue')

means = df.groupby('time')['score'].mean()
axes[0].plot(means.index, means.values, marker='o',
             linewidth=3, color='red', label='평균')
axes[0].set_title('시점별 기억력 점수 변화 (개인 + 평균)')
axes[0].set_xlabel('측정 시점')
axes[0].set_ylabel('점수')
axes[0].legend()

df.boxplot(column='score', by='time', ax=axes[1])
axes[1].set_title('시점별 점수 분포')
axes[1].set_xlabel('측정 시점')
axes[1].set_ylabel('점수')
axes[1].get_figure().suptitle('')

plt.tight_layout()
plt.show()

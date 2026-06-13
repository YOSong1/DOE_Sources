# code_10_05_02.py
# -*- coding: utf-8 -*-
"""
페이지: 10.5 점-이계열 상관계수 — 합격 여부에 따른 시험 점수 박스플롯.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

data_exam = {
    'student_id': range(1, 21),
    'test_score': [56, 75, 45, 71, 62, 50, 49, 90, 65, 85,
                   55, 78, 40, 68, 72, 51, 60, 80, 47, 92],
    'pass_fail':  [0, 1, 0, 1, 1, 0, 0, 1, 1, 1,
                   0, 1, 0, 1, 1, 0, 1, 1, 0, 1]
}
df_exam = pd.DataFrame(data_exam)
r_pb, p_value = stats.pointbiserialr(df_exam['pass_fail'], df_exam['test_score'])

plt.figure(figsize=(8, 5))
sns.boxplot(data=df_exam, x='pass_fail', y='test_score',
            hue='pass_fail', palette={0: '#e74c3c', 1: '#2ecc71'},
            legend=False)

plt.title(f'합격 여부에 따른 시험 점수 분포\n(r_pb = {r_pb:.3f}, p = {p_value:.4f})',
          fontsize=13)
plt.xlabel('합격 여부 (0=불합격, 1=합격)')
plt.ylabel('시험 점수')
plt.xticks([0, 1], ['불합격 (0)', '합격 (1)'])
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

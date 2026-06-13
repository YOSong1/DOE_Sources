# code_15_03_01.py
# -*- coding: utf-8 -*-
"""
페이지: 15.3 예제로 이해: 조미료 선호도의 난괴법 분석
설명: 4 블록 × 3 처리 (조미료 A/B/C) RCBD 데이터 구성 및 ANOVA.
"""

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt

# 예시 데이터프레임 구성
data = {
    'Block': ['Block1', 'Block1', 'Block1',
              'Block2', 'Block2', 'Block2',
              'Block3', 'Block3', 'Block3',
              'Block4', 'Block4', 'Block4'],
    'Treatment': ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'],
    'Score': [7.2, 6.5, 7.8,
              6.8, 6.3, 7.2,
              7.5, 7.0, 7.9,
              8.0, 7.4, 8.3]
}
df = pd.DataFrame(data)
print("실험 데이터:")
print(df)

# ANOVA를 위한 모형 정의
# 반응변수: Score
# 모형: Score ~ C(Treatment) + C(Block)
model = ols('Score ~ C(Treatment) + C(Block)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print("ANOVA Table:")
print(anova_table)

# 평균값 시각화 (처리별 평균)
treatment_means = df.groupby('Treatment')['Score'].mean()
plt.figure()
treatment_means.plot(kind='bar')
plt.title("Average Score by Treatment")
plt.xlabel("Treatment")
plt.ylabel("Mean Score")
plt.show()

# 블록별 평균 시각화
block_means = df.groupby('Block')['Score'].mean()
plt.figure()
block_means.plot(kind='bar')
plt.title("Average Score by Block")
plt.xlabel("Block")
plt.ylabel("Mean Score")
plt.show()

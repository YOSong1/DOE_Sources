# code_18_03_03.py
# Chapter 18.3 원본 코드 3: 일원 ANOVA

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

np.random.seed(42)
levels = ['A', 'B', 'C']
n_rep = 5
true_means = {'A': 50, 'B': 55, 'C': 60}
std_dev = 3
data = []
for level in levels:
    for _ in range(n_rep):
        data.append([level, np.random.normal(true_means[level], std_dev)])
df = pd.DataFrame(data, columns=['ProcessTimeLevel', 'Measurement'])

model = ols('Measurement ~ C(ProcessTimeLevel)', data=df).fit()
anova_result = sm.stats.anova_lm(model, typ=2)

print("===== ANOVA 결과 =====")
print(anova_result)

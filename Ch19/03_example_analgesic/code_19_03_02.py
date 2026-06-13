# code_19_03_02.py
# Chapter 19.3 원본 코드 2: 혼합 효과 모형 (mixedlm) 분석

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

np.random.seed(42)
subjects = np.repeat(np.arange(1, 11), 2)
periods = np.tile([1, 2], 10)
treatments = []
sequences = []
for _ in range(5):
    treatments.extend(['A', 'B']); sequences.extend(['A->B', 'A->B'])
for _ in range(5):
    treatments.extend(['B', 'A']); sequences.extend(['B->A', 'B->A'])

df = pd.DataFrame({'Subject': subjects, 'Period': periods,
                   'Sequence': sequences, 'Treatment': treatments})
df['Score'] = (df['Treatment'].map({'A': 10, 'B': 12})
               + df['Period'].map({1: 0, 2: -1})
               + np.repeat(np.random.normal(0, 1.5, 10), 2)
               + np.random.normal(0, 1, 20)).round(2)

# Score ~ Treatment + Period (고정), groups=Subject (랜덤)
model = smf.mixedlm("Score ~ Treatment + Period",
                    data=df, groups=df["Subject"])
result = model.fit()

print("\n--- 혼합 효과 모형 분석 결과 ---")
print(result.summary())

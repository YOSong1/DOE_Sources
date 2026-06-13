# code_19_03_01.py
# Chapter 19.3 원본 코드 1: 2x2 교차 설계 가상 데이터 생성 (page 324314)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

np.random.seed(42)

subjects = np.repeat(np.arange(1, 11), 2)
periods = np.tile([1, 2], 10)

treatments = []
sequences = []

# 그룹 1 (A -> B), 피험자 1~5
for _ in range(5):
    treatments.extend(['A', 'B'])
    sequences.extend(['A->B', 'A->B'])

# 그룹 2 (B -> A), 피험자 6~10
for _ in range(5):
    treatments.extend(['B', 'A'])
    sequences.extend(['B->A', 'B->A'])

df = pd.DataFrame({
    'Subject': subjects,
    'Period': periods,
    'Sequence': sequences,
    'Treatment': treatments
})

treatment_effect = df['Treatment'].map({'A': 10, 'B': 12})
period_effect = df['Period'].map({1: 0, 2: -1})
subject_random_effect = np.repeat(np.random.normal(0, 1.5, 10), 2)
noise = np.random.normal(0, 1, 20)

df['Score'] = treatment_effect + period_effect + subject_random_effect + noise
df['Score'] = df['Score'].round(2)

print("=== 교차 설계 실험 데이터 (일부) ===")
print(df.head(6))

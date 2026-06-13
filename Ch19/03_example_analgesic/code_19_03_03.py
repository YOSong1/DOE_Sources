# code_19_03_03.py
# Chapter 19.3 원본 코드 3: 박스플롯 시각화

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
subjects = np.repeat(np.arange(1, 11), 2)
periods = np.tile([1, 2], 10)
treatments, sequences = [], []
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

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

plt.figure()
df.boxplot(column='Score', by='Treatment')
plt.title('처리(진통제)별 통증 완화 점수')
plt.suptitle('')
plt.xlabel('진통제 종류')
plt.ylabel('점수 (Score)')
plt.show()

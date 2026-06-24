# code_19_05_01.py
# Chapter 19.5 연습 문제 원본 코드: 2x2 UI 교차 설계 가상 데이터 (page 324410)

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

np.random.seed(101)
n_subjects = 12
subjects_ui = np.repeat(np.arange(1, n_subjects + 1), 2)
periods_ui = np.tile([1, 2], n_subjects)

treatments_ui = []
sequences_ui = []
for _ in range(n_subjects // 2):
    treatments_ui.extend(['A', 'B']); sequences_ui.extend(['A->B', 'A->B'])
for _ in range(n_subjects // 2):
    treatments_ui.extend(['B', 'A']); sequences_ui.extend(['B->A', 'B->A'])

df_ui = pd.DataFrame({
    'Subject': subjects_ui,
    'Period': periods_ui,
    'Sequence': sequences_ui,
    'Treatment': treatments_ui
})

base_time = 120
treatment_effects_ui = {'A': 0, 'B': -15}
period_effects_ui = {1: 0, 2: -10}
subject_random_effects_ui = np.repeat(np.random.normal(0, 10, n_subjects), 2)
noise_ui = np.random.normal(0, 5, n_subjects * 2)

df_ui['Time'] = (base_time
                 + df_ui['Treatment'].map(treatment_effects_ui)
                 + df_ui['Period'].map(period_effects_ui)
                 + subject_random_effects_ui + noise_ui)
df_ui['Time'] = df_ui['Time'].round(1)

print(df_ui.head())

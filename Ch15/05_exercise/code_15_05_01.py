# code_15_05_01.py
# -*- coding: utf-8 -*-
"""
페이지: 15.5 연습 문제 — 서로 다른 학습 방법의 효과 비교 (RCBD)
설명: 3블록(성취 수준) × 3처리(학습 방법) × 반복 2회 = 18개 데이터 생성.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns  # 시각화를 위해 추가

# --- 1. 실험 조건 정의 ---
treatments = ['A', 'B', 'C']  # 학습 방법
blocks = ['Block1_High',
          'Block2_Mid',
          'Block3_Low']  # 성취 수준 그룹 (블록)
replicates_per_cell = 2  # 각 블록-처리 조합당 반복 수

# --- 2. 가상의 반응 변수(점수) 데이터 생성 ---
np.random.seed(555)
simulated_data_education = []

# 블록 효과 및 처리 효과 (임의 설정)
block_effects = {'Block1_High': 15,
                 'Block2_Mid': 5,
                 'Block3_Low': -5}
treatment_effects = {'A': 5,
                     'B': -2,
                     'C': 8}
base_score = 60

for block in blocks:
    for treatment in treatments:
        for _ in range(replicates_per_cell):
            score = base_score + block_effects[block] + treatment_effects[treatment] \
                    + np.random.normal(0, 3)
            score = round(np.clip(score, 0, 100), 1)

            simulated_data_education.append({'Block': block,
                                             'Treatment': treatment,
                                             'Score': score})

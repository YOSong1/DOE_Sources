# code_14_05_01.py
# -*- coding: utf-8 -*-
"""
페이지: 14.5 연습 문제 — 자동차 연비 개선을 위한 엔진 파라미터 최적화
설명: 3개 3수준 인자(점화 시점, 연료 분사압, 공기흡입량)에 L9 직교배열을
      적용한 가상의 연비(km/L) 데이터 생성.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. L9 직교배열 및 요인 수준 정의 ---
levels_A_engine = [10, 12, 14]
levels_B_engine = [100, 120, 140]
levels_C_engine = [300, 350, 400]

# L9 직교배열 인덱스 (0, 1, 2는 각 levels 리스트의 인덱스)
l9_design_indices_engine = [
    (0, 0, 0), (0, 1, 1), (0, 2, 2),
    (1, 0, 1), (1, 1, 2), (1, 2, 0),
    (2, 0, 2), (2, 1, 0), (2, 2, 1)
]

# --- 2. 가상의 연비(반응값) 데이터 생성 ---
np.random.seed(123)
base_efficiency = 10.0

# 각 요인 수준에 따른 효과 (임의로 설정, 학생들이 찾아야 할 숨겨진 효과)
effect_A = {10: 0.5, 12: 1.0, 14: 0.2}
effect_B = {100: 0.8, 120: 0.5, 140: -0.2}
effect_C = {300: -0.3, 350: 0.6, 400: 1.2}

simulated_responses_engine = []
for a_idx, b_idx, c_idx in l9_design_indices_engine:
    val_A = levels_A_engine[a_idx]
    val_B = levels_B_engine[b_idx]
    val_C = levels_C_engine[c_idx]

    current_efficiency = base_efficiency + effect_A[val_A] + effect_B[val_B] + \
        effect_C[val_C] + np.random.normal(0, 0.3)
    simulated_responses_engine.append(round(current_efficiency, 2))

print(simulated_responses_engine)

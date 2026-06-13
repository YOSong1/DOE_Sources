# code_11_03_01.py
# -*- coding: utf-8 -*-
"""
페이지: 11.3 예제로 이해: 초콜릿 코팅 품질의 완전 요인 실험
설명: 3요인 2수준 (코팅 온도, 혼합 속도, 냉각 시간) x 반복 3회의
      가상 실험 데이터를 생성한다.
"""

import pandas as pd
import itertools
import numpy as np
import statsmodels.formula.api as smf
from scipy import stats

# 요인 정의
factors = {
    "Coating_Temperature": [30, 35],
    "Mixing_Speed": [50, 100],
    "Cooling_Time": [5, 10]
}

# 반복 실험 포함 데이터 생성
np.random.seed(42)
experiment_data = []
for temp, speed, time in itertools.product(
    factors["Coating_Temperature"],
    factors["Mixing_Speed"],
    factors["Cooling_Time"]
):
    for rep in range(3):
        # 요인 수준을 -1/+1로 정규화하고 임의의 주효과 및 상호작용 부여
        temp_norm = (temp - 32.5)/2.5
        speed_norm = (speed - 75)/25
        time_norm = (time - 7.5)/2.5
        quality = 85 + 5*temp_norm + 2*speed_norm + 3*time_norm \
            + 1.5*temp_norm*time_norm + np.random.normal(0, 1.5)
        experiment_data.append({
            "Coating_Temperature": temp,
            "Mixing_Speed": speed,
            "Cooling_Time": time,
            "Replicate": rep + 1,
            "Coating_Quality": quality
        })

df_experiment = pd.DataFrame(experiment_data)
print(df_experiment.head())

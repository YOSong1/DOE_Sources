# code_11_05_01.py
# -*- coding: utf-8 -*-
"""
페이지: 11.5 연습 문제 — 반도체 웨이퍼 공정 최적화
설명: 식각 시간, 플라즈마 강도, 가스 혼합 비율의 3요인 2수준 x 반복 3회
      가상 표면 거칠기 데이터를 생성한다.
"""

import pandas as pd
import itertools
import numpy as np
import statsmodels.formula.api as smf
from scipy import stats

factors_etching = {
    "Etching_Time": [15, 30],
    "Plasma_Intensity": [200, 300],
    "Gas_Mixture_Ratio": [50, 70]
}

np.random.seed(42)
etching_experiment_data = []
for time, intensity, ratio in itertools.product(
    factors_etching["Etching_Time"],
    factors_etching["Plasma_Intensity"],
    factors_etching["Gas_Mixture_Ratio"]
):
    for rep in range(3):
        # -1/+1 코딩
        time_norm = (time - 22.5)/7.5
        intensity_norm = (intensity - 250)/50
        ratio_norm = (ratio - 60)/10
        # 주효과 및 상호작용 가정
        surface_roughness = 10 + 1.5*time_norm - 2.5*intensity_norm + 0.5*ratio_norm \
            - 1.0*time_norm*intensity_norm + np.random.normal(0, 0.5)
        etching_experiment_data.append({
            "Etching_Time": time,
            "Plasma_Intensity": intensity,
            "Gas_Mixture_Ratio": ratio,
            "Replicate": rep + 1,
            "Surface_Roughness": surface_roughness
        })
df_etching = pd.DataFrame(etching_experiment_data)
print(df_etching.head())

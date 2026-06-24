# code_13_05_01.py
# -*- coding: utf-8 -*-
"""
페이지: 13.5 연습 문제 — 제빵 공정 최적화 (응답 표면 분석)
설명: 발효 시간과 굽는 온도 두 요인에 대한 가상 부드러움 점수 데이터 생성.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 한글 폰트 설정 (환경에 맞게 주석 해제 또는 변경)
# plt.rc('font', family='Malgun Gothic')  # Windows 예시
# plt.rc('font', family='AppleGothic')    # macOS 예시
plt.rc('axes', unicode_minus=False)  # 마이너스 부호 깨짐 방지

np.random.seed(420)  # 결과 재현성을 위한 시드
n_samples = 30       # 총 실험 횟수 (가상)

# 요인 수준 범위 내에서 임의의 값 생성 또는 체계적 설계 값 사용
# 예시: 발효 시간 (60 ~ 120분), 굽는 온도 (180 ~ 220°C)
fermentation_time = np.random.uniform(60, 120, n_samples)
baking_temperature = np.random.uniform(180, 220, n_samples)

true_softness_effect = (
    50
    + 0.3 * (fermentation_time - 90)
    - 0.2 * (baking_temperature - 200)
    - 0.005 * ((fermentation_time - 90) ** 2)
    - 0.008 * ((baking_temperature - 200) ** 2)
    + 0.001 * (fermentation_time - 90) * (baking_temperature - 200)
)

noise = np.random.normal(0, 3, n_samples)  # 평균 0, 표준편차 3의 오차
softness_score = true_softness_effect + noise

# 반응값이 0~100 범위를 벗어나지 않도록 조정 (실제 데이터에서는 발생 가능)
softness_score = np.clip(softness_score, 0, 100)

# 데이터프레임 생성
df_baking = pd.DataFrame({
    'Fermentation_Time': fermentation_time,
    'Baking_Temperature': baking_temperature,
    'Softness_Score': softness_score
})

print("=== 제빵 공정 실험 데이터 (일부) ===")
print(df_baking.head())
print(f"\n총 생성된 데이터 포인트 수: {len(df_baking)}")

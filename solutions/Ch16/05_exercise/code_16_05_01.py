# code_16_05_01.py
# Chapter 16.5 연습 문제: 신소재 인장 강도 BBD 분석
# 원본 코드: 책 본문(page 324336)에 게재된 데이터 생성 코드 그대로
#
# 3요인(열처리 온도, 합금 A 첨가량, 압연 속도)의 3-level BBD 15회 실험을
# np.random.seed(888) 시드로 가상 생성합니다.

import numpy as np
import pandas as pd

# --- 1. Box-Behnken 설계점 (3요인, 15점 - 코드화된 값) ---
design_points_coded = [
    [-1, -1,  0], [ 1, -1,  0], [-1,  1,  0], [ 1,  1,  0],
    [-1,  0, -1], [ 1,  0, -1], [-1,  0,  1], [ 1,  0,  1],
    [ 0, -1, -1], [ 0,  1, -1], [ 0, -1,  1], [ 0,  1,  1],
    [ 0,  0,  0], [ 0,  0,  0], [ 0,  0,  0]
]
df_design_coded = pd.DataFrame(design_points_coded, columns=['X1', 'X2', 'X3'])

# --- 2. 실제 요인 수준으로 변환 ---
df_design_coded['Heat_Treatment_Temp'] = df_design_coded['X1'].apply(
    lambda x: 500 + x * 50)
df_design_coded['Alloy_A_Percentage'] = df_design_coded['X2'].apply(
    lambda x: 1.5 + x * 0.5)
df_design_coded['Rolling_Speed'] = df_design_coded['X3'].apply(
    lambda x: 10 + x * 5)

# --- 3. 가상의 인장 강도(반응값) 데이터 생성 ---
np.random.seed(888)
base_strength = 650

X1_coded = df_design_coded['X1']
X2_coded = df_design_coded['X2']
X3_coded = df_design_coded['X3']

tensile_strength_values = (
    base_strength
    + 20 * X1_coded
    + 15 * X2_coded
    + 5 * X3_coded
    - 8 * X1_coded**2
    - 6 * X2_coded**2
    + 4 * X1_coded * X2_coded
    + np.random.normal(0, 5, len(df_design_coded))
)

df_design_coded['Tensile_Strength'] = np.round(tensile_strength_values, 1)

df_strength_experiment = df_design_coded[['Heat_Treatment_Temp',
                                          'Alloy_A_Percentage',
                                          'Rolling_Speed',
                                          'Tensile_Strength']].copy()

print("=== 신소재 인장 강도 최적화 실험 데이터 (일부) ===")
print(df_strength_experiment.head())
print(f"\n총 생성된 데이터 포인트 수: {len(df_strength_experiment)}")

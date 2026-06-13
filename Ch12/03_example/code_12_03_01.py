# code_12_03_01.py
# -*- coding: utf-8 -*-
"""
페이지: 12.3 예제로 이해: 반도체 식각 공정의 부분 요인 실험
설명: pyDOE3 의 fracfact 로 2^(5-2) (8 runs, Resolution III) 설계 행렬을 생성하고
      실제 실험 조건으로 변환한다. (12.3.2 ~ 12.3.3 코드)
"""

# 라이브러리 설치 (필요 시)
# pip install pyDOE3 statsmodels pandas numpy matplotlib

import numpy as np
import pandas as pd
from pyDOE3 import fracfact
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 2^(5-2) 부분 요인 설계 행렬 생성
# a, b, c: 독립 요인 (기본 요인)
# ab: D = A*B (생성 함수 1)
# ac: E = A*C (생성 함수 2)
design_matrix = fracfact('a b c ab ac')

factors = ['A', 'B', 'C', 'D', 'E']
df_design = pd.DataFrame(design_matrix, columns=factors)

print("=" * 50)
print("2^(5-2) 부분 요인 설계 행렬")
print("=" * 50)
print(f"실험 횟수: {len(df_design)}회 (전체 요인 실험 대비 1/4)")
print()
print(df_design.to_string(index=True))

# 실제 실험 조건으로 변환
actual_conditions = pd.DataFrame()
actual_conditions['RF 전력 (W)'] = df_design['A'].map({-1.0: 200, 1.0: 400})
actual_conditions['가스 압력 (mTorr)'] = df_design['B'].map({-1.0: 100, 1.0: 300})
actual_conditions['가스 유량 (sccm)'] = df_design['C'].map({-1.0: 50, 1.0: 100})
actual_conditions['웨이퍼 온도 (°C)'] = df_design['D'].map({-1.0: 200, 1.0: 350})
actual_conditions['식각 시간 (min)'] = df_design['E'].map({-1.0: 5, 1.0: 15})

print("\n실제 실험 조건:")
print(actual_conditions.to_string(index=True))

# 실험 결과 데이터 (식각률, nm/min)
etch_rate = [155, 320, 190, 365, 175, 340, 205, 410]
df_design['Y'] = etch_rate

print("\n실험 설계 및 결과:")
print(df_design.to_string(index=True))

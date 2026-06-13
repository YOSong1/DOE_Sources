# code_17_03_02.py
# Chapter 17.3 원본 코드 2: 일원분산분석 수행 및 결과 해석

import numpy as np
from scipy.stats import f_oneway

np.random.seed(42)
fertilizer_A = np.random.normal(loc=10, scale=2, size=10)
fertilizer_B = np.random.normal(loc=12, scale=2, size=10)
fertilizer_C = np.random.normal(loc=14, scale=2, size=10)

f_stat, p_value = f_oneway(fertilizer_A, fertilizer_B, fertilizer_C)
print("일원분산분석 결과")
print(f"F-statistic: {f_stat:.4f}")
print(f"p-value     : {p_value:.4f}")

if p_value < 0.05:
    print("=> 유의수준 5%에서 처리(비료 종류) 간 평균의 차이가 통계적으로 유의합니다.")
else:
    print("=> 유의수준 5%에서 처리(비료 종류) 간 평균의 차이가 통계적으로 유의하지 않습니다.")

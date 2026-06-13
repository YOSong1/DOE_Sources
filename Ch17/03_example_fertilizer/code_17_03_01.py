# code_17_03_01.py
# Chapter 17.3 예제로 이해: 비료 종류에 따른 식물 성장률 비교
# 원본 코드 1: 라이브러리 임포트 및 가상 데이터 생성 (page 324553)

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f_oneway

# 비료 A, B, C 각각 10개씩 (가상적으로 정규분포를 따르는 무작위 데이터)
np.random.seed(42)
fertilizer_A = np.random.normal(loc=10, scale=2, size=10)
fertilizer_B = np.random.normal(loc=12, scale=2, size=10)
fertilizer_C = np.random.normal(loc=14, scale=2, size=10)

print("A:", fertilizer_A)
print("B:", fertilizer_B)
print("C:", fertilizer_C)

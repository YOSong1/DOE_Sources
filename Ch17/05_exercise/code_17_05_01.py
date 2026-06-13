# code_17_05_01.py
# Chapter 17.5 연습 문제: 새로운 교육용 SW의 효과 비교 (CRD)
# 원본 코드: 책 본문(page 324313) 데이터 생성 부분

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
import pandas as pd

np.random.seed(999)

# Version A 그룹: 평균 75점, 표준편차 8
score_A = np.random.normal(loc=75, scale=8, size=10)
# Version B 그룹: 평균 82점, 표준편차 8
score_B = np.random.normal(loc=82, scale=8, size=10)
# Version C 그룹: 평균 77점, 표준편차 8
score_C = np.random.normal(loc=77, scale=8, size=10)

df_scores = pd.DataFrame({
    'Version A': score_A,
    'Version B': score_B,
    'Version C': score_C
})
print("=== 생성된 그룹별 시험 점수 데이터 ===")
print(df_scores.head())

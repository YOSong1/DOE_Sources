# code_14_03_01.py
# -*- coding: utf-8 -*-
"""
페이지: 14.3 예제로 이해: 온도·압력·시간의 L9 직교배열 최적화
설명: L9 직교배열을 구성하고, 가상의 출력값에 대해
      \"더 클수록 좋은\" S/N비를 계산한 뒤 인자별 주효과를 분석한다.
"""

import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt

# --------------------
# 1. L9 직교배열 구성
# --------------------
levels_A = [180, 200, 220]  # 인자 A 수준
levels_B = [1, 2, 3]        # 인자 B 수준
levels_C = [10, 15, 20]     # 인자 C 수준

# L9 배열 (인덱스로 수준을 나타내기 위해 0,1,2로)
l9_design = [
    (0, 0, 0),
    (0, 1, 1),
    (0, 2, 2),
    (1, 0, 1),
    (1, 1, 2),
    (1, 2, 0),
    (2, 0, 2),
    (2, 1, 0),
    (2, 2, 1)
]

# --------------------
# 2. 가상의 출력값 생성
# --------------------
np.random.seed(42)
responses = np.random.normal(loc=50, scale=5, size=9)  # 평균 50, 표준편차 5

# --------------------
# 3. DataFrame으로 정리
# --------------------
data = []
for i, (a_idx, b_idx, c_idx) in enumerate(l9_design):
    A_val = levels_A[a_idx]
    B_val = levels_B[b_idx]
    C_val = levels_C[c_idx]
    y = responses[i]
    data.append([i+1, A_val, B_val, C_val, y])

df = pd.DataFrame(data, columns=["Run", "A", "B", "C", "Response"])
print("=== 실험 데이터 ===")
print(df)

# --------------------
# 4. S/N 비 계산 ("더 클수록 좋은" 공식)
# --------------------
def sn_ratio_larger_better(y):
    return -10 * np.log10(np.mean(1 / (y**2)))

df['SN'] = df['Response'].apply(lambda x: sn_ratio_larger_better(np.array([x])))
print("\n=== S/N 비 계산 결과 ===")
print(df)

# --------------------
# 5. 인자별 주효과 계산
# --------------------
sn_means = df.groupby('A')['SN'].mean().reset_index(name='SN_mean_A')
sn_means_B = df.groupby('B')['SN'].mean().reset_index(name='SN_mean_B')
sn_means_C = df.groupby('C')['SN'].mean().reset_index(name='SN_mean_C')

print("\n=== 인자 A 수준별 평균 S/N ===")
print(sn_means)
print("\n=== 인자 B 수준별 평균 S/N ===")
print(sn_means_B)
print("\n=== 인자 C 수준별 평균 S/N ===")
print(sn_means_C)

# --------------------
# 6. 시각화(주효과도)
# --------------------
plt.figure()
plt.plot([180, 200, 220], sn_means['SN_mean_A'], marker='o')
plt.title('Factor A (Temperature) vs Mean S/N')
plt.xlabel('Temperature (°C)')
plt.ylabel('Mean S/N')
plt.show()

plt.figure()
plt.plot([1, 2, 3], sn_means_B['SN_mean_B'], marker='o')
plt.title('Factor B (Pressure) vs Mean S/N')
plt.xlabel('Pressure (bar)')
plt.ylabel('Mean S/N')
plt.show()

plt.figure()
plt.plot([10, 15, 20], sn_means_C['SN_mean_C'], marker='o')
plt.title('Factor C (Time) vs Mean S/N')
plt.xlabel('Time (min)')
plt.ylabel('Mean S/N')
plt.show()

# code_18_05_01.py
# Chapter 18.5 연습 문제 원본 코드: 세정제 3종 6반복 데이터 생성 (page 324557)

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
import pandas as pd

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

np.random.seed(101)

contaminant_A = np.random.normal(loc=15, scale=2.5, size=6)
contaminant_B = np.random.normal(loc=10, scale=2.5, size=6)
contaminant_C = np.random.normal(loc=12, scale=2.5, size=6)

print("A:", contaminant_A)
print("B:", contaminant_B)
print("C:", contaminant_C)

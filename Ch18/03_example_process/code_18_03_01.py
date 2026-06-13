# code_18_03_01.py
# Chapter 18.3 원본 코드 1: 공정 처리 시간 3수준 5반복 데이터 생성 (page 324299)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

np.random.seed(42)

levels = ['A', 'B', 'C']
n_rep = 5
true_means = {'A': 50, 'B': 55, 'C': 60}
std_dev = 3

data = []
for level in levels:
    for _ in range(n_rep):
        value = np.random.normal(loc=true_means[level], scale=std_dev)
        data.append([level, value])

df = pd.DataFrame(data, columns=['ProcessTimeLevel', 'Measurement'])
print(df)

# code_17_03_03.py
# Chapter 17.3 원본 코드 3: 박스플롯 시각화

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
fertilizer_A = np.random.normal(loc=10, scale=2, size=10)
fertilizer_B = np.random.normal(loc=12, scale=2, size=10)
fertilizer_C = np.random.normal(loc=14, scale=2, size=10)

data = [fertilizer_A, fertilizer_B, fertilizer_C]
labels = ["Fertilizer A", "Fertilizer B", "Fertilizer C"]
plt.boxplot(data, tick_labels=labels)
plt.title("Completely Randomized Design Example")
plt.xlabel("Fertilizer Type")
plt.ylabel("Plant Growth (cm)")
plt.show()

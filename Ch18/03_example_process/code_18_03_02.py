# code_18_03_02.py
# Chapter 18.3 원본 코드 2: 기술 통계와 박스플롯

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
levels = ['A', 'B', 'C']
n_rep = 5
true_means = {'A': 50, 'B': 55, 'C': 60}
std_dev = 3
data = []
for level in levels:
    for _ in range(n_rep):
        data.append([level, np.random.normal(true_means[level], std_dev)])
df = pd.DataFrame(data, columns=['ProcessTimeLevel', 'Measurement'])

desc_stats = df.groupby('ProcessTimeLevel')['Measurement'].describe()
print("===== 기술 통계 =====")
print(desc_stats, "\n")

plt.figure()
df.boxplot(by='ProcessTimeLevel', column='Measurement', grid=False)
plt.title('Boxplot of Measurements by ProcessTimeLevel')
plt.suptitle('')
plt.xlabel('Process Time Level')
plt.ylabel('Measurement')
plt.show()

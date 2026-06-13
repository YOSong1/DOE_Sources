# code_05_02_02.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.2 베르누이 분포 - PMF 시각화
# 출처: WikiDocs book 1914, page 324470
# p=0.3, 0.5, 0.7 세 경우의 PMF를 막대그래프로 비교

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bernoulli

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

p_values = [0.3, 0.5, 0.7]
k = [0, 1]
colors = ['steelblue', 'darkorange', 'seagreen']

fig, axes = plt.subplots(1, 3, figsize=(12, 4))
fig.suptitle('베르누이 분포 PMF 비교', fontsize=14, fontweight='bold')

for ax, p, color in zip(axes, p_values, colors):
    pmf = [bernoulli.pmf(ki, p) for ki in k]
    ax.bar(['실패 (0)', '성공 (1)'], pmf, color=color, alpha=0.8, edgecolor='black')
    ax.set_title(f'p = {p}')
    ax.set_xlabel('결과')
    ax.set_ylabel('확률')
    ax.set_ylim(0, 1.0)
    for i, v in enumerate(pmf):
        ax.text(i, v + 0.02, f'{v:.2f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('bernoulli_pmf.png', dpi=120)
print("saved bernoulli_pmf.png")

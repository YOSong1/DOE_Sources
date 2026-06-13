# code_05_03_02.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.3 이항 분포 - PMF 비교 시각화
# 출처: WikiDocs book 1914, page 324375
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

n = 20
p_values = [0.1, 0.3, 0.5]
colors = ['steelblue', 'darkorange', 'green']

k = np.arange(0, n + 1)

fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)

for ax, p_val, color in zip(axes, p_values, colors):
    probs = binom.pmf(k, n, p_val)
    ax.bar(k, probs, color=color, alpha=0.8, edgecolor='black')
    ax.set_title(f'B(n=20, p={p_val})', fontsize=13)
    ax.set_xlabel('성공 횟수 k')
    ax.set_ylabel('확률 P(X=k)')
    ax.axvline(n * p_val, color='red', linestyle='--', label=f'평균={n*p_val:.1f}')
    ax.legend()

plt.suptitle('이항 분포 PMF 비교 (n=20, p=0.1 / 0.3 / 0.5)', fontsize=14)
plt.tight_layout()
plt.savefig('binom_pmf.png', dpi=120)
print("saved binom_pmf.png")

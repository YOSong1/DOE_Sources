# code_05_06_02.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.6 초기하 분포 - PMF 시각화
# 출처: WikiDocs book 1914, page 324473
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import hypergeom

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

M, n, N = 20, 5, 5
k_vals = np.arange(0, N + 1)
pmf_vals = hypergeom.pmf(k_vals, M, n, N)

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(k_vals, pmf_vals, color='steelblue', edgecolor='white', width=0.6)
ax.set_title(f'초기하 분포 PMF  (M={M}, n={n}, N={N})', fontsize=13)
ax.set_xlabel('불량품 개수 k')
ax.set_ylabel('P(X = k)')
ax.set_xticks(k_vals)

for k, prob in zip(k_vals, pmf_vals):
    if prob > 0.001:
        ax.text(k, prob + 0.005, f'{prob:.3f}', ha='center', fontsize=9)

ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('hyper_pmf.png', dpi=120)
print("saved hyper_pmf.png")

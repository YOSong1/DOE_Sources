# code_05_04_02.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.4 포아송 분포 - λ=1, 3, 5, 10 PMF 비교
# 출처: WikiDocs book 1914, page 324290
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

lambdas = [1, 3, 5, 10]
colors = ['steelblue', 'darkorange', 'green', 'crimson']

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.flatten()

for ax, lam, color in zip(axes, lambdas, colors):
    k = np.arange(0, int(lam * 3) + 1)
    probs = poisson.pmf(k, lam)
    ax.bar(k, probs, color=color, alpha=0.8, edgecolor='black')
    ax.axvline(lam, color='red', linestyle='--', linewidth=2, label=f'평균=분산={lam}')
    ax.set_title(f'Poisson(λ={lam})', fontsize=13)
    ax.set_xlabel('사건 발생 횟수 k')
    ax.set_ylabel('확률 P(X=k)')
    ax.legend()

plt.suptitle('포아송 분포 PMF 비교 (λ = 1, 3, 5, 10)', fontsize=14)
plt.tight_layout()
plt.savefig('poisson_pmf.png', dpi=120)
print("saved poisson_pmf.png")

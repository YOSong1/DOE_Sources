# code_05_08_02.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.8 포아송-이항 분포 - PMF 시각화
# 출처: WikiDocs book 1914, page 324316
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def poisson_binomial_pmf_dp(probs):
    n = len(probs)
    dp = np.zeros(n + 1)
    dp[0] = 1.0
    for i, p in enumerate(probs):
        for k in range(i + 1, 0, -1):
            dp[k] = dp[k] * (1 - p) + dp[k - 1] * p
        dp[0] *= (1 - p)
    return dp

probs = [0.6, 0.4, 0.7, 0.3, 0.8, 0.5, 0.6, 0.4, 0.7, 0.5]
n = len(probs)
pmf = poisson_binomial_pmf_dp(probs)
mean = sum(probs)

plt.figure(figsize=(9, 5))
plt.bar(range(n + 1), pmf, color='steelblue', edgecolor='black', alpha=0.8)
plt.axvline(mean, color='red', linestyle='--', linewidth=1.5, label=f'기댓값 = {mean:.1f}')
plt.xlabel('성공 횟수 k')
plt.ylabel('확률 P(X = k)')
plt.title('포아송-이항 분포 PMF (10경기, 경기별 승률 상이)')
plt.xticks(range(n + 1))
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('poibin_pmf.png', dpi=120)
print("saved poibin_pmf.png")

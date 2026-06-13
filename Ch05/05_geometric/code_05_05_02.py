# code_05_05_02.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.5 기하 분포 - p=0.1/0.3/0.5 PMF 비교
# 출처: WikiDocs book 1914, page 324341
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import geom

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

k = np.arange(1, 21)
p_values = [0.1, 0.3, 0.5]
colors = ['steelblue', 'tomato', 'seagreen']

fig, ax = plt.subplots(figsize=(9, 5))

for prob, color in zip(p_values, colors):
    pmf = geom.pmf(k, prob)
    ax.plot(k, pmf, marker='o', linestyle='-', color=color,
            label=f'p = {prob}  (평균 {1/prob:.1f}회)')

ax.set_title('기하 분포 PMF 비교 (성공 확률별)', fontsize=13)
ax.set_xlabel('시행 횟수 k')
ax.set_ylabel('P(X = k)')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('geom_pmf.png', dpi=120)
print("saved geom_pmf.png")

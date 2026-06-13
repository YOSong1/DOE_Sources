# code_06_04_02.py
# -*- coding: utf-8 -*-
"""
페이지: 6.4 t 분포 — 자유도별 t 분포 PDF와 표준정규분포 비교 시각화.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t, norm

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

x = np.linspace(-5, 5, 500)
degrees = [1, 3, 10, 30]
colors = ['steelblue', 'darkorange', 'green', 'red']

plt.figure(figsize=(9, 5))
for nu, c in zip(degrees, colors):
    plt.plot(x, t.pdf(x, df=nu), label=f'$\\nu={nu}$', color=c, linewidth=2)

plt.plot(x, norm.pdf(x), label='$N(0,1)$', color='black',
         linewidth=2, linestyle='--')

plt.title('t 분포 PDF — 자유도별 비교 (vs 표준정규분포)')
plt.xlabel('x')
plt.ylabel('확률 밀도 f(x)')
plt.legend()
plt.ylim(0, 0.45)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

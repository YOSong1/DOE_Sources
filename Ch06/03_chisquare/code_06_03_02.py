# code_06_03_02.py
# -*- coding: utf-8 -*-
"""
페이지: 6.3 카이제곱 분포 — 자유도별 PDF 비교 시각화.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

x = np.linspace(0.01, 30, 500)
degrees = [1, 3, 5, 10]
colors = ['steelblue', 'darkorange', 'green', 'red']

plt.figure(figsize=(9, 5))
for k, c in zip(degrees, colors):
    plt.plot(x, chi2.pdf(x, df=k), label=f'$k={k}$', color=c, linewidth=2)

plt.title('카이제곱 분포 PDF — 자유도별 비교')
plt.xlabel('x')
plt.ylabel('확률 밀도 f(x)')
plt.legend()
plt.ylim(0, 0.5)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

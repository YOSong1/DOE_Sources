# code_06_06_02.py
# -*- coding: utf-8 -*-
"""
페이지: 6.6 감마 분포 — α=1,2,5,10에 대한 PDF 비교 시각화 (β=1 고정).
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

x = np.linspace(0.01, 20, 1000)
alphas = [1, 2, 5, 10]
colors = ['steelblue', 'darkorange', 'green', 'crimson']

plt.figure(figsize=(9, 5))
for alpha_val, color in zip(alphas, colors):
    plt.plot(x, gamma.pdf(x, a=alpha_val, scale=1),
             color=color, linewidth=2, label=f"α={alpha_val}, β=1")

plt.title("감마 분포 PDF — α 변화에 따른 형태 비교 (β=1 고정)")
plt.xlabel("x")
plt.ylabel("확률 밀도")
plt.ylim(0, 0.55)
plt.legend()
plt.grid(alpha=0.4)
plt.tight_layout()
plt.show()

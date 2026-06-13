# code_06_05_02.py
# -*- coding: utf-8 -*-
"""
페이지: 6.5 F 분포 — 자유도 조합별 F 분포 PDF 비교 시각화.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

x = np.linspace(0.01, 5, 1000)
params = [(5, 10), (10, 20), (30, 30)]
colors = ['steelblue', 'darkorange', 'green']

plt.figure(figsize=(9, 5))
for (d1, d2), color in zip(params, colors):
    plt.plot(x, f.pdf(x, d1, d2), color=color, linewidth=2,
             label=f"$d_1={d1},\\ d_2={d2}$")

plt.title("F 분포 PDF — 자유도 조합 비교")
plt.xlabel("x")
plt.ylabel("확률 밀도")
plt.ylim(0, 1.2)
plt.legend()
plt.grid(alpha=0.4)
plt.tight_layout()
plt.show()

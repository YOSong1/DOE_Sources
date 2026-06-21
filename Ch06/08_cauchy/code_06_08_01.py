# code_06_08_01.py
# -*- coding: utf-8 -*-
"""
페이지: 6.8 Cauchy 분포 — 정규 분포와 PDF, 꼬리 확률 비교.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import cauchy, norm

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# --- 1. PDF 데이터 ---
x = np.linspace(-8, 8, 1000)
cauchy_pdf = cauchy.pdf(x, loc=0, scale=1)
normal_pdf = norm.pdf(x, loc=0, scale=1)

# --- 2. 시각화 (일반/로그 스케일) ---
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].plot(x, cauchy_pdf, 'b-', linewidth=2, label='Cauchy(0, 1)')
axes[0].plot(x, normal_pdf, 'r--', linewidth=2, label='Normal(0, 1)')
axes[0].set_title('Cauchy vs 정규 분포 PDF (일반 스케일)')
axes[0].set_xlabel('x')
axes[0].set_ylabel('확률 밀도')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].semilogy(x, cauchy_pdf, 'b-', linewidth=2, label='Cauchy(0, 1)')
axes[1].semilogy(x, normal_pdf, 'r--', linewidth=2, label='Normal(0, 1)')
axes[1].yaxis.set_major_formatter(ticker.LogFormatter(base=10))
axes[1].set_title('Cauchy vs 정규 분포 PDF (로그 스케일)')
axes[1].set_xlabel('x')
axes[1].set_ylabel('확률 밀도 (log)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# --- 3. 꼬리 확률 ---
print("꼬리 확률 비교 (|x| > 임계값)")
print(f"{'임계값':>6} | {'Cauchy':>12} | {'정규':>14} | {'비율':>8}")
print("-" * 48)
for tval in [2, 3, 5, 10]:
    p_c = 1 - cauchy.cdf(tval) + cauchy.cdf(-tval)
    p_n = 1 - norm.cdf(tval) + norm.cdf(-tval)
    ratio = p_c / p_n if p_n > 0 else float('inf')
    print(f"{tval:>6} | {p_c:>12.6f} | {p_n:>14.2e} | {ratio:>7.0f}배")

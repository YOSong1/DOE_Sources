# code_06_08_02.py
# -*- coding: utf-8 -*-
"""
페이지: 6.8 Cauchy 분포 — 표본 평균이 수렴하지 않음을 시뮬레이션으로 확인.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import cauchy, norm

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

np.random.seed(42)
max_n = 5000
ns = np.arange(1, max_n + 1)

cauchy_samples = cauchy.rvs(loc=0, scale=1, size=max_n)
cauchy_cum_mean = np.cumsum(cauchy_samples) / ns
cauchy_cum_median = np.array([np.median(cauchy_samples[:i]) for i in ns])

normal_samples = norm.rvs(loc=0, scale=1, size=max_n)
normal_cum_mean = np.cumsum(normal_samples) / ns

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].plot(ns, cauchy_cum_mean, 'b-', linewidth=0.7, label='표본 평균 (수렴 안 함)', alpha=0.8)
axes[0].plot(ns, cauchy_cum_median, 'g-', linewidth=1.5, label='표본 중앙값 (수렴)')
axes[0].axhline(y=0, color='red', linestyle='--', linewidth=1.5, label='위치 모수 x₀=0')
axes[0].set_title('Cauchy 분포: 표본 평균 vs 표본 중앙값')
axes[0].set_xlabel('표본 크기 n')
axes[0].set_ylabel('누적 통계량 값')
axes[0].legend()
axes[0].grid(True, alpha=0.3)
axes[0].set_ylim(-10, 10)

axes[1].plot(ns, normal_cum_mean, 'r-', linewidth=0.7, label='정규 분포 표본 평균')
axes[1].axhline(y=0, color='red', linestyle='--', linewidth=1.5, label='모평균 μ=0')
axes[1].set_title('정규 분포: 표본 평균 (수렴함)')
axes[1].set_xlabel('표본 크기 n')
axes[1].set_ylabel('누적 표본 평균')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# code_06_02_01.py
# -*- coding: utf-8 -*-
"""
페이지: 6.2 지수 분포 (Exponential Distribution)
설명: λ=2 (1분당 평균 2건)인 지수분포로 고객 도착 간격을 모델링하고
       λ 변화에 따른 PDF를 비교 시각화한다.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# 1. 기본 확률 계산 (λ=2, 즉 1분에 평균 2명 도착)
lambda_rate = 2
scale = 1 / lambda_rate  # scale = 0.5분

prob_within_1 = expon.cdf(1, scale=scale)
print(f"1분 이내 도착 확률: {prob_within_1:.4f} ({prob_within_1*100:.2f}%)")

prob_over_2 = expon.sf(2, scale=scale)
print(f"2분 이상 대기 확률: {prob_over_2:.4f} ({prob_over_2*100:.2f}%)")

median_time = expon.ppf(0.5, scale=scale)
print(f"중앙값 대기 시간: {median_time:.4f}분")

# 2. λ=0.5, 1, 2에 따른 PDF 비교 시각화
x = np.linspace(0, 6, 500)
lambda_vals = [0.5, 1.0, 2.0]
colors = ['파랑', '초록', '빨강']
color_map = {'파랑': 'blue', '초록': 'green', '빨강': 'red'}

plt.figure(figsize=(9, 5))
for lam, c in zip(lambda_vals, colors):
    s = 1 / lam
    plt.plot(x, expon.pdf(x, scale=s),
             label=rf'$\lambda={lam}$ (평균 대기 {s:.1f}분)',
             color=color_map[c], linewidth=2)

plt.title('지수 분포 PDF — λ 변화 비교')
plt.xlabel('대기 시간 (분)')
plt.ylabel('확률 밀도')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

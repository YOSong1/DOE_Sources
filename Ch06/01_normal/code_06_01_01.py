# code_06_01_01.py
# -*- coding: utf-8 -*-
"""
페이지: 6.1 정규 분포 (Normal Distribution)
설명: 시험 성적 분포를 정규 분포 N(μ=70, σ=10)로 모델링하여 확률, 백분위수,
       신뢰구간을 계산하고, μ와 σ에 따른 PDF를 비교 시각화한다.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')  # Windows
plt.rc('axes', unicode_minus=False)

# 1. 기본 확률 계산 (μ=70, σ=10인 성적 분포)
mu, sigma = 70, 10

# 80점 이상일 확률
prob_above_80 = norm.sf(80, loc=mu, scale=sigma)
print(f"80점 이상 확률: {prob_above_80:.4f} ({prob_above_80*100:.2f}%)")

# 60~80점 사이일 확률
prob_60_80 = norm.cdf(80, loc=mu, scale=sigma) - norm.cdf(60, loc=mu, scale=sigma)
print(f"60~80점 확률: {prob_60_80:.4f} ({prob_60_80*100:.2f}%)")

# 상위 10% 커트라인
cutoff_top10 = norm.ppf(0.90, loc=mu, scale=sigma)
print(f"상위 10% 커트라인: {cutoff_top10:.2f}점")

# 95% 신뢰 구간
ci = norm.interval(0.95, loc=mu, scale=sigma)
print(f"95% 신뢰 구간: [{ci[0]:.2f}, {ci[1]:.2f}]점")

# 2. μ와 σ 변화에 따른 PDF 비교 시각화
x = np.linspace(20, 120, 500)

params = [
    (70, 5,  '파랑', r'$\mu=70,\,\sigma=5$'),
    (70, 10, '초록', r'$\mu=70,\,\sigma=10$'),
    (70, 20, '주황', r'$\mu=70,\,\sigma=20$'),
    (60, 10, '빨강', r'$\mu=60,\,\sigma=10$'),
]

plt.figure(figsize=(10, 5))
for m, s, color, label in params:
    plt.plot(x, norm.pdf(x, loc=m, scale=s), label=label, linewidth=2)

plt.title('정규 분포 PDF — μ와 σ 변화 비교')
plt.xlabel('점수')
plt.ylabel('확률 밀도')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

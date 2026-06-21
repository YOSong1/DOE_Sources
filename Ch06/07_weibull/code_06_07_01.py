# code_06_07_01.py
# -*- coding: utf-8 -*-
"""
페이지: 6.7 Weibull 분포 — k=2, λ=1000 시간으로 전구 수명을 분석하고
k별 PDF를 비교한다.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import weibull_min
import matplotlib.ticker as ticker

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# --- 1. 매개변수 설정 ---
k = 2.0
lambda_ = 1000

# --- 2. 기댓값, 분산 ---
mean_life = weibull_min.mean(c=k, scale=lambda_)
var_life = weibull_min.var(c=k, scale=lambda_)
print(f"평균 수명: {mean_life:.1f} 시간")
print(f"수명 표준편차: {np.sqrt(var_life):.1f} 시간")

# --- 3. 핵심 확률 ---
t_warranty = 500
p_fail = weibull_min.cdf(t_warranty, c=k, scale=lambda_)
print(f"{t_warranty}시간 내 고장 확률: {p_fail:.4f} ({p_fail*100:.2f}%)")

t_5pct = weibull_min.ppf(0.05, c=k, scale=lambda_)
print(f"고장률 5% 이하 보증 기간: {t_5pct:.1f} 시간")

# --- 4. k별 PDF 비교 (λ=1) ---
x = np.linspace(0, 3, 500)   # x=0.0001 수정 후 진행
k_values = [0.5, 1.0, 2.0, 5.0]
colors = ['blue', 'green', 'orange', 'red']
labels = ['k=0.5 (초기 고장↓)', 'k=1 (지수 분포)', 'k=2 (레일리 분포)', 'k=5 (마모 고장↑)']

plt.figure(figsize=(9, 5))
for k_val, color, label in zip(k_values, colors, labels):
    pdf = weibull_min.pdf(x, c=k_val, scale=1.0)
    plt.plot(x, pdf, color=color, linewidth=2, label=label)

plt.title('Weibull 분포 PDF — 형상 매개변수 k별 비교 (λ=1)')
plt.xlabel('x')
plt.ylabel('확률 밀도 f(x)')
plt.legend()
plt.ylim(0, 2.5)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

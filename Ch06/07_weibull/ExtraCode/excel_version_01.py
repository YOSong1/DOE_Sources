# -*- coding: utf-8 -*-
"""
페이지: 6.7 Weibull 분포
Excel 활용 버전: sample_bulb_lifetime.xlsx의 전구 수명 200개 표본을
scipy.stats.weibull_min.fit으로 적합하고, 보증 기간 분석을 수행한다.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import weibull_min

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_bulb_lifetime.xlsx'))
x = df['수명_시간'].values
print(f"[Excel] n = {len(x)},  평균 = {x.mean():.1f}h,  중앙값 = {np.median(x):.1f}h\n")

# 1) MLE 적합 (floc=0: 위치 모수를 0으로 고정)
c_hat, loc_, scale_hat = weibull_min.fit(x, floc=0)
print(f"적합 결과 (MLE): k̂ = {c_hat:.4f}, λ̂ = {scale_hat:.4f}")
if c_hat < 1:
    print("  → k<1: 초기 고장 패턴 (bathtub의 좌측)")
elif c_hat == 1:
    print("  → k=1: 지수분포와 동일 (우발 고장)")
else:
    print("  → k>1: 마모 고장 (시간 경과에 따라 고장률 증가)")

# 2) 평균, 분산을 모수와 감마함수로 직접 검산
from scipy.special import gamma as Gfun
mean_th = scale_hat * Gfun(1 + 1/c_hat)
var_th = scale_hat**2 * (Gfun(1 + 2/c_hat) - Gfun(1 + 1/c_hat)**2)
print(f"\n이론 평균 = λ·Γ(1+1/k) = {scale_hat:.2f} × Γ({1+1/c_hat:.3f}) = {mean_th:.2f}")
print(f"표본 평균 = {x.mean():.2f}  (둘이 비슷해야 함)")
print(f"이론 표준편차 = {np.sqrt(var_th):.2f}, 표본 표준편차 = {x.std(ddof=1):.2f}")

# 3) 보증 기간 분석
t_warr = 500
p_fail = weibull_min.cdf(t_warr, c=c_hat, scale=scale_hat)
t_5pct = weibull_min.ppf(0.05, c=c_hat, scale=scale_hat)
print(f"\n{t_warr}h 내 고장 확률(적합 모형): {p_fail:.4f}")
print(f"실제 표본에서 {t_warr}h 이하 비율: {(x <= t_warr).mean():.4f}")
print(f"5% 고장 보증 기간 추정: {t_5pct:.1f}h")

# 4) 히스토그램 + 적합 PDF + 생존함수
xs = np.linspace(1, x.max() * 1.1, 300)
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
axes[0].hist(x, bins=25, density=True, alpha=0.5, color='steelblue',
             edgecolor='white', label='관측치')
axes[0].plot(xs, weibull_min.pdf(xs, c=c_hat, scale=scale_hat),
             'r-', linewidth=2, label=f'Weibull(k̂={c_hat:.2f}, λ̂={scale_hat:.0f})')
axes[0].set_title('전구 수명 분포 적합')
axes[0].set_xlabel('수명(h)')
axes[0].set_ylabel('밀도')
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].plot(xs, weibull_min.sf(xs, c=c_hat, scale=scale_hat),
             'g-', linewidth=2, label='S(t) = 1-F(t)')
axes[1].set_title('생존 함수 (Reliability)')
axes[1].set_xlabel('시간(h)')
axes[1].set_ylabel('생존 확률')
axes[1].grid(alpha=0.3)
axes[1].legend()
plt.tight_layout()
plt.show()

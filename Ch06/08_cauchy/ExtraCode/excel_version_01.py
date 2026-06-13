# -*- coding: utf-8 -*-
"""
페이지: 6.8 Cauchy 분포
Excel 활용 버전: sample_stock_returns.xlsx의 일간 수익률에서
표본 평균/중앙값의 안정성을 비교하고, Cauchy 적합과 정규 적합을 시각적으로 대비.
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
from scipy.stats import cauchy, norm

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_stock_returns.xlsx'))
r = df['수익률'].values
print(f"[Excel] n = {len(r)}\n", df.describe(), '\n')

# 1) 평균 vs 중앙값 (Cauchy 같은 heavy-tail에서는 평균이 불안정)
print("--- 위치 추정량 비교 ---")
print(f"표본 평균   : {r.mean():.6f}  (Cauchy에서는 발산할 수 있음)")
print(f"표본 중앙값 : {np.median(r):.6f}  (Cauchy의 위치 모수 추정에 권장)")
print(f"표본 IQR/2  : {(np.percentile(r, 75) - np.percentile(r, 25))/2:.6f}  (척도 γ 추정)")

# 2) Cauchy 적합
loc_c, scale_c = cauchy.fit(r)
print(f"\nCauchy 적합: x̂₀ = {loc_c:.6f},  γ̂ = {scale_c:.6f}")

# 3) 정규 적합 (비교용)
mu_n, sigma_n = norm.fit(r)
print(f"정규 적합  : μ̂ = {mu_n:.6f},  σ̂ = {sigma_n:.6f}")

# 4) 누적 평균/중앙값 시각화
ns = np.arange(1, len(r) + 1)
cum_mean = np.cumsum(r) / ns
cum_median = np.array([np.median(r[:i]) for i in ns])

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(ns, cum_mean, label='누적 평균', alpha=0.7)
axes[0].plot(ns, cum_median, label='누적 중앙값', linewidth=1.5)
axes[0].axhline(0, color='red', linestyle='--', label='기준 0')
axes[0].set_title('관측 수익률: 누적 평균 vs 중앙값')
axes[0].set_xlabel('거래일 누적')
axes[0].legend()
axes[0].grid(alpha=0.3)

# 5) 히스토그램 + 두 적합 PDF
xs = np.linspace(np.percentile(r, 1), np.percentile(r, 99), 500)
axes[1].hist(r, bins=80, density=True, alpha=0.5, color='gray',
             edgecolor='white', label='수익률 히스토그램')
axes[1].plot(xs, cauchy.pdf(xs, loc=loc_c, scale=scale_c), 'b-',
             linewidth=2, label='Cauchy 적합')
axes[1].plot(xs, norm.pdf(xs, loc=mu_n, scale=sigma_n), 'r--',
             linewidth=2, label='정규 적합')
axes[1].set_xlim(np.percentile(r, 1), np.percentile(r, 99))
axes[1].set_title('수익률 분포: Cauchy vs 정규 적합')
axes[1].set_xlabel('일간 수익률')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\n[해석] heavy-tail 데이터에서는 Cauchy 적합이 더 잘 맞는 경향이 있습니다.")
print("       정규 분포 가정 시 극단값 발생 확률을 과소평가하게 됩니다.")

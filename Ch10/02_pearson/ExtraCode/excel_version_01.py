# -*- coding: utf-8 -*-
"""
페이지: 10.2 피어슨 상관계수
Excel 활용 버전: sample_study_score.xlsx로 r을 공분산/표준편차 공식으로 직접 계산하고,
Fisher Z 변환으로 95% 신뢰구간을 구한다.
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
from scipy import stats

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_study_score.xlsx'))
print(f"[Excel] n = {len(df)}\n", df, '\n')

x = df['공부시간_h'].values
y = df['시험점수'].values
n = len(x)

# 1) r 공식 직접 계산
x_bar, y_bar = x.mean(), y.mean()
cov_xy = ((x - x_bar) * (y - y_bar)).sum() / (n - 1)
sx, sy = x.std(ddof=1), y.std(ddof=1)
r_manual = cov_xy / (sx * sy)
print(f"x̄ = {x_bar:.3f}, ȳ = {y_bar:.3f}")
print(f"Cov(x,y) = {cov_xy:.4f}, sₓ = {sx:.4f}, sy = {sy:.4f}")
print(f"r = Cov(x,y) / (sₓ·sy) = {r_manual:.4f}")

# 2) scipy 비교
r_sp, p_sp = stats.pearsonr(x, y)
print(f"\nscipy: r = {r_sp:.4f}, p = {p_sp:.4e}")

# 3) Fisher Z 변환을 통한 95% CI
z = 0.5 * np.log((1 + r_sp) / (1 - r_sp))
se_z = 1 / np.sqrt(n - 3)
z_lo, z_up = z - 1.96 * se_z, z + 1.96 * se_z
r_lo = (np.exp(2*z_lo) - 1) / (np.exp(2*z_lo) + 1)
r_up = (np.exp(2*z_up) - 1) / (np.exp(2*z_up) + 1)
print(f"\nFisher Z = 0.5·ln((1+r)/(1-r)) = {z:.4f}")
print(f"95% CI for ρ: [{r_lo:.4f}, {r_up:.4f}]")

# 4) 결정계수 R²
print(f"\n결정계수 R² = r² = {r_sp**2:.4f}")
print(f"  → y 변동의 {r_sp**2*100:.1f}%를 x로 설명")

# 5) 시각화
m, b = np.polyfit(x, y, 1)
xs = np.linspace(x.min(), x.max(), 100)
plt.figure(figsize=(8, 5))
plt.scatter(x, y, s=80, alpha=0.8)
plt.plot(xs, m * xs + b, 'r-', linewidth=2, label=f'추세 y={m:.2f}x+{b:.2f}')
plt.title(f'공부시간 vs 시험점수 (r={r_sp:.3f})')
plt.xlabel('공부시간(h)')
plt.ylabel('시험점수')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

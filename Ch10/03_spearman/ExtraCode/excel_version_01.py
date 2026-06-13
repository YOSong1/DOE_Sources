# -*- coding: utf-8 -*-
"""
페이지: 10.3 스피어만 순위 상관계수
Excel 활용 버전: sample_with_outlier.xlsx로 ρ를 단순화 공식
ρ = 1 - 6·Σd² / (n(n²-1)) 로 직접 계산하고, 이상치 제거 시 r과 ρ가 어떻게 달라지는지 비교.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_with_outlier.xlsx'))
print(f"[Excel] n = {len(df)}\n", df, '\n')

x = df['공부시간_h'].values
y = df['시험점수'].values
n = len(x)

# 1) 단순화 공식 직접 계산 (동순위 없는 경우)
rx = stats.rankdata(x)
ry = stats.rankdata(y)
d = rx - ry
rho_manual = 1 - 6 * (d**2).sum() / (n * (n**2 - 1))
print("--- 스피어만 ρ 직접 계산 ---")
print(pd.DataFrame({'x': x, 'y': y, 'rank_x': rx, 'rank_y': ry, 'd': d, 'd²': d**2}))
print(f"Σd² = {(d**2).sum():.2f}, n(n²-1) = {n*(n**2-1)}")
print(f"ρ = 1 - 6·Σd² / (n(n²-1)) = {rho_manual:.4f}")

# 2) scipy 결과
rho_sp, p_sp = stats.spearmanr(x, y)
r_p, p_p = stats.pearsonr(x, y)
print(f"\nscipy 스피어만 ρ = {rho_sp:.4f}, p = {p_sp:.4f}")
print(f"scipy 피어슨   r = {r_p:.4f}, p = {p_p:.4f}")

# 3) 이상치 제거 후 비교
mask = x < 20  # 이상치(50) 제외
r_clean = stats.pearsonr(x[mask], y[mask])[0]
rho_clean = stats.spearmanr(x[mask], y[mask])[0]
print(f"\n이상치 제거 후 (n={mask.sum()}):")
print(f"  피어슨 r   = {r_clean:.4f}  ({r_p:.4f} → {r_clean:.4f})")
print(f"  스피어만 ρ = {rho_clean:.4f}  ({rho_sp:.4f} → {rho_clean:.4f})")

# 4) 시각화: 원본 vs 순위
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].scatter(x, y, s=80, alpha=0.7)
axes[0].set_title(f'원본 (r={r_p:.3f}, ρ={rho_sp:.3f})')
axes[0].set_xlabel('공부시간')
axes[0].set_ylabel('성적')
axes[0].grid(alpha=0.3)

axes[1].scatter(rx, ry, s=80, alpha=0.7, color='tomato')
axes[1].set_title('순위 변환 — 이상치 효과 소멸')
axes[1].set_xlabel('공부시간 순위')
axes[1].set_ylabel('성적 순위')
axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.show()

print("\n[해석] 피어슨은 이상치에 민감해 관계를 과소평가, 스피어만은 순위만 보므로 견고함.")

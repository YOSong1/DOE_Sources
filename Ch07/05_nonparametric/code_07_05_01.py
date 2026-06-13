# code_07_05_01.py
# -*- coding: utf-8 -*-
"""
페이지: 7.5 비모수 검정 — (1) 만-위트니 U 검정 (지수 분포 데이터).
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

np.random.seed(42)
group_a = np.random.exponential(scale=1.0, size=30)
group_b = np.random.exponential(scale=1.5, size=35)

_, p_a = stats.shapiro(group_a)
_, p_b = stats.shapiro(group_b)
print(f"Shapiro-Wilk p-값 — 그룹 A: {p_a:.4f}, 그룹 B: {p_b:.4f}")
if p_a < 0.05 or p_b < 0.05:
    print("정규성 가정 충족 안 됨 → 비모수 검정 사용")

u_stat, p_value = stats.mannwhitneyu(group_a, group_b, alternative='two-sided')
print(f"\nU-통계량: {u_stat:.4f}")
print(f"p-값: {p_value:.4f}")

if p_value < 0.05:
    print("결론: 두 집단 분포가 유의미하게 다릅니다.")
else:
    print("결론: 두 집단 분포가 같다는 가설을 기각하지 못합니다.")

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].hist(group_a, bins=12, color="steelblue", alpha=0.7, label="그룹 A")
axes[0].hist(group_b, bins=12, color="coral", alpha=0.7, label="그룹 B")
axes[0].set_title("분포 비교 (히스토그램)")
axes[0].legend()
axes[1].boxplot([group_a, group_b], tick_labels=["그룹 A", "그룹 B"])
axes[1].set_title("분포 비교 (박스플롯)")
plt.tight_layout()
plt.show()

# code_07_02_02.py
# -*- coding: utf-8 -*-
"""
페이지: 7.2 F-검정 — (2) 일원 ANOVA: 세 비료의 식물 성장량 비교.
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
fertilizer_a = np.random.normal(loc=20, scale=3, size=15)
fertilizer_b = np.random.normal(loc=22, scale=3, size=15)
fertilizer_c = np.random.normal(loc=25, scale=3, size=15)

f_stat, p_value = stats.f_oneway(fertilizer_a, fertilizer_b, fertilizer_c)
print(f"F-통계량: {f_stat:.4f}")
print(f"p-값: {p_value:.4f}")

if p_value < 0.05:
    print("결론: 적어도 하나의 비료 집단 평균이 다릅니다.")
    print("→ 사후 검정(Tukey HSD)을 통해 어느 집단이 다른지 확인하세요.")
else:
    print("결론: 세 비료의 평균 성장량이 같다는 가설을 기각하지 못합니다.")

plt.boxplot([fertilizer_a, fertilizer_b, fertilizer_c],
            tick_labels=["비료 A", "비료 B", "비료 C"])
plt.title("비료 종류에 따른 식물 성장량 비교")
plt.ylabel("성장량 (cm)")
plt.grid(True)
plt.show()

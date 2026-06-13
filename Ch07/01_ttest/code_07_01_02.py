# code_07_01_02.py
# -*- coding: utf-8 -*-
"""
페이지: 7.1 t-검정 — (2) 독립표본 (Welch) t검정: 신약 vs 기존약.
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
new_drug = np.random.normal(loc=10, scale=2, size=20)
existing_drug = np.random.normal(loc=7, scale=3, size=20)

levene_stat, levene_p = stats.levene(new_drug, existing_drug)
print(f"Levene 등분산 검정 p-값: {levene_p:.4f}")

t_stat, p_value = stats.ttest_ind(new_drug, existing_drug, equal_var=False)
print(f"t-통계량: {t_stat:.4f}")
print(f"p-값: {p_value:.4f}")

if p_value < 0.05:
    print("결론: 두 약물의 평균 효과가 유의미하게 다릅니다. (H₀ 기각)")
else:
    print("결론: 두 약물의 평균 효과 차이가 유의미하지 않습니다.")

plt.boxplot([new_drug, existing_drug], tick_labels=["신약", "기존 약"])
plt.title("두 약물의 효과 비교")
plt.ylabel("효과 (혈압 감소량)")
plt.grid(True)
plt.show()

# code_07_05_03.py
# -*- coding: utf-8 -*-
"""
페이지: 7.5 비모수 검정 — (3) 크루스칼-왈리스 검정 (세 식단의 체중 감량).
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy import stats

np.random.seed(42)
diet_a = np.random.exponential(scale=2, size=20)
diet_b = np.random.exponential(scale=3, size=20)
diet_c = np.random.exponential(scale=4, size=20)

h_stat, p_value = stats.kruskal(diet_a, diet_b, diet_c)
print(f"H-통계량: {h_stat:.4f}")
print(f"p-값: {p_value:.4f}")

if p_value < 0.05:
    print("결론: 적어도 하나의 식단 집단 분포가 다릅니다.")
    print("→ 사후 검정(Dunn 검정 등)으로 어느 집단이 다른지 확인하세요.")
else:
    print("결론: 세 식단 집단 분포가 같다는 가설을 기각하지 못합니다.")

# code_07_05_02.py
# -*- coding: utf-8 -*-
"""
페이지: 7.5 비모수 검정 — (2) 윌콕슨 부호 순위 검정 (명상 전후 스트레스).
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy import stats

np.random.seed(42)
before = np.random.exponential(scale=5, size=20) + 5
after = before - np.random.exponential(scale=2, size=20)

w_stat, p_value = stats.wilcoxon(before, after, alternative='two-sided')
print(f"W-통계량: {w_stat:.4f}")
print(f"p-값: {p_value:.4f}")
print(f"중앙값 변화: {np.median(before):.2f} → {np.median(after):.2f}")

if p_value < 0.05:
    print("결론: 명상 전후 스트레스 지수가 유의미하게 변화했습니다.")
else:
    print("결론: 명상 전후 스트레스 지수 변화가 유의미하지 않습니다.")

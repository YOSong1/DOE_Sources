# code_07_03_02.py
# -*- coding: utf-8 -*-
"""
페이지: 7.3 카이제곱 검정 — (2) 독립성 검정 (광고 유형 vs 구매 여부).
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
from scipy import stats

observed = np.array([
    [50, 30],
    [20, 50],
    [30, 20],
])

df_obs = pd.DataFrame(
    observed,
    index=["광고 A", "광고 B", "광고 C"],
    columns=["구매", "미구매"]
)
print("관찰 빈도표:")
print(df_obs)

chi2_stat, p_value, dof, expected = stats.chi2_contingency(observed)
print(f"\n카이제곱 통계량: {chi2_stat:.4f}")
print(f"p-값: {p_value:.4f}")
print(f"자유도: {dof}")
print(f"\n기대 빈도표:")
print(pd.DataFrame(expected, index=["광고 A", "광고 B", "광고 C"], columns=["구매", "미구매"]))

if p_value < 0.05:
    print("\n결론: 광고 유형과 구매 여부 사이에 유의미한 연관이 있습니다.")
else:
    print("\n결론: 광고 유형과 구매 여부가 독립이라는 가설을 기각하지 못합니다.")

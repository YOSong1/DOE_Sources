# code_10_05_01.py
# -*- coding: utf-8 -*-
"""
페이지: 10.5 점-이계열 상관계수 — 시험 점수와 합격 여부 관계.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

data_exam = {
    'student_id': range(1, 21),
    'test_score': [56, 75, 45, 71, 62, 50, 49, 90, 65, 85,
                   55, 78, 40, 68, 72, 51, 60, 80, 47, 92],
    'pass_fail':  [0, 1, 0, 1, 1, 0, 0, 1, 1, 1,
                   0, 1, 0, 1, 1, 0, 1, 1, 0, 1]
}
df_exam = pd.DataFrame(data_exam)

r_pb, p_value = stats.pointbiserialr(df_exam['pass_fail'], df_exam['test_score'])
print(f"점-이계열 상관계수 (r_pb): {r_pb:.3f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("시험 점수와 합격 여부 간에 통계적으로 유의미한 상관관계가 있습니다.")
else:
    print("통계적으로 유의미한 상관관계를 확인할 수 없습니다.")

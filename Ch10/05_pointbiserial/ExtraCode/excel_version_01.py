# -*- coding: utf-8 -*-
"""
페이지: 10.5 점-이계열 상관계수
Excel 활용 버전: sample_pass_score.xlsx로 r_pb를 공식
r_pb = (M₁-M₀)/s · √(pq) 로 직접 계산하고 pearsonr / pointbiserialr 결과와 비교.
또한 독립표본 t-검정과 동등성을 확인한다.
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
df = pd.read_excel(os.path.join(HERE, 'sample_pass_score.xlsx'))
print(f"[Excel] n = {len(df)}\n")

x = df['시험점수'].values
g = df['합격여부'].values
n = len(x)

# 1) 그룹별 통계량
m1 = x[g == 1].mean()
m0 = x[g == 0].mean()
n1 = (g == 1).sum()
n0 = (g == 0).sum()
p = n1 / n
q = n0 / n
s = x.std(ddof=1)  # 전체 표본 표준편차
print(f"합격(1) 그룹: n₁={n1}, M₁={m1:.3f}")
print(f"불합격(0) 그룹: n₀={n0}, M₀={m0:.3f}")
print(f"전체 표준편차 s = {s:.4f}")
print(f"p = n₁/n = {p:.3f}, q = n₀/n = {q:.3f}")

# 2) 공식 직접 계산: r_pb = (M₁ - M₀)/s · √(pq)
r_pb_manual = (m1 - m0) / s * np.sqrt(p * q)
print(f"\nr_pb = (M₁-M₀)/s · √(pq) = ({m1:.3f}-{m0:.3f})/{s:.3f} · √({p*q:.4f}) = {r_pb_manual:.4f}")

# 3) scipy 비교
r_pb_sp, p_sp = stats.pointbiserialr(g, x)
r_pear, p_pear = stats.pearsonr(g, x)
print(f"\nscipy pointbiserialr: {r_pb_sp:.4f}, p = {p_sp:.4e}")
print(f"scipy pearsonr (동일): {r_pear:.4f}, p = {p_pear:.4e}")
print("  → 두 함수가 같은 값을 내는 이유는 r_pb가 피어슨의 특수 경우이기 때문.")

# 4) 독립표본 t-검정과의 관계
t_stat, t_p = stats.ttest_ind(x[g == 1], x[g == 0], equal_var=True)
print(f"\n독립 t-검정: t = {t_stat:.4f}, p = {t_p:.4f}")
# r_pb와 t의 관계: r_pb = t / sqrt(t² + df)
df_t = n - 2
r_from_t = t_stat / np.sqrt(t_stat**2 + df_t)
print(f"  t로부터 변환: r_pb = t/√(t²+df) = {r_from_t:.4f}")

# 5) 시각화
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
# 박스플롯
axes[0].boxplot([x[g==0], x[g==1]], tick_labels=['불합격', '합격'])
axes[0].set_title(f'r_pb = {r_pb_sp:.3f}, p = {p_sp:.4f}')
axes[0].set_ylabel('시험 점수')
axes[0].grid(alpha=0.3)
# 산점도 (이진 변수 jitter)
np.random.seed(0)
jit = g + np.random.uniform(-0.1, 0.1, n)
axes[1].scatter(jit, x, alpha=0.7, s=80)
axes[1].set_xticks([0, 1])
axes[1].set_xticklabels(['불합격', '합격'])
axes[1].set_title('합격 여부 vs 점수 (jitter 산점도)')
axes[1].set_ylabel('시험 점수')
axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.show()

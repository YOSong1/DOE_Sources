# -*- coding: utf-8 -*-
"""
페이지: 7.1 t-검정
Excel 활용 버전: sample_tests.xlsx의 세 시트를 차례로 읽어
단일/독립/대응 t검정을 동일한 절차로 수행하고, 효과 크기(Cohen's d)도 함께 계산한다.
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

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'sample_tests.xlsx')


def cohens_d(a, b):
    """독립표본 효과 크기"""
    nx, ny = len(a), len(b)
    sx, sy = a.std(ddof=1), b.std(ddof=1)
    sp = np.sqrt(((nx-1)*sx**2 + (ny-1)*sy**2) / (nx + ny - 2))
    return (a.mean() - b.mean()) / sp


# === (1) 단일표본 t검정: 부품 길이 vs 50mm ===
print("=" * 60)
print("(1) 단일표본 t검정 — 부품 길이가 50mm인가?")
print("=" * 60)
df1 = pd.read_excel(XLSX, sheet_name='부품길이')
x = df1['길이_mm'].values
n = len(x)
x_bar, s = x.mean(), x.std(ddof=1)
t_man = (x_bar - 50) / (s / np.sqrt(n))
t_stat, p = stats.ttest_1samp(x, 50)
print(f"n={n}, x̄={x_bar:.4f}, s={s:.4f}")
print(f"수동 t = (x̄-μ₀)/(s/√n) = {t_man:.4f}")
print(f"scipy t={t_stat:.4f}, p={p:.4f}, 결론: {'기각' if p<0.05 else '유지'}")

# === (2) 독립표본 (Welch) t검정 ===
print("\n" + "=" * 60)
print("(2) 독립표본 t검정 — 신약 vs 기존약")
print("=" * 60)
df2 = pd.read_excel(XLSX, sheet_name='약물효과')
new = df2['신약'].values
old = df2['기존약'].values
print(f"신약: n={len(new)}, 평균={new.mean():.3f}, 표준편차={new.std(ddof=1):.3f}")
print(f"기존: n={len(old)}, 평균={old.mean():.3f}, 표준편차={old.std(ddof=1):.3f}")

# 등분산성 확인 → Welch
lev = stats.levene(new, old)
print(f"Levene 등분산 p-값: {lev.pvalue:.4f}  → Welch t-test 사용 권장")
t_w, p_w = stats.ttest_ind(new, old, equal_var=False)
print(f"Welch t = {t_w:.4f}, p = {p_w:.4f}")
print(f"Cohen's d 효과크기 = {cohens_d(new, old):.3f}")
print(f"결론: {'두 약물 평균 차이 유의' if p_w<0.05 else '차이 비유의'}")

# === (3) 대응표본 t검정 ===
print("\n" + "=" * 60)
print("(3) 대응표본 t검정 — 운동 전후 혈압")
print("=" * 60)
df3 = pd.read_excel(XLSX, sheet_name='운동전후혈압')
b = df3['운동전'].values
a = df3['운동후'].values
d = b - a
print(f"n={len(d)}, 평균 차이 d̄={d.mean():.3f}, sd={d.std(ddof=1):.3f}")
t_p = d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))
t_stat3, p3 = stats.ttest_rel(b, a)
print(f"수동 t = d̄ / (s_d/√n) = {t_p:.4f}")
print(f"scipy t={t_stat3:.4f}, p={p3:.4f}")
# 대응 효과 크기 (Cohen's d_z)
dz = d.mean() / d.std(ddof=1)
print(f"Cohen's d_z (대응) = {dz:.3f}")
print(f"결론: {'운동 효과 유의' if p3<0.05 else '운동 효과 비유의'}")

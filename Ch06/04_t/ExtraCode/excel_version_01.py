# -*- coding: utf-8 -*-
"""
페이지: 6.4 t 분포
Excel 활용 버전: sample_blood_pressure.xlsx의 25명 환자 혈압을 읽어
단일표본 t검정을 수행하고, t 통계량 수식의 각 항을 명시적으로 계산한다.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import numpy as np
import pandas as pd
from scipy.stats import t as tdist, ttest_1samp

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_blood_pressure.xlsx'))
print(f"[Excel] 표본 크기 n = {len(df)}\n", df.describe(), '\n')

x = df['혈압'].values
n = len(x)
mu0 = 120.0  # 귀무가설: 평균 혈압 = 120

# 1) 표본 통계량
x_bar = x.mean()
s = x.std(ddof=1)
se = s / np.sqrt(n)
print(f"x̄ = {x_bar:.4f}, s = {s:.4f}, SE = s/√n = {se:.4f}")

# 2) t 통계량을 수식대로 계산
t_manual = (x_bar - mu0) / se
nu = n - 1
print(f"t = (x̄ - μ₀) / SE = ({x_bar:.4f} - {mu0}) / {se:.4f} = {t_manual:.4f}")
print(f"자유도 ν = n - 1 = {nu}")

# 3) scipy 결과와 비교
t_stat, p_val = ttest_1samp(x, mu0)
print(f"\nscipy 결과: t = {t_stat:.4f}, p = {p_val:.4f}")
print(f"수동 p값(양측): {2 * tdist.sf(abs(t_manual), nu):.4f}")

# 4) 95% 신뢰구간
ci_low = x_bar - tdist.ppf(0.975, nu) * se
ci_up = x_bar + tdist.ppf(0.975, nu) * se
print(f"\n95% CI for μ: [{ci_low:.4f}, {ci_up:.4f}]")
if not (ci_low <= mu0 <= ci_up):
    print(f"  → 신뢰구간이 μ₀={mu0}을 포함하지 않음 → H₀ 기각")
else:
    print(f"  → 신뢰구간이 μ₀={mu0}을 포함 → H₀ 기각 실패")

# 5) 결과 해석
print("\n[해석]")
if p_val < 0.05:
    print("  신약 투여 후 평균 혈압이 120과 통계적으로 유의미하게 다릅니다.")
else:
    print("  신약 투여 후 평균 혈압이 120과 다르다는 충분한 근거가 없습니다.")

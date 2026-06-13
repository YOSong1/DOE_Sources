# code_12_02_02.py
# -*- coding: utf-8 -*-
"""
페이지: 12.2 부분 요인 실험의 절차
설명: 2^(4-1) 설계 (Generator: D = ABC) 의 예시 데이터에 대한 ANOVA 분석.
"""

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# 예시: 2^(4-1) 설계, Generator D = ABC
data = pd.DataFrame({
    'A': [-1,-1,-1,-1, 1, 1, 1, 1],
    'B': [-1,-1, 1, 1,-1,-1, 1, 1],
    'C': [-1, 1,-1, 1,-1, 1,-1, 1],
    'D': [-1, 1, 1,-1, 1,-1,-1, 1],  # D = ABC
    'y': [45, 71, 48, 65, 68, 60, 80, 65]
})

# 주효과 + 2차 상호작용 분석 (교락 고려하여 선택적으로 포함)
model = ols('y ~ A + B + C + D + A:B + A:C', data=data).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

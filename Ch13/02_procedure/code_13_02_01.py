# code_13_02_01.py
# -*- coding: utf-8 -*-
"""
페이지: 13.2 응답 표면 방법론의 일반적인 절차
설명: 2요인 CCD 예시 데이터에 대한 2차 모형 적합 및 ANOVA.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# CCD 실험 데이터 예시 (2요인: x1, x2)
data = pd.DataFrame({
    'x1': [-1, -1,  1,  1,  0,  0, -1.414,  1.414, 0, 0],
    'x2': [-1,  1, -1,  1, -1.414,  1.414, 0, 0, 0, 0],
    'y' : [52, 74, 62, 80, 45, 86, 55, 77, 90, 88]
})

# 2차 모형 적합 (주효과 + 2차항 + 상호작용항)
model = ols('y ~ x1 + x2 + I(x1**2) + I(x2**2) + x1:x2', data=data).fit()
print(model.summary())

# ANOVA 테이블
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

# code_11_02_02.py
# -*- coding: utf-8 -*-
"""
페이지: 11.2 완전 요인 실험의 절차
설명: 3요인 2수준 데이터에 대한 ANOVA 분석 예시.
      statsmodels의 ols로 주효과와 2차 상호작용을 포함하는 모형을 적합한다.
"""

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# 예시 데이터 (A, B, C: 요인, y: 반응변수)
data = pd.DataFrame({
    'A': [-1, -1, -1, -1, 1, 1, 1, 1],
    'B': [-1, -1, 1, 1, -1, -1, 1, 1],
    'C': [-1, 1, -1, 1, -1, 1, -1, 1],
    'y': [22, 31, 25, 43, 33, 41, 37, 49]
})

# 주효과 + 2차 상호작용 모형 적합
model = ols('y ~ A + B + C + A:B + A:C + B:C', data=data).fit()

# ANOVA 테이블 출력
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

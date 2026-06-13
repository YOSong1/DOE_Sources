# code_11_03_02.py
# -*- coding: utf-8 -*-
"""
페이지: 11.3 예제로 이해: 초콜릿 코팅 품질의 완전 요인 실험
설명: 전체 모델(모든 상호작용) 과 간단한 모델(주효과 + 1개 2차 상호작용)
      을 적합하여 비교한다.
"""

import statsmodels.formula.api as smf
# 데이터프레임 df_experiment 는 original_01.py 로부터 생성된 것을 사용

# 전체 모델 (주효과 + 모든 상호작용)
formula_full = "Coating_Quality ~ Coating_Temperature * Mixing_Speed * Cooling_Time"
model_full = smf.ols(formula_full, data=df_experiment).fit()
print(model_full.summary())

# 간단한 모델 (주효과 + 특정 2차 상호작용)
formula_simple = (
    "Coating_Quality ~ Coating_Temperature + Mixing_Speed + Cooling_Time "
    "+ Coating_Temperature:Cooling_Time"
)
model_simple = smf.ols(formula_simple, data=df_experiment).fit()
print(model_simple.summary())

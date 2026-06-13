# code_11_03_04.py
# -*- coding: utf-8 -*-
"""
페이지: 11.3 예제로 이해: 초콜릿 코팅 품질의 완전 요인 실험
설명: 간단한 모델에 대한 ANOVA 테이블 (Type I SS) 출력.
"""

from statsmodels.stats.anova import anova_lm

# ANOVA 테이블 (Type I 제곱합)
anova_table = anova_lm(model_simple)
print("=" * 65)
print("ANOVA 테이블 (간단한 모델: 주효과 + 온도×냉각 시간 상호작용)")
print("=" * 65)
print(anova_table.to_string())

# code_12_05_01.py
# -*- coding: utf-8 -*-
"""
페이지: 12.5 연습 문제 — 플라스틱 사출 성형 공정 스크리닝
설명: 6요인 2수준 → 2^(6-2) IV (16 runs, Generator E=ABC, F=BCD) 의
      가상 인장 강도 데이터 생성.
"""

import numpy as np
import pandas as pd
from pyDOE3 import fracfact

# Resolution IV 설계: 2^(6-2) = 16회
# 생성 함수 예시: E = ABC, F = BCD
design = fracfact('a b c d abc bcd')
np.random.seed(7)

# 가상 인장 강도 데이터 (MPa) — A와 C의 주효과가 크도록 설정
tensile = (
    45
    + 5 * design[:, 0]   # A (용융 온도)
    + 1 * design[:, 1]   # B (사출 압력)
    + 4 * design[:, 2]   # C (냉각 시간)
    + 0.5 * design[:, 3] # D (게이트 크기)
    + 1.5 * design[:, 4] # E (사출 속도)
    - 2 * design[:, 5]   # F (수분 함량)
    + np.random.normal(0, 0.8, 16)
)

df_plastic = pd.DataFrame(design, columns=['A', 'B', 'C', 'D', 'E', 'F'])
df_plastic['Tensile_Strength'] = tensile
print(df_plastic)

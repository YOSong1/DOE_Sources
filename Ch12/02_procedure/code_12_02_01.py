# code_12_02_01.py
# -*- coding: utf-8 -*-
"""
페이지: 12.2 부분 요인 실험의 절차
설명: 2^(4-1) 설계 (Generator: D = ABC) 의 설계 행렬 구성 예시.
"""

import numpy as np
import pandas as pd
from itertools import product

# 기본 요인 A, B, C (2^3 완전 요인)
levels = [-1, 1]
base = list(product(levels, repeat=3))
df = pd.DataFrame(base, columns=['A', 'B', 'C'])

# Generator: D = ABC (4번째 요인을 ABC 상호작용으로 정의)
df['D'] = df['A'] * df['B'] * df['C']

print("2^(4-1) 설계 행렬 (Generator: D = ABC)")
print(df)
print(f"\n정의 관계: I = ABCD")
print(f"별칭 예: A ↔ BCD, B ↔ ACD, AB ↔ CD")

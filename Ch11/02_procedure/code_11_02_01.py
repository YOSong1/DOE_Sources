# code_11_02_01.py
# -*- coding: utf-8 -*-
"""
페이지: 11.2 완전 요인 실험의 절차
설명: 3요인 2수준 (2^3) 완전 요인 설계 행렬 생성 예시.
      itertools.product를 이용해 -1/+1 코딩으로 모든 처리 조합을 생성한다.
"""

import numpy as np
import pandas as pd
from itertools import product

# 3개 요인, 각 2수준 (-1, +1)
factors = ['A', 'B', 'C']
levels = [-1, 1]

# 완전 요인 실험 설계 행렬 생성
combinations = list(product(levels, repeat=len(factors)))
design_matrix = pd.DataFrame(combinations, columns=factors)
print(design_matrix)

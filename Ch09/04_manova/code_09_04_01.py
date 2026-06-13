# code_09_04_01.py
# -*- coding: utf-8 -*-
"""
페이지: 9.4 MANOVA — 교육 수준이 수학/읽기 점수에 미치는 영향.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
from statsmodels.multivariate.manova import MANOVA

np.random.seed(42)
data = {
    'education': ['HS'] * 15 + ['BS'] * 15 + ['MS'] * 15,
    'math':    list(np.random.normal(70, 5, 15)) +
               list(np.random.normal(78, 5, 15)) +
               list(np.random.normal(86, 5, 15)),
    'reading': list(np.random.normal(74, 4, 15)) +
               list(np.random.normal(82, 4, 15)) +
               list(np.random.normal(90, 4, 15))
}
df = pd.DataFrame(data)

maov = MANOVA.from_formula('math + reading ~ education', data=df)
result = maov.mv_test()
print(result)

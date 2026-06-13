# code_09_04_02.py
# -*- coding: utf-8 -*-
"""
페이지: 9.4 MANOVA — Box's M 공분산 동질성 검정.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
import pingouin as pg

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

box_m = pg.box_m(df, dvs=['math', 'reading'], group='education')
print("Box's M 검정 결과:")
print(box_m)

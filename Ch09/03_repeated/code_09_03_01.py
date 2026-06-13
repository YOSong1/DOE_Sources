# code_09_03_01.py
# -*- coding: utf-8 -*-
"""
페이지: 9.3 반복 측정 ANOVA — 10명의 참가자가 3시점 기억력 테스트.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import pandas as pd
import pingouin as pg

data = {
    'subject': [f'S{i+1}' for i in range(10) for _ in range(3)],
    'time':    ['t1', 't2', 't3'] * 10,
    'score':   [55, 60, 63, 50, 52, 55, 65, 66, 70, 58, 60, 64,
                62, 65, 67, 59, 61, 60, 70, 72, 75, 68, 70, 71,
                57, 59, 60, 52, 55, 58]
}
df = pd.DataFrame(data)

spher = pg.sphericity(df, dv='score', within='time', subject='subject')
print("Mauchly 구형성 검정:")
print(spher)

aov = pg.rm_anova(dv='score', within='time', subject='subject',
                  data=df, detailed=True)
print("\n반복 측정 ANOVA 결과:")
print(aov)

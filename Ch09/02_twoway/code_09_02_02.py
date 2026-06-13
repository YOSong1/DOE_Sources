# code_09_02_02.py
# -*- coding: utf-8 -*-
"""
페이지: 9.2 이원배치 ANOVA — 상호작용 도표.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

data = {
    'fertilizer': ['A','A','A','A','B','B','B','B','C','C','C','C'] * 2,
    'watering':   ['low']*12 + ['high']*12,
    'height': [20, 22, 21, 23, 25, 27, 26, 28, 24, 23, 25, 24,
               30, 32, 31, 33, 34, 35, 36, 33, 32, 31, 33, 34]
}
df = pd.DataFrame(data)

cell_means = df.groupby(['fertilizer', 'watering'])['height'].mean().unstack()

cell_means.plot(marker='o', figsize=(7, 4))
plt.title('비료 종류 × 관수 수준 상호작용 도표')
plt.xlabel('비료 종류')
plt.ylabel('평균 식물 높이 (cm)')
plt.legend(title='관수 수준')
plt.tight_layout()
plt.show()

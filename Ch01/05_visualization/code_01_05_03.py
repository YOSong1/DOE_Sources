# code_01_05_03.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.5 시각화 - 히스토그램 + KDE
# =============================================================================
# 페이지: 324260 - 1.5 시각화
# =============================================================================

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)
scores = np.random.normal(loc=75, scale=10, size=100)

fig, ax = plt.subplots(figsize=(8, 5))

# 히스토그램 (밀도 기준으로 정규화)
ax.hist(scores, bins=15, density=True, color='steelblue',
        edgecolor='white', alpha=0.6, label='히스토그램')

# KDE 곡선
kde = gaussian_kde(scores)
x_range = np.linspace(scores.min(), scores.max(), 200)
ax.plot(x_range, kde(x_range), color='tomato', linewidth=2, label='KDE')

ax.set_title('점수 분포 (히스토그램 + KDE)')
ax.set_xlabel('점수')
ax.set_ylabel('밀도')
ax.legend()
plt.show()

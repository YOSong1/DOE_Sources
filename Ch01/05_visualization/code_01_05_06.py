# code_01_05_06.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.5 시각화 - 박스 플롯 (학과별)
# =============================================================================
# 페이지: 324260 - 1.5 시각화
# =============================================================================

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)
math_scores = np.random.normal(80, 10, 30)
cs_scores = np.random.normal(75, 12, 30)
eco_scores = np.random.normal(85, 8, 30)

data = [math_scores, cs_scores, eco_scores]
labels = ['수학과', '컴퓨터공학과', '경제학과']

plt.figure(figsize=(8, 5))
plt.boxplot(data, tick_labels=labels, patch_artist=True,
            boxprops=dict(facecolor='steelblue', alpha=0.6))
plt.title('학과별 점수 분포')
plt.ylabel('점수')
plt.grid(axis='y', alpha=0.3)
plt.show()

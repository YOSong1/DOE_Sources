# code_01_05_07.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.5 시각화 - subplots로 여러 그래프 배치
# =============================================================================
# 페이지: 324260 - 1.5 시각화
# =============================================================================

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)
scores = np.random.normal(75, 10, 100)

# 2행 2열 격자 배치
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('다양한 그래프 유형 비교', fontsize=14)

# (0,0) 히스토그램
axes[0, 0].hist(scores, bins=15, color='steelblue',
                edgecolor='white', alpha=0.8)
axes[0, 0].set_title('히스토그램')

# (0,1) 박스 플롯
axes[0, 1].boxplot(scores, patch_artist=True,
                   boxprops=dict(facecolor='steelblue', alpha=0.6))
axes[0, 1].set_title('박스 플롯')

# (1,0) 산점도
hours = np.random.uniform(1, 10, 50)
exam = 50 + 4 * hours + np.random.normal(0, 5, 50)
axes[1, 0].scatter(hours, exam, color='tomato', alpha=0.7)
axes[1, 0].set_title('산점도')

# (1,1) 막대 그래프
departments = ['수학', 'CS', '경제', '물리']
avg = [82, 79, 85, 77]
axes[1, 1].bar(departments, avg, color='seagreen', edgecolor='white')
axes[1, 1].set_title('막대 그래프')

plt.tight_layout()
plt.show()

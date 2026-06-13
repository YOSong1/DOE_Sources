# code_01_05_08.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.5 시각화 - Seaborn 통합 예제
# =============================================================================
# 페이지: 324260 - 1.5 시각화
# 설명: histplot, boxplot, scatterplot 통합.
# =============================================================================

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)
df = pd.DataFrame({
    'score': np.concatenate([
        np.random.normal(80, 10, 30),
        np.random.normal(75, 12, 30),
        np.random.normal(85, 8, 30)
    ]),
    'major': ['수학과'] * 30 + ['CS학과'] * 30 + ['경제학과'] * 30
})

fig, axes = plt.subplots(1, 3, figsize=(14, 5))

# 히스토그램 + KDE
sns.histplot(data=df, x='score', kde=True, ax=axes[0], color='steelblue')
axes[0].set_title('히스토그램 (KDE 포함)')

# 박스 플롯
sns.boxplot(data=df, x='major', y='score', ax=axes[1], palette='pastel')
axes[1].set_title('박스 플롯')

# 산점도
hours = np.random.uniform(1, 10, 90)
sns.scatterplot(x=hours, y=df['score'], ax=axes[2], alpha=0.6)
axes[2].set_title('산점도')

plt.tight_layout()
plt.show()

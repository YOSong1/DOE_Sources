# code_01_05_02.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.5 시각화 - 히스토그램
# =============================================================================
# 페이지: 324260 - 1.5 시각화
# 설명: 평균 75, 표준편차 10 정규분포 100명 점수 분포.
# =============================================================================

import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 생성 (평균 75점, 표준편차 10점인 100명의 점수)
np.random.seed(42)
scores = np.random.normal(loc=75, scale=10, size=100)

plt.figure(figsize=(8, 5))

# bins: 막대 개수
plt.hist(scores, bins=15, color='steelblue', edgecolor='white', alpha=0.8)
plt.title('시험 점수 분포')
plt.xlabel('점수')
plt.ylabel('빈도')
plt.grid(axis='y', alpha=0.3)
plt.show()

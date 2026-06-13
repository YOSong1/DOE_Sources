# code_01_05_04.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.5 시각화 - 막대 그래프 (학과별 평균)
# =============================================================================
# 페이지: 324260 - 1.5 시각화
# =============================================================================

import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

departments = ['수학과', '컴퓨터공학과', '경제학과', '물리학과']
avg_scores = [82.3, 79.1, 85.6, 77.4]

plt.figure(figsize=(8, 5))
plt.bar(departments, avg_scores,
        color=['steelblue', 'tomato', 'seagreen', 'orange'],
        edgecolor='white')
plt.title('학과별 평균 점수')
plt.xlabel('학과')
plt.ylabel('평균 점수')
plt.ylim(70, 90)
plt.grid(axis='y', alpha=0.3)
plt.show()

# 수평 막대 그래프
# plt.barh(departments, avg_scores, color='steelblue')

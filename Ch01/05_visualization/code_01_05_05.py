# code_01_05_05.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.5 시각화 - 산점도 + 추세선
# =============================================================================
# 페이지: 324260 - 1.5 시각화
# 설명: 공부 시간 vs 시험 점수, polyfit으로 1차 추세선.
# =============================================================================

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(7)
# 공부 시간 (1~10시간)과 점수 (양의 상관관계 가정)
study_hours = np.random.uniform(1, 10, 20)
scores = 50 + 4 * study_hours + np.random.normal(0, 5, 20)

plt.figure(figsize=(8, 5))
plt.scatter(study_hours, scores, color='steelblue',
            s=80, alpha=0.8, label='학생 데이터')

# 추세선 (1차 다항식 피팅)
z = np.polyfit(study_hours, scores, 1)
p = np.poly1d(z)
x_line = np.linspace(1, 10, 100)
plt.plot(x_line, p(x_line), color='tomato',
         linewidth=2, linestyle='--', label='추세선')

plt.title('공부 시간 vs 시험 점수 (20명)')
plt.xlabel('공부 시간 (시간)')
plt.ylabel('시험 점수 (점)')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

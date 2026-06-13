# code_05_05_01.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.5 기하 분포 - 상담원 연결 예시
# 출처: WikiDocs book 1914, page 324341

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import geom

# 상담원 연결 성공 확률
p = 0.3

# 1. 특정 시도에서 처음 성공할 확률 (3번째 시도)
prob_3rd = geom.pmf(3, p)
print(f"3번째 시도에서 처음 연결될 확률: {prob_3rd:.4f}")

# 2. 5번 이하 시도로 연결될 누적 확률
prob_within_5 = geom.cdf(5, p)
print(f"5번 이하 시도로 연결될 확률: {prob_within_5:.4f}")

# 3. 90% 확률로 연결되기 위한 최소 시도 횟수
min_attempts = geom.ppf(0.9, p)
print(f"90% 확률로 연결되기 위한 최소 시도 횟수: {min_attempts:.0f}번")

# 4. 기댓값과 분산
print(f"기댓값(평균 시도 횟수): {geom.mean(p):.2f}")
print(f"분산: {geom.var(p):.2f}")

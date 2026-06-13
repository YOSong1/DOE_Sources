# code_05_07_01.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.7 다항 분포 - 공정한 주사위 100회 시뮬레이션
# 출처: WikiDocs book 1914, page 324376

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multinomial

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 파라미터 설정
n = 100
k = 6
p = [1/6] * k

# 2. PMF 계산 — 각 면이 정확히 n/k번 나올 확률
x_expected = [n // k] * k
x_expected[-1] = n - sum(x_expected[:-1])
prob = multinomial.pmf(x_expected, n, p)
print(f"기대 빈도와 정확히 일치할 확률: {prob:.6f}")

# 3. 시뮬레이션: 주사위 100회 던지기 1,000번 반복
np.random.seed(42)
samples = multinomial.rvs(n, p, size=1000)
observed_mean = samples.mean(axis=0)

# 4. 관측 빈도 vs 기대 빈도 시각화
faces = [f'{i}면' for i in range(1, k+1)]
expected = [n * pi for pi in p]

x_pos = np.arange(k)
width = 0.35

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x_pos - width/2, observed_mean, width, label='시뮬레이션 평균', color='steelblue', alpha=0.8)
ax.bar(x_pos + width/2, expected, width, label='기대 빈도', color='orange', alpha=0.8)
ax.set_xlabel('주사위 면')
ax.set_ylabel('빈도')
ax.set_title('주사위 100회 던지기: 관측 vs 기대 빈도')
ax.set_xticks(x_pos)
ax.set_xticklabels(faces)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('multinom_pmf.png', dpi=120)
print("saved multinom_pmf.png")

# 5. 기댓값, 분산
mean = [n * pi for pi in p]
variance = [n * pi * (1 - pi) for pi in p]
print(f"기댓값: {[round(m, 2) for m in mean]}")
print(f"분산: {[round(v, 2) for v in variance]}")

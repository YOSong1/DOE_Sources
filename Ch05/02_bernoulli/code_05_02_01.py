# code_05_02_01.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.2 베르누이 분포 - 동전 던지기 시뮬레이션
# 출처: WikiDocs book 1914, page 324470
# 설명: scipy.stats.bernoulli로 PMF, 기댓값, 분산, 난수 생성을 수행

import numpy as np
from scipy.stats import bernoulli

# 성공 확률 설정 (앞면이 나올 확률)
p = 0.6

# PMF 계산
print(f"P(X=1) = {bernoulli.pmf(1, p):.4f}")  # 성공 확률
print(f"P(X=0) = {bernoulli.pmf(0, p):.4f}")  # 실패 확률

# 기댓값과 분산
print(f"기댓값 E[X] = {bernoulli.mean(p):.4f}")
print(f"분산 Var(X) = {bernoulli.var(p):.4f}")

# 동전 10번 던지기 시뮬레이션
np.random.seed(42)
results = bernoulli.rvs(p, size=10)
print(f"\n시뮬레이션 결과 (1=앞면, 0=뒷면): {results}")
print(f"앞면 횟수: {results.sum()}번 / 10번")

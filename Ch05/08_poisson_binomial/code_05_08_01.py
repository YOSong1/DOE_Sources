# code_05_08_01.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.8 포아송-이항 분포 - 동적 계획법 구현
# 출처: WikiDocs book 1914, page 324316

import numpy as np
import matplotlib.pyplot as plt

def poisson_binomial_pmf_dp(probs):
    """
    동적 계획법으로 포아송-이항 분포 PMF를 계산합니다.
    probs: 각 시행의 성공 확률 리스트
    반환: PMF 배열 (인덱스 k = 성공 횟수 k의 확률)
    """
    n = len(probs)
    dp = np.zeros(n + 1)
    dp[0] = 1.0

    for i, p in enumerate(probs):
        for k in range(i + 1, 0, -1):
            dp[k] = dp[k] * (1 - p) + dp[k - 1] * p
        dp[0] *= (1 - p)

    return dp

# 스포츠 팀 시즌 승리 예측: 각 경기 승률이 다름
probs = [0.6, 0.4, 0.7, 0.3, 0.8, 0.5, 0.6, 0.4, 0.7, 0.5]
n = len(probs)
pmf = poisson_binomial_pmf_dp(probs)

mean = sum(probs)
variance = sum(p * (1 - p) for p in probs)
print(f"기댓값 E[X] = {mean:.4f}")
print(f"분산 Var(X) = {variance:.4f}")
print()
for k in range(n + 1):
    print(f"P(X = {k:2d}) = {pmf[k]:.4f}")

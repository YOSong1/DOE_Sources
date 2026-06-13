# code_05_04_01.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.4 포아송 분포 - 콜센터 전화 예측
# 출처: WikiDocs book 1914, page 324290

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

# 매개변수: 10분당 평균 3건
lam = 3
k = np.arange(0, 11)

# 확률 계산 및 출력
probabilities = poisson.pmf(k, lam)
for i, prob in zip(k, probabilities):
    print(f"P(X={i:2d}) = {prob:.4f}")

# 기댓값과 분산 확인 (평균 = 분산 = λ)
print(f"\n기댓값 E[X] = {poisson.mean(lam):.1f}")
print(f"분  산 Var  = {poisson.var(lam):.1f}")

# 5건 초과 확률
print(f"\nP(X > 5) = {poisson.sf(5, lam):.4f}")

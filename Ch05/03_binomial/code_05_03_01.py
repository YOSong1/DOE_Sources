# code_05_03_01.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.3 이항 분포 - 공장 불량품 검사
# 출처: WikiDocs book 1914, page 324375

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# 매개변수 설정: 시행 횟수 n=20, 불량 확률 p=0.05
n, p = 20, 0.05

# 기댓값과 분산 출력
print(f"기댓값 E[X] = {binom.mean(n, p):.2f}")   # 1.00
print(f"분산 Var(X) = {binom.var(n, p):.4f}")      # 0.9500

# 불량품 0~5개일 확률
k_vals = np.arange(0, 6)
for k in k_vals:
    prob = binom.pmf(k, n, p)
    print(f"P(X={k}) = {prob:.4f}")

# 불량품이 3개 이하일 누적 확률
print(f"\nP(X ≤ 3) = {binom.cdf(3, n, p):.4f}")

# 불량품이 5개 이상일 확률
print(f"P(X ≥ 5) = {binom.sf(4, n, p):.4f}")

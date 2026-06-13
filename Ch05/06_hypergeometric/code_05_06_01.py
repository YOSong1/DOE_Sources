# code_05_06_01.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.6 초기하 분포 - 불량품 검사 + 로또
# 출처: WikiDocs book 1914, page 324473

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import hypergeom

# ── 예시 1: 불량품 검사 ──────────────────────────────────────────────
M = 20    # 총 제품 수
n = 5     # 불량품 수
N = 5     # 검사할 제품 수

k_vals = np.arange(0, N + 1)
pmf_vals = hypergeom.pmf(k_vals, M, n, N)

print("=== 불량품 검사 ===")
for k, prob in zip(k_vals, pmf_vals):
    print(f"  불량품 {k}개 포함될 확률: {prob:.4f}")
print(f"  기댓값: {hypergeom.mean(M, n, N):.4f}")
print(f"  분산:   {hypergeom.var(M, n, N):.4f}")

# ── 예시 2: 로또 (45개 중 6개 추출, 당첨 번호 6개) ──────────────────
M2 = 45
n2 = 6
N2 = 6

k_vals2 = np.arange(0, N2 + 1)
pmf_vals2 = hypergeom.pmf(k_vals2, M2, n2, N2)

print("\n=== 로또 당첨 확률 ===")
for k, prob in zip(k_vals2, pmf_vals2):
    if prob > 0:
        print(f"  {k}개 일치 확률: {prob:.8f}")

# code_02_02_01.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 2.2 확률의 기본 성질 - 공리적 성질 검증
# =============================================================================
# 책: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
# 페이지: 326984 - 2.2 확률의 기본 성질
# 설명: 주사위 100,000회 시뮬레이션으로 공리 2(정규화),
#       공사건, 여사건, 합사건의 확률을 검증.
# =============================================================================

import numpy as np

np.random.seed(42)
n = 100000  # 시행 횟수

# 주사위 시뮬레이션
rolls = np.random.randint(1, 7, size=n)

# 1. 공리 2: 표본공간 확률 = 1
p_all = np.mean(np.isin(rolls, [1, 2, 3, 4, 5, 6]))
print(f"공리 2 — P(Ω) = {p_all:.4f}  (이론값: 1.0000)")

# 2. 공사건 확률 = 0
p_impossible = np.mean(rolls == 7)
print(f"공사건  — P(7) = {p_impossible:.4f}  (이론값: 0.0000)")

# 3. 여사건: 짝수 사건 A, 여사건 A^c = 홀수
A = rolls % 2 == 0       # 짝수
Ac = rolls % 2 != 0      # 홀수 (여사건)
p_A = np.mean(A)
p_Ac = np.mean(Ac)
print(f"여사건  — P(A) = {p_A:.4f}, P(A^c) = {p_Ac:.4f}, "
      f"합 = {p_A + p_Ac:.4f}  (이론합: 1.0000)")

# 4. 합사건: A=짝수, B=3의 배수
B = rolls % 3 == 0       # 3의 배수: {3, 6}
AB = A & B               # 교집합: {6}
p_B = np.mean(B)
p_AB = np.mean(AB)
p_AuB_empirical = np.mean(A | B)
p_AuB_formula = p_A + p_B - p_AB
print(f"합사건  — 관측: {p_AuB_empirical:.4f}, 공식: {p_AuB_formula:.4f}  "
      f"(이론값: {4/6:.4f})")

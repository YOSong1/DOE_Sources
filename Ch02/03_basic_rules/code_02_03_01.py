# code_02_03_01.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 2.3 확률의 기본 법칙 - 카드 뽑기 시뮬레이션
# =============================================================================
# 책: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
# 페이지: 327108 - 2.3 확률의 기본 법칙
# 설명: 덧셈 법칙(스페이드∪에이스), 여사건 법칙(주사위 2번 적어도 한번 6)을
#       시뮬레이션으로 검증.
# =============================================================================

import numpy as np

np.random.seed(42)
n = 100000  # 시행 횟수

# 카드 덱 생성: (무늬, 숫자) 쌍
# 무늬: 0=스페이드, 1=다이아몬드, 2=하트, 3=클럽
# 숫자: 1(에이스)~13
suits = np.random.randint(0, 4, size=n)   # 무늬 (0~3)
ranks = np.random.randint(1, 14, size=n)  # 숫자 (1~13)

# 사건 A: 스페이드 (suit == 0)
# 사건 B: 에이스 (rank == 1)
A = suits == 0
B = ranks == 1
AB = A & B       # 교집합: 스페이드 에이스
AuB = A | B      # 합집합: 스페이드 또는 에이스

p_A = np.mean(A)
p_B = np.mean(B)
p_AB = np.mean(AB)
p_AuB_sim = np.mean(AuB)
p_AuB_formula = p_A + p_B - p_AB

print("=== 덧셈 법칙 검증 (카드 뽑기) ===")
print(f"P(스페이드)       = {p_A:.4f}  (이론: {13/52:.4f})")
print(f"P(에이스)         = {p_B:.4f}  (이론: {4/52:.4f})")
print(f"P(스페이드 에이스) = {p_AB:.4f}  (이론: {1/52:.4f})")
print(f"P(스페이드∪에이스) 시뮬레이션: {p_AuB_sim:.4f}")
print(f"P(스페이드∪에이스) 공식 적용: {p_AuB_formula:.4f}")
print(f"이론값:                       {16/52:.4f}")

print()

# 여사건 법칙: 주사위 2번 던져 적어도 한 번 6
print("=== 여사건 법칙 검증 (주사위 2번) ===")
d1 = np.random.randint(1, 7, size=n)
d2 = np.random.randint(1, 7, size=n)
at_least_one_six = np.mean((d1 == 6) | (d2 == 6))
theory = 1 - (5/6)**2
print(f"적어도 한 번 6 (시뮬레이션): {at_least_one_six:.4f}")
print(f"적어도 한 번 6 (이론값):     {theory:.4f}")

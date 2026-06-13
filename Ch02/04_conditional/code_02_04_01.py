# code_02_04_01.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 2.4 조건부 확률 - 베이즈 정리 (스팸 / 의학 진단)
# =============================================================================
# 책: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
# 페이지: 326986 - 2.4 조건부 확률
# 설명: 스팸 메일 예제와 의학 진단 예제를 베이즈 정리로 수치 계산하고
#       시뮬레이션으로 검증.
# =============================================================================

import numpy as np

np.random.seed(42)

# ────────────────────────────────────────
# 1. 베이즈 정리 수치 계산 — 스팸 메일 예제
# ────────────────────────────────────────
p_spam = 0.3              # P(스팸)
p_normal = 0.7            # P(일반)
p_discount_spam = 0.9     # P(할인 | 스팸)
p_discount_normal = 0.2   # P(할인 | 일반)

# 전확률의 법칙
p_discount = p_discount_spam * p_spam + p_discount_normal * p_normal

# 베이즈 정리
p_spam_given_discount = (p_discount_spam * p_spam) / p_discount

print("=== 스팸 메일 예제 ===")
print(f"P(할인)            = {p_discount:.4f}")
print(f"P(스팸 | 할인)     = {p_spam_given_discount:.4f}")

print()

# ────────────────────────────────────────
# 2. 베이즈 정리 수치 계산 — 의학 진단 예제
# ────────────────────────────────────────
p_disease = 0.01                # P(환자)
p_no_disease = 0.99             # P(비환자)
p_pos_given_disease = 0.99      # 민감도
p_pos_given_no_disease = 0.05   # 1 - 특이도

# 전확률의 법칙
p_positive = (p_pos_given_disease * p_disease
              + p_pos_given_no_disease * p_no_disease)

# 베이즈 정리
p_disease_given_pos = (p_pos_given_disease * p_disease) / p_positive

print("=== 의학 진단 예제 ===")
print(f"P(양성)              = {p_positive:.4f}")
print(f"P(환자 | 양성)       = {p_disease_given_pos:.4f}")

print()

# ────────────────────────────────────────
# 3. 시뮬레이션으로 검증
# ────────────────────────────────────────
n = 100000
is_spam = np.random.choice([True, False], size=n, p=[0.3, 0.7])
has_discount = np.where(
    is_spam,
    np.random.rand(n) < 0.9,
    np.random.rand(n) < 0.2
)

discount_mask = has_discount
spam_given_discount_sim = np.mean(is_spam[discount_mask])
p_discount_sim = np.mean(discount_mask)

print("=== 시뮬레이션 검증 (스팸 예제) ===")
print(f"P(할인) 시뮬레이션:        {p_discount_sim:.4f}  "
      f"(이론: {p_discount:.4f})")
print(f"P(스팸|할인) 시뮬레이션:   {spam_given_discount_sim:.4f}  "
      f"(이론: {p_spam_given_discount:.4f})")

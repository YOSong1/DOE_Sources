import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 2.3 확률의 기본 법칙 - Excel 활용 버전: 카드/주사위 로그로 법칙 검증
# =============================================================================
# 책: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
# 페이지: 327108 - 2.3 확률의 기본 법칙
#
# sample_data.xlsx의 두 시트를 사용:
#   - cards: 2000회 카드 한 장 뽑기 (suit, rank, is_spade, is_ace)
#   - two_dice: 2000회 주사위 2개 던지기 (dice1, dice2, any_six)
#
# 다음 법칙을 단계별 검증:
#   1) 덧셈 법칙 (일반): P(A∪B) = P(A)+P(B)-P(A∩B)
#   2) 곱셈 법칙 (독립): P(A∩B) ?= P(A)*P(B) — 독립 여부 확인
#   3) 여사건 법칙:      P(적어도 한 번 6) = 1 - (5/6)^2
# =============================================================================

import os
import sys
import io
import pandas as pd

# Windows 콘솔 한글/특수문자 출력을 위해 UTF-8 강제
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(BASE, "sample_data.xlsx")

# -----------------------------------------------------------------------------
# 1) Excel 읽기
# -----------------------------------------------------------------------------
cards = pd.read_excel(XLSX, sheet_name="cards")
dice = pd.read_excel(XLSX, sheet_name="two_dice")
n_c = len(cards)
n_d = len(dice)

print("=== cards 시트 (앞 5개) ===")
print(cards.head())
print(f"\n총 시행: {n_c}회")

print("\n=== two_dice 시트 (앞 5개) ===")
print(dice.head())
print(f"총 시행: {n_d}회")

# -----------------------------------------------------------------------------
# 2) 덧셈 법칙 (일반): 스페이드(A) ∪ 에이스(B)
# -----------------------------------------------------------------------------
print("\n=== 2.3.1 덧셈 법칙 — P(A∪B) = P(A)+P(B)-P(A∩B) ===")

p_A = cards["is_spade"].mean()
p_B = cards["is_ace"].mean()

inter = (cards["is_spade"] & cards["is_ace"]).astype(int)
union = (cards["is_spade"] | cards["is_ace"]).astype(int)

p_AB = inter.mean()
p_union_emp = union.mean()
p_union_formula = p_A + p_B - p_AB

print("[수식 분해]")
print(f"  P(A=스페이드) = {cards['is_spade'].sum()}/{n_c} = {p_A:.4f}  "
      f"(이론 13/52={13/52:.4f})")
print(f"  P(B=에이스)   = {cards['is_ace'].sum()}/{n_c} = {p_B:.4f}  "
      f"(이론 4/52={4/52:.4f})")
print(f"  P(A∩B)        = {inter.sum()}/{n_c} = {p_AB:.4f}  "
      f"(이론 1/52={1/52:.4f})")
print(f"\n  데이터의 P(A∪B)             = {p_union_emp:.4f}")
print(f"  공식 P(A)+P(B)-P(A∩B)       = {p_A:.4f}+{p_B:.4f}-{p_AB:.4f} "
      f"= {p_union_formula:.4f}")
print(f"  이론값 16/52                 = {16/52:.4f}")
print(f"  → 두 결과 일치? "
      f"{abs(p_union_emp - p_union_formula) < 1e-6}")

# -----------------------------------------------------------------------------
# 3) 곱셈 법칙 (독립): 카드의 무늬와 숫자는 독립일까?
# -----------------------------------------------------------------------------
print("\n=== 2.3.2 곱셈 법칙 — 독립성 확인 ===")
# 두 사건이 독립이면 P(A∩B) = P(A) * P(B)
lhs = p_AB
rhs = p_A * p_B
print(f"  P(A∩B)        = {lhs:.4f}")
print(f"  P(A) × P(B)   = {p_A:.4f} × {p_B:.4f} = {rhs:.4f}")
print(f"  두 값 차이     = {abs(lhs - rhs):.4f}")
print("  → 거의 같으므로 '카드 무늬 ⫫ 카드 숫자'는 독립으로 볼 수 있습니다.")

# -----------------------------------------------------------------------------
# 4) 여사건 법칙: 주사위 2번 던져 적어도 한 번 6
# -----------------------------------------------------------------------------
print("\n=== 2.3.3 여사건 법칙 — P(적어도 한 번 6) = 1 - (5/6)^2 ===")

# 명시적으로 단계 표시
no_six = ((dice["dice1"] != 6) & (dice["dice2"] != 6)).astype(int)
p_no_six_emp = no_six.mean()
p_at_least_one_six_emp = dice["any_six"].mean()

p_no_six_theory = (5/6) ** 2
p_at_least_theory = 1 - p_no_six_theory

print(f"  P(한 번도 6 아님) 데이터    = {p_no_six_emp:.4f}")
print(f"  P(한 번도 6 아님) 이론(5/6)² = {p_no_six_theory:.4f}")
print(f"\n  P(적어도 한 번 6) 데이터    = {p_at_least_one_six_emp:.4f}")
print(f"  P(적어도 한 번 6) 공식      = 1 - {p_no_six_emp:.4f} "
      f"= {1 - p_no_six_emp:.4f}")
print(f"  이론값                       = 1 - (5/6)² = {p_at_least_theory:.4f}")

print("\n[해석] '적어도 한 번'을 직접 세기는 어렵지만, 여사건('한 번도 아님')은\n"
      "        독립 사건의 곱셈으로 간단히 구할 수 있습니다. 여사건 법칙은\n"
      "        '복잡한 사건 ↔ 단순한 여사건'으로 문제를 뒤집는 강력한 기법입니다.")

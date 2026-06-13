import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 2.4 조건부 확률 - Excel 활용 버전: 의료 진단 / 스팸 메일 데이터
# =============================================================================
# 책: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
# 페이지: 326986 - 2.4 조건부 확률
#
# sample_data.xlsx의 두 시트:
#   - medical_test: 5000명 의료 진단 (has_disease, test_positive)
#   - spam_mail:    5000개 메일 (is_spam, contains_discount)
#
# 다음을 데이터로 직접 계산:
#   1) 조건부 확률 정의:    P(A|B) = P(A∩B)/P(B)
#   2) 전확률의 법칙:        P(B) = ΣP(B|A_i)P(A_i)
#   3) 베이즈 정리:          P(A|B) = P(B|A)P(A)/P(B)
#   4) 데이터 vs 이론값 비교
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
# 1) Excel 데이터 읽기
# -----------------------------------------------------------------------------
med = pd.read_excel(XLSX, sheet_name="medical_test")
spam = pd.read_excel(XLSX, sheet_name="spam_mail")

print("=== medical_test 시트 (앞 5개) ===")
print(med.head())
print(f"\n총 인원: {len(med)}명")
print(f"실제 환자 수: {med['has_disease'].sum()}명 ({med['has_disease'].mean()*100:.2f}%)")
print(f"양성 판정 수: {med['test_positive'].sum()}명")

print("\n=== spam_mail 시트 (앞 5개) ===")
print(spam.head())
print(f"\n총 메일: {len(spam)}개, 스팸: {spam['is_spam'].sum()}개")

# =============================================================================
# A. 의료 진단 — 베이즈 정리 데이터 검증
# =============================================================================
print("\n" + "=" * 70)
print("A. 의료 진단 데이터로 베이즈 정리 검증")
print("=" * 70)

# (1) 주변/조건부 확률 계산 (데이터 기반)
p_disease = med["has_disease"].mean()
p_positive = med["test_positive"].mean()
p_d_and_pos = ((med["has_disease"] == 1) & (med["test_positive"] == 1)).mean()
p_nd_and_pos = ((med["has_disease"] == 0) & (med["test_positive"] == 1)).mean()

print("\n[1단계] 데이터에서 직접 비율 계산")
print(f"  P(환자)             = {p_disease:.4f}  (목표 0.0100)")
print(f"  P(양성)             = {p_positive:.4f}  (이론 0.0594)")
print(f"  P(환자 ∩ 양성)      = {p_d_and_pos:.4f}  (이론 0.0099)")
print(f"  P(비환자 ∩ 양성)    = {p_nd_and_pos:.4f}  (이론 0.0495)")

# (2) 조건부 확률을 정의에 따라 계산
print("\n[2단계] 조건부 확률 P(양성|환자), P(양성|비환자) — 민감도/거짓양성")
p_pos_given_disease = p_d_and_pos / p_disease
p_pos_given_no_disease = p_nd_and_pos / (1 - p_disease)
print(f"  P(양성|환자)   = P(환자∩양성)/P(환자)   "
      f"= {p_d_and_pos:.4f}/{p_disease:.4f} = {p_pos_given_disease:.4f}  "
      f"(이론 0.99)")
print(f"  P(양성|비환자) = P(비환자∩양성)/P(비환자) "
      f"= {p_nd_and_pos:.4f}/{1-p_disease:.4f} = {p_pos_given_no_disease:.4f}  "
      f"(이론 0.05)")

# (3) 전확률의 법칙으로 P(양성) 다시 계산하여 일치 확인
print("\n[3단계] 전확률의 법칙 P(양성) = P(양성|환자)P(환자) + P(양성|비환자)P(비환자)")
p_pos_total = (p_pos_given_disease * p_disease
               + p_pos_given_no_disease * (1 - p_disease))
print(f"  = {p_pos_given_disease:.4f}*{p_disease:.4f} + "
      f"{p_pos_given_no_disease:.4f}*{1-p_disease:.4f}")
print(f"  = {p_pos_total:.4f}")
print(f"  (데이터의 P(양성): {p_positive:.4f} ← 일치 확인)")

# (4) 베이즈 정리로 P(환자|양성) 계산
print("\n[4단계] 베이즈 정리 P(환자|양성) = P(양성|환자)P(환자) / P(양성)")
p_disease_given_pos_bayes = (p_pos_given_disease * p_disease) / p_pos_total

# 데이터에서 직접 확인
p_disease_given_pos_data = (
    med[med["test_positive"] == 1]["has_disease"].mean()
)

print(f"  베이즈 공식 결과:    "
      f"{p_pos_given_disease:.4f}*{p_disease:.4f}/{p_pos_total:.4f} "
      f"= {p_disease_given_pos_bayes:.4f}")
print(f"  데이터 직접 계산:    "
      f"(양성 중 환자) / (양성 전체) = "
      f"{p_disease_given_pos_data:.4f}")
print(f"  이론값(약):          0.1667")

print("\n[해석] 검사 민감도가 99%로 매우 높아도, 유병률이 1%로 낮으면\n"
      "        양성 판정자 중 실제 환자 비율은 ~17%에 불과합니다.\n"
      "        이것이 '베이즈 정리가 직관에 반하는 결과를 만드는' 대표 사례입니다.")

# =============================================================================
# B. 스팸 메일 — 같은 절차로 베이즈 정리 검증
# =============================================================================
print("\n" + "=" * 70)
print("B. 스팸 메일 데이터로 베이즈 정리 검증")
print("=" * 70)

p_spam = spam["is_spam"].mean()
p_disc = spam["contains_discount"].mean()
p_spam_and_disc = ((spam["is_spam"] == 1)
                   & (spam["contains_discount"] == 1)).mean()

print(f"\n  P(스팸)         = {p_spam:.4f}  (목표 0.30)")
print(f"  P(할인)         = {p_disc:.4f}  (이론 0.41)")
print(f"  P(스팸∩할인)    = {p_spam_and_disc:.4f}  (이론 0.27)")

# 조건부 확률
p_disc_given_spam = p_spam_and_disc / p_spam
p_disc_given_normal = (
    ((spam["is_spam"] == 0) & (spam["contains_discount"] == 1)).sum()
    / (spam["is_spam"] == 0).sum()
)

print(f"\n  P(할인|스팸)    = {p_disc_given_spam:.4f}  (이론 0.90)")
print(f"  P(할인|일반)    = {p_disc_given_normal:.4f}  (이론 0.20)")

# 베이즈 정리
p_spam_given_disc = (p_disc_given_spam * p_spam) / p_disc
print(f"\n  P(스팸|할인) 베이즈 공식 = "
      f"{p_disc_given_spam:.4f}*{p_spam:.4f}/{p_disc:.4f} "
      f"= {p_spam_given_disc:.4f}")
print(f"  데이터에서 직접          = "
      f"{spam[spam['contains_discount']==1]['is_spam'].mean():.4f}  "
      f"(이론 ~0.66)")

print("\n[해석] '할인'이라는 단어가 들어 있으면 그 메일이 스팸일 확률은\n"
      "        66% 정도로 높아집니다. 사전확률 30%보다 두 배 이상 높아진 것이\n"
      "        '새로운 증거로 믿음을 갱신'한 결과입니다.")

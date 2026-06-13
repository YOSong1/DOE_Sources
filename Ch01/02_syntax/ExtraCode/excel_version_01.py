import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.2 Python 기본 문법 - Excel 활용 버전: 학생 점수 분석
# =============================================================================
# 책: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
# 페이지: 324206 - 1.2 Python 기본 문법
#
# sample_data.xlsx의 students 시트를 읽어 다음을 수행:
#   1) 자료형 확인 (1.2.1)
#   2) 리스트/딕셔너리 형태로 변환 (1.2.2)
#   3) for / if / 함수로 평균/분산 직접 계산 (1.2.3~1.2.5)
#   4) NumPy 결과와 비교
# =============================================================================

import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(BASE, "sample_data.xlsx")

# -----------------------------------------------------------------------------
# 1) Excel 데이터 읽기 및 구조 출력
# -----------------------------------------------------------------------------
df = pd.read_excel(XLSX, sheet_name="students")
print("=== Excel에서 읽은 데이터 (sample_data.xlsx / students) ===")
print(df)
print(f"\n행 수: {df.shape[0]}, 열 수: {df.shape[1]}")
print("\n각 열의 자료형:")
print(df.dtypes)

# -----------------------------------------------------------------------------
# 2) 리스트와 딕셔너리로 변환 (1.2.1 자료형, 1.2.2 자료구조)
# -----------------------------------------------------------------------------
scores_list = df["score"].tolist()        # 점수만 리스트로
first_student = df.iloc[0].to_dict()      # 첫 학생을 딕셔너리로

print("\n=== 리스트/딕셔너리 변환 ===")
print(f"scores_list 타입: {type(scores_list).__name__}, "
      f"값: {scores_list}")
print(f"first_student 타입: {type(first_student).__name__}")
print(f"first_student['name']: {first_student['name']}")
print(f"first_student.get('grade', 'N/A'): "
      f"{first_student.get('grade', 'N/A')}")

# -----------------------------------------------------------------------------
# 3) for / if 로 등급 부여 후 통계 (1.2.3 제어문)
# -----------------------------------------------------------------------------
print("\n=== for + if 로 학생별 등급 부여 ===")
print(f"{'name':<10} {'score':>5}  {'grade':>5}")
print("-" * 25)
for _, row in df.iterrows():
    s = row["score"]
    if s >= 8:
        grade = "A"
    elif s >= 6:
        grade = "B"
    elif s >= 4:
        grade = "C"
    else:
        grade = "F"
    print(f"{row['name']:<10} {s:>5}  {grade:>5}")

# -----------------------------------------------------------------------------
# 4) 직접 구현한 평균/분산 함수 (1.2.4 함수, 1.2.5 실습)
# -----------------------------------------------------------------------------
def mean(data):
    return sum(data) / len(data)


def variance(data):
    m = mean(data)
    # 각 편차의 제곱을 모두 더한 뒤 데이터 수로 나눔 (모분산)
    return sum((x - m) ** 2 for x in data) / len(data)


print("\n=== 평균/분산 수동 계산 vs NumPy ===")
my_mean = mean(scores_list)
my_var = variance(scores_list)

# 수식의 각 항을 명시적으로 출력 — '한 단계 더 사고하기'
print(f"  합계 Σx = {sum(scores_list)}")
print(f"  데이터 수 n = {len(scores_list)}")
print(f"  평균 = Σx / n = {sum(scores_list)}/{len(scores_list)} = {my_mean:.4f}")

deviations_sq = [(x - my_mean) ** 2 for x in scores_list]
print(f"  각 편차 제곱: {[round(d, 3) for d in deviations_sq]}")
print(f"  편차제곱합 Σ(x-μ)² = {sum(deviations_sq):.4f}")
print(f"  분산 = Σ(x-μ)² / n = {sum(deviations_sq):.4f}/{len(scores_list)} "
      f"= {my_var:.4f}")

np_mean = np.mean(scores_list)
np_var = np.var(scores_list)
print(f"\nNumPy 평균: {np_mean:.4f}, NumPy 분산: {np_var:.4f}")
print(f"일치 여부: "
      f"{abs(my_mean - np_mean) < 1e-10 and abs(my_var - np_var) < 1e-10}")

print("\n[해석] 직접 코드로 풀어 본 수식과 NumPy의 결과가 일치하는 것을 "
      "확인했습니다.\n        이 패턴은 향후 모든 통계 검증의 기본입니다.")

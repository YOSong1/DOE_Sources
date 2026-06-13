import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.4 Pandas - Excel 활용 버전: 고객 및 거래 데이터 분석
# =============================================================================
# 책: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
# 페이지: 324259 - 1.4 Pandas
#
# sample_data.xlsx의 customers / transactions 시트를 통해:
#   1) 데이터 확인 (head/info/describe/shape) — 1.4.3
#   2) 선택과 필터링 — 1.4.4
#   3) 결측값 처리 — 1.4.6
#   4) groupby 집계 — 1.4.7
#   5) 정렬 — 1.4.8
#   6) 두 시트 병합(merge) 활용
# =============================================================================

import os
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(BASE, "sample_data.xlsx")

# -----------------------------------------------------------------------------
# 1) Excel 읽기 — 1.4.2
# -----------------------------------------------------------------------------
customers = pd.read_excel(XLSX, sheet_name="customers")
tx = pd.read_excel(XLSX, sheet_name="transactions")

print("=== customers 시트 ===")
print(customers)
print("\n=== transactions 시트 (앞 5건) ===")
print(tx.head())

# -----------------------------------------------------------------------------
# 2) 데이터 확인 — 1.4.3
# -----------------------------------------------------------------------------
print("\n=== 1.4.3 데이터 확인 ===")
print(f"customers.shape  = {customers.shape}")
print(f"customers.columns = {list(customers.columns)}")
print(f"customers.dtypes:\n{customers.dtypes}")
print("\ncustomers.describe():")
print(customers.describe(include="all"))

# -----------------------------------------------------------------------------
# 3) 선택과 필터링 — 1.4.4
# -----------------------------------------------------------------------------
print("\n=== 1.4.4 조건 필터링 ===")
high = customers[customers["Score"] >= 85]
print("Score >= 85 고객:")
print(high)

both = customers[
    (customers["Score"] >= 80) & (customers["Major"] == "Math")
]
print("\nScore>=80 AND Major=='Math':")
print(both)

# -----------------------------------------------------------------------------
# 4) 결측값 처리 — 1.4.6
# -----------------------------------------------------------------------------
print("\n=== 1.4.6 결측값 처리 ===")
print("열별 결측값 개수:")
print(customers.isna().sum())

mean_score = customers["Score"].mean()
print(f"\n결측값을 채울 평균 점수: {mean_score:.2f}")

# 명시적으로 단계 출력 — '한 단계 더 사고'
filled = customers.fillna({
    "Score": mean_score,
    "Major": "미정",
})
print("\n결측값 처리 후:")
print(filled)

# -----------------------------------------------------------------------------
# 5) groupby — 1.4.7
# -----------------------------------------------------------------------------
print("\n=== 1.4.7 groupby 집계 ===")
print("Region별 평균 Score:")
print(filled.groupby("Region")["Score"].mean().round(2))

print("\nMajor별 mean/sum/count:")
print(filled.groupby("Major")["Score"].agg(["mean", "sum", "count"]).round(2))

# -----------------------------------------------------------------------------
# 6) 정렬 — 1.4.8
# -----------------------------------------------------------------------------
print("\n=== 1.4.8 정렬 ===")
print("Score 내림차순:")
print(filled.sort_values("Score", ascending=False))

# -----------------------------------------------------------------------------
# 7) 두 시트 병합으로 더 깊은 분석
# -----------------------------------------------------------------------------
print("\n=== 두 시트 merge: 고객별 거래 합계 ===")
# transactions의 customer 컬럼과 customers의 Name 컬럼을 연결
merged = tx.merge(
    filled[["Name", "Region", "Major"]],
    left_on="customer", right_on="Name", how="left",
)
print("merged.head():")
print(merged.head())

print("\n고객별 거래 합계 (정렬):")
total_by_cust = (merged.groupby("customer")["amount"].sum()
                 .sort_values(ascending=False))
print(total_by_cust)

print("\n[해석] customers 시트의 인구정보와 transactions 시트의 거래 금액을 "
      "merge 하면\n        '고객 속성'과 '거래 행동'을 결합해 분석할 수 있습니다. "
      "Pandas의 강점입니다.")

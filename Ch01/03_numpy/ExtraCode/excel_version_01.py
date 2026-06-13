import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.3 Numpy - Excel 활용 버전: 제품 검사 데이터 분석
# =============================================================================
# 책: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
# 페이지: 324207 - 1.3 Numpy
#
# sample_data.xlsx의 products / scores 시트를 읽어:
#   1) DataFrame → NumPy 배열 변환 (1.3.2)
#   2) 인덱싱/슬라이싱 (1.3.3)
#   3) 벡터화 연산: 표준화 z-score (1.3.4)
#   4) 통계 함수 일괄 적용 (1.3.5)
#   5) reshape/전치 (1.3.7)
# =============================================================================

import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(BASE, "sample_data.xlsx")

# -----------------------------------------------------------------------------
# 1) Excel 데이터 읽기
# -----------------------------------------------------------------------------
products = pd.read_excel(XLSX, sheet_name="products")
scores_df = pd.read_excel(XLSX, sheet_name="scores")

print("=== Excel에서 읽은 데이터 ===")
print("[products 시트]")
print(products)
print("\n[scores 시트]")
print(scores_df)

# -----------------------------------------------------------------------------
# 2) DataFrame → NumPy 배열 (1.3.2 배열 생성)
# -----------------------------------------------------------------------------
# 측정값 3개 열(length/diameter/weight)을 (12 x 3) 행렬로
measure_cols = ["length_mm", "diameter_mm", "weight_g"]
measurements = products[measure_cols].to_numpy()
scores = scores_df["score"].to_numpy()

print(f"\nmeasurements 배열 형태: {measurements.shape} (제품 수 × 측정 항목 수)")
print(f"scores 배열 형태:        {scores.shape}")

# -----------------------------------------------------------------------------
# 3) 인덱싱/슬라이싱 (1.3.3)
# -----------------------------------------------------------------------------
print("\n=== 인덱싱/슬라이싱 ===")
print(f"첫 번째 제품 전체 측정값: {measurements[0, :]}")
print(f"마지막 제품의 무게(g):    {measurements[-1, 2]}")
print(f"앞 3개 제품의 length/diameter:\n{measurements[:3, :2]}")

# -----------------------------------------------------------------------------
# 4) 벡터화 연산: z-score 표준화 (1.3.4)
# -----------------------------------------------------------------------------
print("\n=== 벡터화 연산 (z-score 표준화) ===")
mu = measurements.mean(axis=0)      # 각 열의 평균
sigma = measurements.std(axis=0)    # 각 열의 표준편차

print(f"열 평균 μ (length, diameter, weight): {np.round(mu, 3)}")
print(f"열 표준편차 σ:                       {np.round(sigma, 3)}")

# 브로드캐스팅: (12,3) - (3,) → (12,3)
z = (measurements - mu) / sigma
print("\nz-score 표 (상위 5개 제품):")
print(np.round(z[:5], 3))
print("→ 각 측정값이 평균에서 표준편차의 몇 배 떨어져 있는지를 나타냅니다.")

# -----------------------------------------------------------------------------
# 5) 통계 함수 (1.3.5) — scores 배열에 일괄 적용
# -----------------------------------------------------------------------------
print("\n=== 시험 점수 데이터 통계 함수 일괄 적용 ===")
print(f"평균:    {np.mean(scores):.4f}")
print(f"중앙값:  {np.median(scores):.4f}")
print(f"표준편차(모): {np.std(scores):.4f}")
print(f"표준편차(표본, ddof=1): {np.std(scores, ddof=1):.4f}")
print(f"분산(모): {np.var(scores):.4f}")
print(f"최댓값:  {np.max(scores)}")
print(f"최솟값:  {np.min(scores)}")
print(f"합계:    {np.sum(scores)}")
print(f"Q1 (25%): {np.percentile(scores, 25):.4f}")
print(f"Q3 (75%): {np.percentile(scores, 75):.4f}")
print(f"IQR = Q3 - Q1 = "
      f"{np.percentile(scores, 75) - np.percentile(scores, 25):.4f}")

# -----------------------------------------------------------------------------
# 6) reshape / 전치 (1.3.7)
# -----------------------------------------------------------------------------
print("\n=== 형태 변환 ===")
print(f"원본 형태: {measurements.shape}")
print(f"전치 후 형태: {measurements.T.shape}  (측정 항목별로 모든 제품을 한 행에)")
print("전치 행렬의 첫 행 = 모든 제품의 length_mm:")
print(np.round(measurements.T[0], 2))

# -----------------------------------------------------------------------------
# 7) 내적 응용: 가중치 적용 (1.3.4 dot product)
# -----------------------------------------------------------------------------
# 각 측정값에 가중치를 부여하여 종합 점수 계산
weights = np.array([0.4, 0.3, 0.3])   # length, diameter, weight 중요도
composite = measurements @ weights    # (12,3) @ (3,) = (12,)
print(f"\n가중치 {weights}를 적용한 제품별 종합 점수:")
print(np.round(composite, 3))
print(f"내적 사용 평균: {np.dot(np.ones(12)/12, composite):.4f}")

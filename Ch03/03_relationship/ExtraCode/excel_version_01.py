"""
3.3 데이터 관계 분석 - Excel 활용 버전
==========================================
sample_data.xlsx의 공부시간 vs 시험점수 데이터를 읽어,
공분산과 피어슨 상관계수를 직접 계산식으로 단계별 출력하고,
numpy/scipy 결과와 일치하는지 비교한다.

학습 포인트:
- 공분산은 단위 의존적이라는 점을 직접 확인 (공부시간을 '분'으로 바꾸면 값이 60배로 증가)
- 상관계수는 단위가 바뀌어도 동일 (무차원).
"""

import os
import sys
import pandas as pd
import numpy as np
from scipy import stats

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

XLSX = os.path.join(os.path.dirname(__file__), "sample_data.xlsx")


def main():
    df = pd.read_excel(XLSX, sheet_name="공부시간_점수")
    print("=" * 60)
    print("1단계: Excel 데이터 구조")
    print("=" * 60)
    print(f"행/열: {df.shape}")
    print(f"컬럼: {list(df.columns)}")
    print(df.head())

    x = df["주당공부시간"].to_numpy(dtype=float)
    y = df["시험점수"].to_numpy(dtype=float)
    n = len(x)

    # 2. 평균
    print("\n" + "=" * 60)
    print("2단계: 평균 계산")
    print("=" * 60)
    x_bar, y_bar = x.mean(), y.mean()
    print(f"  공부시간 평균 (x_bar) = {x_bar:.4f}")
    print(f"  시험점수 평균 (y_bar) = {y_bar:.4f}")

    # 3. 공분산 직접 계산
    print("\n" + "=" * 60)
    print("3단계: 공분산 직접 계산")
    print("=" * 60)
    dx = x - x_bar
    dy = y - y_bar
    cross = dx * dy
    sum_cross = cross.sum()
    cov_sample = sum_cross / (n - 1)
    print(f"  Sum (xi - x_bar)(yi - y_bar) = {sum_cross:.4f}")
    print(f"  표본 공분산 = Sum / (n-1) = {sum_cross:.4f} / {n - 1} = {cov_sample:.4f}")
    print(f"  numpy 확인: np.cov(...)[0,1] = {np.cov(x, y, ddof=1)[0, 1]:.4f}")

    # 4. 상관계수 직접 계산
    print("\n" + "=" * 60)
    print("4단계: 상관계수 직접 계산")
    print("=" * 60)
    sx = np.sqrt((dx ** 2).sum() / (n - 1))
    sy = np.sqrt((dy ** 2).sum() / (n - 1))
    r_manual = cov_sample / (sx * sy)
    print(f"  표본표준편차 sx = {sx:.4f}, sy = {sy:.4f}")
    print(f"  r = Cov / (sx * sy) = {cov_sample:.4f} / ({sx:.4f} * {sy:.4f}) = {r_manual:.6f}")

    r_np = np.corrcoef(x, y)[0, 1]
    r_sp, p_val = stats.pearsonr(x, y)
    print(f"  np.corrcoef       = {r_np:.6f}")
    print(f"  scipy.pearsonr r  = {r_sp:.6f}, p-value = {p_val:.6g}")

    # 5. 단위를 바꿔도 상관계수는 동일하다는 점 확인
    print("\n" + "=" * 60)
    print("5단계: 단위 변환 실험 — 공부시간을 '분'으로 환산")
    print("=" * 60)
    x_min = x * 60  # 시간 -> 분
    cov_min = np.cov(x_min, y, ddof=1)[0, 1]
    r_min = np.corrcoef(x_min, y)[0, 1]
    print(f"  공분산 (시간 단위) = {cov_sample:.4f}")
    print(f"  공분산 (분 단위)   = {cov_min:.4f}   -> 정확히 60배가 됨 (단위 의존)")
    print(f"  상관계수 (시간) = {r_manual:.6f}")
    print(f"  상관계수 (분)   = {r_min:.6f}   -> 변하지 않음 (무차원)")

    # 6. 해석
    print("\n" + "=" * 60)
    print("6단계: 결과 해석")
    print("=" * 60)
    if abs(r_sp) >= 0.7:
        strength = "강한"
    elif abs(r_sp) >= 0.3:
        strength = "보통"
    else:
        strength = "약한"
    direction = "양" if r_sp > 0 else "음"
    print(f"  -> 공부시간과 시험점수 사이에는 {strength} {direction}의 상관관계 (r = {r_sp:.4f})")
    print(f"  -> p-value = {p_val:.4g} (< 0.05 이면 통계적으로 유의)")


if __name__ == "__main__":
    main()

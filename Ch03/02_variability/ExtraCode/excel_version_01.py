"""
3.2 데이터 변동성 - Excel 활용 버전
========================================
sample_data.xlsx의 두 공장 부품 직경 데이터를 읽어
범위 / 분산 / 표준편차 / IQR / 변동계수를 각각 손계산처럼 단계별로 계산하고,
두 공장의 변동성 차이를 비교한다.

학습 포인트:
- 평균이 거의 같아도 변동성이 다르면 품질이 완전히 다르다.
- 표본분산 분모로 n-1을 사용하는 이유(불편추정량)를 직접 비교 확인.
- 변동계수는 단위가 같더라도 평균 대비 상대 변동성을 비교할 때 유용.
"""

import os
import sys
import pandas as pd
import numpy as np

# Windows cp949 환경에서도 한글이 깨지지 않도록 UTF-8 stdout 강제
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

XLSX = os.path.join(os.path.dirname(__file__), "sample_data.xlsx")


def analyze(name: str, x: np.ndarray) -> dict:
    print("\n" + "=" * 60)
    print(f"[{name} 공장 분석] (n={len(x)})")
    print("=" * 60)
    n = len(x)
    mean = x.mean()
    print(f"  최솟값/최댓값: {x.min():.3f} / {x.max():.3f}")
    print(f"  평균: {mean:.4f} mm")

    # 1) 범위
    rng = x.max() - x.min()
    print(f"  (1) 범위(Range) = max - min = {rng:.4f}")

    # 2) 분산 (직접 계산 vs numpy)
    deviation = x - mean
    sq_dev = deviation ** 2
    pop_var = sq_dev.sum() / n
    samp_var = sq_dev.sum() / (n - 1)
    print(f"  (2) Sum (xi - mean)^2 = {sq_dev.sum():.4f}")
    print(f"      모분산   = Sum(xi-mean)^2 / n     = {pop_var:.4f}")
    print(f"      표본분산 = Sum(xi-mean)^2 / (n-1) = {samp_var:.4f}  <- 분모가 n-1")

    # 3) 표준편차
    pop_std = np.sqrt(pop_var)
    samp_std = np.sqrt(samp_var)
    print(f"  (3) 모표준편차    = sqrt(모분산)   = {pop_std:.4f} mm")
    print(f"      표본표준편차 = sqrt(표본분산) = {samp_std:.4f} mm")

    # 4) IQR
    q1, q3 = np.percentile(x, [25, 75])
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = x[(x < low) | (x > high)]
    print(f"  (4) Q1={q1:.4f}, Q3={q3:.4f}, IQR={iqr:.4f}")
    print(f"      이상치 경계: [{low:.4f}, {high:.4f}], 이상치 개수: {len(outliers)}")

    # 5) 변동계수
    cv = samp_std / mean * 100
    print(f"  (5) 변동계수(CV) = s / mean * 100 = {cv:.3f}%")

    return dict(mean=mean, samp_std=samp_std, iqr=iqr, cv=cv)


def main():
    df = pd.read_excel(XLSX, sheet_name="공정데이터")
    print("=" * 60)
    print("Excel에서 읽은 데이터 구조")
    print("=" * 60)
    print(f"행/열: {df.shape}")
    print(f"컬럼: {list(df.columns)}")
    print(df.head())

    A = df["A공장_직경_mm"].to_numpy()
    B = df["B공장_직경_mm"].to_numpy()

    stat_A = analyze("A", A)
    stat_B = analyze("B", B)

    print("\n" + "=" * 60)
    print("두 공장 변동성 종합 비교")
    print("=" * 60)
    print(f"  평균:         A={stat_A['mean']:.4f}  vs  B={stat_B['mean']:.4f}")
    print(f"  표본표준편차: A={stat_A['samp_std']:.4f}  vs  B={stat_B['samp_std']:.4f}")
    print(f"  IQR:          A={stat_A['iqr']:.4f}  vs  B={stat_B['iqr']:.4f}")
    print(f"  변동계수:     A={stat_A['cv']:.3f}%  vs  B={stat_B['cv']:.3f}%")
    ratio = stat_B['samp_std'] / stat_A['samp_std']
    print(f"\n  -> B공장 표준편차는 A공장의 {ratio:.2f}배. 평균이 비슷해도 품질 균일성은 A가 훨씬 우수.")


if __name__ == "__main__":
    main()

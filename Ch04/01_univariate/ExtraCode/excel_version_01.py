"""
4.1 1차원 확률 변수 - Excel 활용 버전
==========================================
sample_data.xlsx 의 주사위 600회 결과를 읽어
- 경험적 PMF, CDF를 계산하여 이론 PMF/CDF와 비교
- 정의식 E[X] = Σ x·P(X=x), Var(X) = E[X²] - (E[X])² 를 단계별로 적용
- 시행 수가 늘어남에 따라 표본 추정치가 이론값에 수렴함을 확인

학습 포인트:
- "확률 = 시행 횟수가 많아질 때의 상대 빈도" 라는 직관을 직접 데이터로 확인.
- PMF 정의(합 = 1)와 CDF 정의(누적합)를 수기 식으로 계산.
"""

import os
import sys
import pandas as pd
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

XLSX = os.path.join(os.path.dirname(__file__), "sample_data.xlsx")


def main():
    rolls_df = pd.read_excel(XLSX, sheet_name="굴림결과")
    print("=" * 60)
    print("1단계: Excel 데이터 구조")
    print("=" * 60)
    print(f"행/열: {rolls_df.shape}")
    print(f"컬럼: {list(rolls_df.columns)}")
    print(rolls_df.head())

    rolls = rolls_df["주사위눈"].to_numpy()
    n = len(rolls)
    x_vals = np.arange(1, 7)

    # 2. 경험적 PMF
    print("\n" + "=" * 60)
    print("2단계: 경험적 PMF — 각 눈의 상대 빈도")
    print("=" * 60)
    counts = np.array([(rolls == k).sum() for k in x_vals])
    emp_pmf = counts / n
    theo_pmf = np.full(6, 1 / 6)
    print(f"  눈 : 빈도 / 상대빈도(P̂) / 이론(1/6=0.1667)")
    for k, c, p in zip(x_vals, counts, emp_pmf):
        print(f"   {k}  : {c:4d}  /  {p:.4f}        /  0.1667")
    print(f"  P̂의 합 = {emp_pmf.sum():.4f}  (PMF 정의에 의해 1이어야 함)")

    # 3. 경험적 CDF
    print("\n" + "=" * 60)
    print("3단계: 경험적 CDF — 누적합")
    print("=" * 60)
    emp_cdf = np.cumsum(emp_pmf)
    theo_cdf = np.cumsum(theo_pmf)
    for k, fc, tc in zip(x_vals, emp_cdf, theo_cdf):
        print(f"  F(x≤{k}) = {fc:.4f}   |  이론 = {tc:.4f}")

    # 4. 기댓값 정의식 적용
    print("\n" + "=" * 60)
    print("4단계: E[X] = Σ x · P(X = x)")
    print("=" * 60)
    e_x = np.sum(x_vals * emp_pmf)
    e_x_theory = np.sum(x_vals * theo_pmf)
    print("  항별 기여 (x * P̂):")
    for k, p in zip(x_vals, emp_pmf):
        print(f"    {k} × {p:.4f} = {k * p:.4f}")
    print(f"  → E[X] (표본)  = {e_x:.4f}")
    print(f"  → E[X] (이론)  = {e_x_theory:.4f} (=3.5)")

    # 5. 분산 정의식 적용 (두 방식 비교)
    print("\n" + "=" * 60)
    print("5단계: Var(X) — 두 가지 공식 비교")
    print("=" * 60)
    # 방식 A: Σ (x - μ)² P(X=x)
    var_a = np.sum(((x_vals - e_x) ** 2) * emp_pmf)
    # 방식 B: E[X²] - (E[X])²
    e_x2 = np.sum((x_vals ** 2) * emp_pmf)
    var_b = e_x2 - e_x ** 2
    print(f"  방식 A: Σ(x-μ)² P̂(x)   = {var_a:.4f}")
    print(f"  방식 B: E[X²] - (E[X])² = {e_x2:.4f} - {e_x ** 2:.4f} = {var_b:.4f}")
    print(f"  두 값이 일치하는지: {np.isclose(var_a, var_b)}")
    print(f"  이론 분산 = 2.9167")

    # 6. 표본 크기별 수렴 확인 (대수의 법칙)
    print("\n" + "=" * 60)
    print("6단계: 시행 수 늘릴수록 표본 평균이 이론값(3.5)에 수렴")
    print("=" * 60)
    for sub in [10, 50, 100, 300, 600]:
        print(f"  처음 {sub:3d}회 평균 = {rolls[:sub].mean():.4f}")


if __name__ == "__main__":
    main()

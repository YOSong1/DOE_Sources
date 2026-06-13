"""
4.2 2차원 확률 변수 - Excel 활용 버전
==========================================
sample_data.xlsx 의 (키, 몸무게) 200명 데이터를 읽어
- 두 변수를 구간으로 나눠 결합 PMF 표 작성
- 주변 PMF / 조건부 PMF / 독립성 / 공분산 / 상관계수를 차례로 계산
- 동일한 데이터를 다른 단위(키를 m로)로 변환하여 공분산은 단위 의존적, 상관계수는 무차원임을 확인

학습 포인트:
- 연속형 데이터를 구간(bin)으로 묶어 이산형 결합 분포로 다루는 실용적 기법.
- 주변화 = 행/열 합, 조건부 = 행/열 합으로 나누기.
- 독립성 검증: P(X,Y) ≈ P(X)·P(Y) 인지 비교.
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
    df = pd.read_excel(XLSX, sheet_name="키몸무게")
    print("=" * 60)
    print("1단계: Excel 데이터 구조")
    print("=" * 60)
    print(f"행/열: {df.shape}")
    print(f"컬럼: {list(df.columns)}")
    print(df.head())

    h = df["키_cm"].to_numpy()
    w = df["몸무게_kg"].to_numpy()
    n = len(h)

    # 2. 키/몸무게를 3개 구간으로 묶기
    print("\n" + "=" * 60)
    print("2단계: 연속형 → 이산화 (3개 구간으로 묶기)")
    print("=" * 60)
    h_bins = ["저(150~165)", "중(165~175)", "고(175~)"]
    w_bins = ["저(~60)", "중(60~70)", "고(70~)"]
    h_cat = pd.cut(h, bins=[-np.inf, 165, 175, np.inf], labels=h_bins)
    w_cat = pd.cut(w, bins=[-np.inf, 60, 70, np.inf], labels=w_bins)

    # 3. 결합 PMF
    print("\n" + "=" * 60)
    print("3단계: 결합 PMF P(X=h_i, Y=w_j) 계산")
    print("=" * 60)
    joint_count = pd.crosstab(w_cat, h_cat)
    joint_pmf = joint_count / n
    print("  결합 빈도표(W는 행, H는 열):")
    print(joint_count)
    print("\n  결합 PMF (각 칸 / n):")
    print(joint_pmf.round(4))
    print(f"  합계 확인: {joint_pmf.values.sum():.4f}  (= 1)")

    # 4. 주변 PMF
    print("\n" + "=" * 60)
    print("4단계: 주변 PMF (Marginal) — 행/열 합")
    print("=" * 60)
    p_h = joint_pmf.sum(axis=0)
    p_w = joint_pmf.sum(axis=1)
    print(f"  P_H(키 구간별): \n{p_h.round(4)}")
    print(f"  P_W(몸무게 구간별): \n{p_w.round(4)}")

    # 5. 조건부 PMF — 키가 '고(175~)' 일 때 몸무게 분포
    print("\n" + "=" * 60)
    print("5단계: 조건부 PMF — 키가 '고(175~)'인 사람의 몸무게 분포")
    print("=" * 60)
    target_h = "고(175~)"
    cond = joint_pmf[target_h] / p_h[target_h]
    print(f"  P(W | H={target_h}):")
    print(cond.round(4))
    print(f"  합 = {cond.sum():.4f} (조건부 PMF는 합이 1)")

    # 6. 독립성 검증 — P(X,Y) vs P(X)P(Y)
    print("\n" + "=" * 60)
    print("6단계: 독립성 검증 — P(X,Y) ≈ P(X) · P(Y) ?")
    print("=" * 60)
    p_indep = np.outer(p_w.values, p_h.values)   # 행: W, 열: H
    diff = joint_pmf.values - p_indep
    print(f"  실제 결합 PMF:\n{joint_pmf.round(4).values}")
    print(f"\n  곱(독립 가정) P(X)·P(Y):\n{p_indep.round(4)}")
    print(f"\n  차이의 절댓값 최대: {np.abs(diff).max():.4f}")
    if np.abs(diff).max() > 0.05:
        print("  -> 차이가 의미 있게 큼 → 독립이 아님 (강한 상관 시사)")
    else:
        print("  -> 차이가 작음 → 거의 독립")

    # 7. 공분산과 상관계수 (원시 데이터)
    print("\n" + "=" * 60)
    print("7단계: 공분산 / 상관계수 — 정의식 적용")
    print("=" * 60)
    h_bar, w_bar = h.mean(), w.mean()
    cov_hw = ((h - h_bar) * (w - w_bar)).sum() / (n - 1)
    sh = np.sqrt(((h - h_bar) ** 2).sum() / (n - 1))
    sw = np.sqrt(((w - w_bar) ** 2).sum() / (n - 1))
    rho = cov_hw / (sh * sw)
    print(f"  평균: 키={h_bar:.3f} cm, 몸무게={w_bar:.3f} kg")
    print(f"  표본 표준편차: s_h={sh:.4f}, s_w={sw:.4f}")
    print(f"  Cov(H, W) = Σ(h-h̄)(w-w̄)/(n-1) = {cov_hw:.4f}")
    print(f"  ρ = Cov / (s_h · s_w) = {rho:.6f}")
    print(f"  numpy 확인: np.corrcoef = {np.corrcoef(h, w)[0,1]:.6f}")

    # 8. 단위 변환 실험 (키를 m로)
    print("\n" + "=" * 60)
    print("8단계: 단위 변환 — 키를 m로 바꾸면?")
    print("=" * 60)
    h_m = h / 100.0
    cov_new = np.cov(h_m, w, ddof=1)[0, 1]
    rho_new = np.corrcoef(h_m, w)[0, 1]
    print(f"  공분산 (cm 단위) = {cov_hw:.4f}")
    print(f"  공분산 (m  단위) = {cov_new:.6f}   (정확히 1/100배 — 단위 의존)")
    print(f"  상관계수 (cm) = {rho:.6f}")
    print(f"  상관계수 (m)  = {rho_new:.6f}   (변하지 않음 — 무차원)")


if __name__ == "__main__":
    main()

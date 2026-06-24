# code_14_05_solution.py
# -*- coding: utf-8 -*-
"""
페이지: 14.5 연습 문제 — 자동차 연비 개선을 위한 엔진 파라미터 최적화 [해답]
================================================================================
다구찌 방법(Taguchi Method)을 이용한 엔진 파라미터 최적화 연습 문제의 풀이.

문제 요약
---------
3개의 3수준 인자(A: 점화 시점, B: 연료 분사압, C: 공기흡입량)에 대해
L9 직교배열을 적용하여 연비(km/L)를 최대화(망대특성)하는 최적 조건을 찾는다.
각 조건당 1회 측정(n=1)을 가정한다.

해결 단계
---------
1) L9 직교배열 설계 및 실험 계획표 작성
2) 가상 연비 데이터 생성 (문제 제공 코드와 동일, seed=123)
3) 망대특성 S/N비 계산 및 데이터프레임에 열 추가
4) 인자별 수준 평균 S/N비(주효과) 분석
5) 최적 수준 조합 도출 및 최적 조건에서의 S/N비 예측
6) 시각화: S/N 주효과도 + 잔차 분석(주효과 합으로 예측한 S/N vs 관측 S/N)

주의: 본 풀이는 자기완결형이며 외부 xlsx 파일을 사용하지 않는다.
      matplotlib만 사용(seaborn 미사용), 한글 폰트는 Malgun Gothic.
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- 한글 폰트 및 마이너스 기호 설정 ---
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))

# 인자 코드 → 설명 라벨/단위
FACTOR_LABELS = {
    "A": "점화 시점 (BTDC °)",
    "B": "연료 분사압 (bar)",
    "C": "공기흡입량 (L/min)",
}


# ------------------------------------------------------------------------------
# [1] L9 직교배열 설계 및 데이터 생성
# ------------------------------------------------------------------------------
def build_l9_data():
    """문제 제공 코드와 동일한 로직(seed=123)으로 L9 실험 데이터를 생성한다."""
    # --- 요인 수준 정의 ---
    levels_A_engine = [10, 12, 14]      # 점화 시점 (BTDC °)
    levels_B_engine = [100, 120, 140]   # 연료 분사압 (bar)
    levels_C_engine = [300, 350, 400]   # 공기흡입량 (L/min)

    # L9 직교배열 인덱스 (0,1,2 는 각 levels 리스트의 인덱스)
    l9_design_indices_engine = [
        (0, 0, 0), (0, 1, 1), (0, 2, 2),
        (1, 0, 1), (1, 1, 2), (1, 2, 0),
        (2, 0, 2), (2, 1, 0), (2, 2, 1),
    ]

    # --- 가상의 연비(반응값) 데이터 생성 ---
    np.random.seed(123)  # 재현성을 위한 시드 (문제와 동일)
    base_efficiency = 10.0

    # 각 요인 수준에 따른 숨겨진 효과
    effect_A = {10: 0.5, 12: 1.0, 14: 0.2}
    effect_B = {100: 0.8, 120: 0.5, 140: -0.2}
    effect_C = {300: -0.3, 350: 0.6, 400: 1.2}

    rows = []
    for run, (a_idx, b_idx, c_idx) in enumerate(l9_design_indices_engine, start=1):
        val_A = levels_A_engine[a_idx]
        val_B = levels_B_engine[b_idx]
        val_C = levels_C_engine[c_idx]

        eff = (base_efficiency + effect_A[val_A] + effect_B[val_B]
               + effect_C[val_C] + np.random.normal(0, 0.3))
        rows.append({
            "Run": run,
            "A": val_A,
            "B": val_B,
            "C": val_C,
            "Fuel_Efficiency": round(eff, 2),
        })

    df = pd.DataFrame(rows)
    return df


# ------------------------------------------------------------------------------
# [2] 망대특성 S/N비
# ------------------------------------------------------------------------------
def sn_larger_the_better(y, n=1):
    """
    망대특성(더 클수록 좋은) S/N비.
        S/N = -10 * log10( (1/n) * sum(1/y_i^2) )
    반복이 없으므로(n=1) 단일 측정값 y에 대해 계산한다.
    """
    y = np.asarray(y, dtype=float)
    return -10.0 * np.log10((1.0 / n) * (1.0 / (y ** 2)))


# ------------------------------------------------------------------------------
# [3] 인자별 수준 평균 S/N비(주효과) 분석
# ------------------------------------------------------------------------------
def level_means(df, factor, value_col="SN"):
    """특정 인자의 각 수준별 평균값(주효과)을 반환한다."""
    return df.groupby(factor)[value_col].mean()


def main():
    # === 1. 실험 계획표 ===
    df = build_l9_data()
    print("=" * 64)
    print("[1] L9 직교배열 실험 계획표 (각 인자의 실제 수준 값)")
    print("=" * 64)
    print(df.to_string(index=False))

    # === 2. S/N비 계산 (망대특성) ===
    df["SN"] = sn_larger_the_better(df["Fuel_Efficiency"].values, n=1)
    print("\n" + "=" * 64)
    print("[2] 망대특성 S/N비 계산 결과 (n=1)")
    print("=" * 64)
    print(df.round(4).to_string(index=False))

    # === 3. 인자별 수준 평균 S/N비 (주효과) ===
    print("\n" + "=" * 64)
    print("[3] 인자별 수준 평균 S/N비 (주효과 분석)")
    print("=" * 64)
    sn_tables = {}
    for f in ["A", "B", "C"]:
        m = level_means(df, f, "SN")
        sn_tables[f] = m
        print(f"\n  인자 {f} - {FACTOR_LABELS[f]}")
        print(m.round(4).to_string())

    # 주효과 크기(델타 = 최대-최소 평균 S/N) 로 영향력 순위
    deltas = {f: float(sn_tables[f].max() - sn_tables[f].min()) for f in ["A", "B", "C"]}
    rank = sorted(deltas, key=deltas.get, reverse=True)
    print("\n  주효과 크기(Delta = max-min 평균 S/N):")
    for r, f in enumerate(rank, start=1):
        print(f"    {r}순위  인자 {f} ({FACTOR_LABELS[f]}): Delta = {deltas[f]:.4f}")

    # === 4. 최적 수준 조합 도출 ===
    print("\n" + "=" * 64)
    print("[4] 최적 수준 조합 (S/N비 최대화)")
    print("=" * 64)
    optimum = {f: int(sn_tables[f].idxmax()) for f in ["A", "B", "C"]}
    for f in ["A", "B", "C"]:
        print(f"  인자 {f} ({FACTOR_LABELS[f]}): 최적 수준 = {optimum[f]}"
              f"  (평균 S/N = {sn_tables[f].max():.4f})")

    # === 5. 최적 조건에서의 S/N비 예측 ===
    # 예측식: SN_pred = grand_mean + sum( (인자별 최적수준 평균 S/N) - grand_mean )
    grand_mean = df["SN"].mean()
    sn_pred = grand_mean + sum(sn_tables[f].max() - grand_mean for f in ["A", "B", "C"])
    # S/N비 -> 예측 연비 환산 (망대특성: y = 10^(SN/20))
    eff_pred = 10.0 ** (sn_pred / 20.0)
    print("\n" + "=" * 64)
    print("[5] 최적 조건 예측")
    print("=" * 64)
    print(f"  전체 평균 S/N비(grand mean) : {grand_mean:.4f} dB")
    print(f"  예측 S/N비(최적 조건)        : {sn_pred:.4f} dB")
    print(f"  예측 연비(환산)             : {eff_pred:.4f} km/L")
    print(f"  실험 내 최대 연비           : {df['Fuel_Efficiency'].max():.2f} km/L "
          f"(Run {int(df.loc[df['Fuel_Efficiency'].idxmax(), 'Run'])})")

    print("\n  [결론] 연비 최대화 최적 조건:")
    print(f"    - 점화 시점(A)   : BTDC {optimum['A']}°")
    print(f"    - 연료 분사압(B) : {optimum['B']} bar")
    print(f"    - 공기흡입량(C)  : {optimum['C']} L/min")
    print("  가장 영향력이 큰 인자는 "
          f"'{FACTOR_LABELS[rank[0]]}' (인자 {rank[0]}) 이다.")
    print("  향후 검증: 위 최적 조건으로 확인 실험(confirmation run)을 수행하여")
    print("            예측 S/N비/연비가 재현되는지 확인할 것을 권장한다.")

    # === 6. 시각화 ===
    plot_main_effects(df, sn_tables, grand_mean, optimum)
    plot_residuals(df, sn_tables, grand_mean)

    print("\n분석 완료. PNG 파일이 저장되었습니다.")


# ------------------------------------------------------------------------------
# 시각화 1: S/N 주효과도
# ------------------------------------------------------------------------------
def plot_main_effects(df, sn_tables, grand_mean, optimum):
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), sharey=True)
    for ax, f in zip(axes, ["A", "B", "C"]):
        m = sn_tables[f]
        ax.plot(m.index.astype(str), m.values, "o-", color="#1f77b4", lw=2, ms=8)
        ax.axhline(grand_mean, color="gray", ls="--", lw=1, alpha=0.7,
                   label="전체 평균")
        # 최적 수준 강조
        opt_val = optimum[f]
        ax.plot(str(opt_val), m.loc[opt_val], "o", color="red", ms=12,
                mfc="none", mew=2, label="최적 수준")
        ax.set_title(f"인자 {f}\n{FACTOR_LABELS[f]}")
        ax.set_xlabel("수준")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("평균 S/N비 (dB)")
    axes[0].legend(loc="best", fontsize=9)
    fig.suptitle("S/N비 주효과도 (망대특성, 클수록 좋음)", fontsize=14, y=1.02)
    plt.tight_layout()
    out = os.path.join(HERE, "code_14_05_solution_main_effects.png")
    plt.savefig(out, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"\n  [그림 저장] S/N 주효과도 -> {os.path.basename(out)}")


# ------------------------------------------------------------------------------
# 시각화 2: 주효과 모형 적합도 / 잔차 분석
# ------------------------------------------------------------------------------
def plot_residuals(df, sn_tables, grand_mean):
    """가법(주효과) 모형으로 각 실험의 S/N비를 예측하고 잔차를 분석한다."""
    # 가법 모형 예측: SN_hat = grand_mean + (A효과) + (B효과) + (C효과)
    sn_hat = []
    for _, row in df.iterrows():
        pred = grand_mean
        for f in ["A", "B", "C"]:
            pred += sn_tables[f].loc[row[f]] - grand_mean
        sn_hat.append(pred)
    df = df.copy()
    df["SN_hat"] = sn_hat
    df["Residual"] = df["SN"] - df["SN_hat"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # (a) 관측 S/N vs 예측 S/N
    ax = axes[0]
    ax.scatter(df["SN_hat"], df["SN"], color="#1f77b4", s=60, zorder=3)
    lo = min(df["SN_hat"].min(), df["SN"].min())
    hi = max(df["SN_hat"].max(), df["SN"].max())
    ax.plot([lo, hi], [lo, hi], "r--", lw=1.5, label="y = x")
    ax.set_xlabel("예측 S/N비 (가법 모형, dB)")
    ax.set_ylabel("관측 S/N비 (dB)")
    ax.set_title("관측 vs 예측 S/N비")
    ax.legend()
    ax.grid(alpha=0.3)

    # (b) 잔차 플롯 (Run 순서)
    ax = axes[1]
    ax.stem(df["Run"], df["Residual"], basefmt=" ")
    ax.axhline(0, color="gray", lw=1)
    ax.set_xlabel("실험 번호 (Run)")
    ax.set_ylabel("잔차 (관측 - 예측, dB)")
    ax.set_title("잔차 플롯")
    ax.set_xticks(df["Run"])
    ax.grid(alpha=0.3)

    fig.suptitle("가법(주효과) 모형 적합도 및 잔차 분석", fontsize=14, y=1.02)
    plt.tight_layout()
    out = os.path.join(HERE, "code_14_05_solution_residuals.png")
    plt.savefig(out, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  [그림 저장] 잔차 분석 -> {os.path.basename(out)}")


if __name__ == "__main__":
    main()

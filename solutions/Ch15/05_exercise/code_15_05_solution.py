# code_15_05_solution.py
# -*- coding: utf-8 -*-
"""
15.5 연습 문제 해답 — 서로 다른 학습 방법의 효과 비교 (RCBD / 난괴법)
=======================================================================
세 가지 학습 방법(처리 A, B, C)의 효과를, 학생들의 기존 성취 수준(블록: 상/중/하)을
통제한 난괴법(Randomized Complete Block Design)으로 분석한다.

자기완결형(self-contained) 스크립트:
  - 문제에서 제시한 데이터 생성 코드(seed=555)를 그대로 포함 → 외부 xlsx 미사용
  - matplotlib 만 사용(seaborn 미사용), 한글 폰트 Malgun Gothic

구현 과제
  [1] 가상 데이터 생성 및 데이터프레임 구성 / 구조 확인
  [2] RCBD ANOVA — 처리(Treatment) + 블록(Block) 효과 분리
  [3] 유의효과(α=0.05) 식별 및 블록화 효율 검토
  [4] 처리 평균 비교 및 사후분석(Tukey HSD)
  [5] 처리/블록 효과 및 잔차 진단 시각화 (PNG 저장)
  [6] 최적 학습 방법 도출 및 출력
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# --- matplotlib 한글 폰트 설정 ---
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
ALPHA = 0.05


def make_data() -> pd.DataFrame:
    """문제에서 제시한 코드 조각(seed=555) 그대로 18개 데이터 생성."""
    treatments = ["A", "B", "C"]  # 학습 방법
    blocks = ["Block1_High", "Block2_Mid", "Block3_Low"]  # 성취 수준 그룹(블록)
    replicates_per_cell = 2  # 각 블록-처리 조합당 반복 수

    np.random.seed(555)  # 결과 재현성을 위한 시드
    rows = []

    block_effects = {"Block1_High": 15, "Block2_Mid": 5, "Block3_Low": -5}
    treatment_effects = {"A": 5, "B": -2, "C": 8}
    base_score = 60

    for block in blocks:
        for treatment in treatments:
            for _ in range(replicates_per_cell):
                score = (
                    base_score
                    + block_effects[block]
                    + treatment_effects[treatment]
                    + np.random.normal(0, 3)
                )
                score = round(float(np.clip(score, 0, 100)), 1)
                rows.append({"Block": block, "Treatment": treatment, "Score": score})

    return pd.DataFrame(rows)


def main() -> None:
    # =========================================================
    # [1] 데이터 생성 및 구조 확인
    # =========================================================
    df = make_data()
    print("=" * 64)
    print("[1] 데이터 생성 및 구조 확인")
    print("=" * 64)
    print(df.to_string(index=False))
    print(f"\n총 데이터 수: {df.shape[0]}개  (3 블록 × 3 처리 × 2 반복)")

    print("\n블록 × 처리 평균 점수 (피벗):")
    pivot = df.pivot_table(index="Block", columns="Treatment",
                           values="Score", aggfunc="mean")
    print(pivot.round(2))

    print("\n처리(학습 방법)별 평균 점수:")
    print(df.groupby("Treatment")["Score"].mean().round(2).to_string())
    print("\n블록(성취 수준)별 평균 점수:")
    print(df.groupby("Block")["Score"].mean().round(2).to_string())

    # =========================================================
    # [2] RCBD ANOVA — 처리 + 블록 효과 분리
    # =========================================================
    print("\n" + "=" * 64)
    print("[2] RCBD ANOVA (처리 + 블록 모델)")
    print("=" * 64)
    model_rcbd = ols("Score ~ C(Treatment) + C(Block)", data=df).fit()
    anova_rcbd = sm.stats.anova_lm(model_rcbd, typ=2)
    print(anova_rcbd.round(4))

    # =========================================================
    # [3] 유의효과 식별 (α=0.05) + 블록화 효율
    # =========================================================
    print("\n" + "=" * 64)
    print("[3] 유의효과 판정 (α=0.05) 및 블록화 효율")
    print("=" * 64)

    p_treat = anova_rcbd.loc["C(Treatment)", "PR(>F)"]
    p_block = anova_rcbd.loc["C(Block)", "PR(>F)"]

    treat_sig = p_treat < ALPHA
    block_sig = p_block < ALPHA

    print(f"  처리(Treatment) p-value = {p_treat:.4g}  → "
          f"{'유의함 (학습 방법 간 차이 있음)' if treat_sig else '유의하지 않음'}")
    print(f"  블록(Block)     p-value = {p_block:.4g}  → "
          f"{'유의함 (성취 수준 간 차이 있음)' if block_sig else '유의하지 않음'}")

    sig_effects = []
    if treat_sig:
        sig_effects.append("Treatment")
    if block_sig:
        sig_effects.append("Block")
    print(f"\n  → p<{ALPHA} 유의 효과: {sig_effects if sig_effects else '없음'}")

    # 블록화 효율: CRD(블록 무시) MSE 와 RCBD MSE 비교
    model_crd = ols("Score ~ C(Treatment)", data=df).fit()
    anova_crd = sm.stats.anova_lm(model_crd, typ=2)
    mse_rcbd = anova_rcbd.loc["Residual", "sum_sq"] / anova_rcbd.loc["Residual", "df"]
    mse_crd = anova_crd.loc["Residual", "sum_sq"] / anova_crd.loc["Residual", "df"]
    efficiency = mse_crd / mse_rcbd

    print("\n  [블록화 효율 검토] CRD(블록 무시) vs RCBD")
    print(f"    MSE_CRD  = {mse_crd:.4f}")
    print(f"    MSE_RCBD = {mse_rcbd:.4f}")
    print(f"    상대효율 ε = MSE_CRD / MSE_RCBD = {efficiency:.3f}")
    if efficiency > 1:
        print(f"    → ε>1: 블록화로 오차분산이 줄어 블록 설계가 효과적이었음.")
    else:
        print(f"    → ε≤1: 블록화 이득이 미미함.")

    # =========================================================
    # [4] 처리 평균 비교 및 사후분석(Tukey HSD)
    # =========================================================
    print("\n" + "=" * 64)
    print("[4] 처리 평균 비교 및 사후분석 (Tukey HSD)")
    print("=" * 64)
    if treat_sig:
        print("  처리 효과가 유의 → Tukey HSD 다중비교 수행:")
        tukey = pairwise_tukeyhsd(df["Score"], df["Treatment"], alpha=ALPHA)
        print(tukey.summary())
    else:
        print("  처리 효과가 유의하지 않아 사후분석을 생략합니다.")
        tukey = None

    # =========================================================
    # [5] 시각화 (처리/블록 효과 + 잔차 진단)
    # =========================================================
    print("\n" + "=" * 64)
    print("[5] 시각화 (PNG 저장)")
    print("=" * 64)

    treat_means = df.groupby("Treatment")["Score"].mean()
    treat_sems = df.groupby("Treatment")["Score"].sem()
    block_means = df.groupby("Block")["Score"].mean()

    resid = model_rcbd.resid
    fitted = model_rcbd.fittedvalues

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))

    # (a) 처리별 평균 점수 ± 표준오차
    ax = axes[0, 0]
    ax.bar(treat_means.index, treat_means.values,
           yerr=treat_sems.values, capsize=6,
           color=["#4C72B0", "#DD8452", "#55A868"], edgecolor="black")
    for x, v in zip(range(len(treat_means)), treat_means.values):
        ax.text(x, v + 0.5, f"{v:.1f}", ha="center", va="bottom", fontsize=10)
    ax.set_title("학습 방법별 평균 점수 (±표준오차)")
    ax.set_xlabel("학습 방법 (Treatment)")
    ax.set_ylabel("문제 해결 능력 점수")

    # (b) 블록별 평균 점수
    ax = axes[0, 1]
    ax.bar(block_means.index, block_means.values,
           color="#8172B3", edgecolor="black")
    for x, v in zip(range(len(block_means)), block_means.values):
        ax.text(x, v + 0.5, f"{v:.1f}", ha="center", va="bottom", fontsize=10)
    ax.set_title("성취 수준 그룹(블록)별 평균 점수")
    ax.set_xlabel("블록 (Block)")
    ax.set_ylabel("문제 해결 능력 점수")
    ax.tick_params(axis="x", rotation=10)

    # (c) 잔차 vs 적합값 (등분산성 진단)
    ax = axes[1, 0]
    ax.scatter(fitted, resid, color="#C44E52", edgecolor="black")
    ax.axhline(0, color="gray", linestyle="--")
    ax.set_title("잔차 진단: 잔차 vs 적합값")
    ax.set_xlabel("적합값 (Fitted)")
    ax.set_ylabel("잔차 (Residual)")

    # (d) 잔차 Q-Q plot (정규성 진단)
    ax = axes[1, 1]
    sm.qqplot(resid, line="s", ax=ax)
    ax.set_title("잔차 진단: 정규 Q-Q Plot")

    fig.suptitle("RCBD 분석 결과 — 학습 방법 효과 비교", fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.97))

    png_path = os.path.join(HERE, "code_15_05_solution_result.png")
    fig.savefig(png_path, dpi=120)
    plt.close(fig)
    print(f"  그림 저장: {os.path.basename(png_path)}")

    # =========================================================
    # [6] 최적 학습 방법 도출
    # =========================================================
    print("\n" + "=" * 64)
    print("[6] 최적 학습 방법 도출")
    print("=" * 64)
    best = treat_means.idxmax()
    worst = treat_means.idxmin()
    print(f"  처리별 평균 점수: " +
          ", ".join(f"{t}={m:.2f}" for t, m in treat_means.items()))
    if treat_sig:
        print(f"\n  → 학습 방법 간 통계적으로 유의한 차이가 있음 (p={p_treat:.4g}).")
        print(f"  → 가장 효과적인 학습 방법: '{best}' (평균 {treat_means[best]:.2f}점)")
        print(f"  → 가장 비효율적인 학습 방법: '{worst}' (평균 {treat_means[worst]:.2f}점)")
    else:
        print(f"\n  → 학습 방법 간 유의한 차이가 없어 특정 방법을 권장하기 어렵습니다.")
        print(f"  → (참고) 표본 평균상 최고: '{best}' (평균 {treat_means[best]:.2f}점)")

    print("\n분석 완료.")


if __name__ == "__main__":
    main()

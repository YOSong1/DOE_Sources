# -*- coding: utf-8 -*-
"""
페이지: 15.5 연습 문제 — 학습 방법 효과 비교 (RCBD) - Excel 활용 버전
=======================================================================
sample_data.xlsx (3 블록 × 3 처리 × 반복 2회 = 18 rows) 를 읽어
RCBD ANOVA, 블록화 효율, Tukey HSD 까지 수행한다.

1. 데이터 구조
2. RCBD ANOVA — 처리/블록 효과 유의성
3. 블록화 효율 (CRD vs RCBD MSE 비교)
4. Tukey HSD 사후 검정
5. 처리별 평균 + 95% CI 시각화
6. 최적 학습 방법 추천
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(__file__)
XLSX = os.path.join(HERE, "sample_data.xlsx")


def main() -> None:
    df = pd.read_excel(XLSX)
    print("=" * 60)
    print("[1] 데이터 구조")
    print("=" * 60)
    print(df.head(9))
    print(f"\nshape: {df.shape}")
    print("\n블록 × 처리 평균:")
    print(df.pivot_table(index="Block", columns="Treatment", values="Score", aggfunc="mean"))

    # RCBD ANOVA
    model_rcbd = ols("Score ~ C(Treatment) + C(Block)", data=df).fit()
    anova_rcbd = sm.stats.anova_lm(model_rcbd, typ=2)
    print("\n[2] RCBD ANOVA")
    print(anova_rcbd.round(4))

    sig = []
    if anova_rcbd.loc["C(Treatment)", "PR(>F)"] < 0.05:
        sig.append("Treatment")
    if anova_rcbd.loc["C(Block)", "PR(>F)"] < 0.05:
        sig.append("Block")
    print(f"\n  → p<0.05 유의 효과: {sig}")

    # 블록화 효율
    model_crd = ols("Score ~ C(Treatment)", data=df).fit()
    anova_crd = sm.stats.anova_lm(model_crd, typ=2)
    mse_rcbd = anova_rcbd.loc["Residual", "sum_sq"] / anova_rcbd.loc["Residual", "df"]
    mse_crd = anova_crd.loc["Residual", "sum_sq"] / anova_crd.loc["Residual", "df"]
    eff = mse_crd / mse_rcbd
    print("\n[3] 블록화 효율")
    print(f"  MSE_CRD  = {mse_crd:.4f}")
    print(f"  MSE_RCBD = {mse_rcbd:.4f}")
    print(f"  ε        = {eff:.3f}  ({'효과적' if eff > 1 else '미미함'})")

    # Tukey HSD
    print("\n[4] Tukey HSD")
    tukey = pairwise_tukeyhsd(df["Score"], df["Treatment"], alpha=0.05)
    print(tukey.summary())

    # 시각화
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="Treatment", y="Score", data=df, ax=ax, ci=95, palette="muted")
    ax.set_title("학습 방법별 평균 점수 (95% CI)")
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "treatment_means.png"), dpi=120)
    plt.close()

    # 최적 처리
    best = df.groupby("Treatment")["Score"].mean().idxmax()
    best_mean = df.groupby("Treatment")["Score"].mean().max()
    print(f"\n[5] 추천 학습 방법: {best}  (평균 점수 {best_mean:.2f})")


if __name__ == "__main__":
    main()

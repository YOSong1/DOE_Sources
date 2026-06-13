# -*- coding: utf-8 -*-
"""
페이지: 15.3 예제로 이해: 조미료 선호도의 난괴법 분석 - Excel 활용 버전
=========================================================================
sample_data.xlsx (4 블록 × 3 처리 = 12 rows) 를 읽어 난괴법 ANOVA 와
사후 검정 (Tukey HSD), 블록화 효율을 계산한다.

1. 데이터 구조 + 블록×처리 분포
2. RCBD ANOVA (Type II)
3. 블록화 효율: ε = MSE_RCBD / MSE_CRD (RCBD가 작을수록 효율이 높음)
4. Tukey HSD 사후 검정으로 처리 쌍별 차이 식별
5. 최적 처리 + 시각화 PNG
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
    print(df)
    print("\n블록 × 처리 cross-tab:")
    print(df.pivot_table(index="Block", columns="Treatment", values="Score"))

    # RCBD ANOVA
    model_rcbd = ols("Score ~ C(Treatment) + C(Block)", data=df).fit()
    anova_rcbd = sm.stats.anova_lm(model_rcbd, typ=2)
    print("\n[2] RCBD ANOVA")
    print(anova_rcbd.round(4))

    # 블록화 효율: CRD 모형과 비교
    model_crd = ols("Score ~ C(Treatment)", data=df).fit()
    anova_crd = sm.stats.anova_lm(model_crd, typ=2)
    mse_rcbd = anova_rcbd.loc["Residual", "sum_sq"] / anova_rcbd.loc["Residual", "df"]
    mse_crd = anova_crd.loc["Residual", "sum_sq"] / anova_crd.loc["Residual", "df"]
    efficiency = mse_crd / mse_rcbd
    print("\n[3] 블록화 효율")
    print(f"  MSE_CRD  = {mse_crd:.4f}")
    print(f"  MSE_RCBD = {mse_rcbd:.4f}")
    print(f"  Efficiency (CRD/RCBD) = {efficiency:.3f}")
    if efficiency > 1:
        print("  → 블록화가 오차 분산을 줄여 정밀도가 향상됨")
    else:
        print("  → 블록화 효과 미미. 블록 변수 재검토 권장")

    # Tukey HSD
    tukey = pairwise_tukeyhsd(endog=df["Score"], groups=df["Treatment"], alpha=0.05)
    print("\n[4] Tukey HSD 사후 검정")
    print(tukey.summary())

    # 최적 처리
    best = df.groupby("Treatment")["Score"].mean().idxmax()
    print(f"\n[5] 평균 점수 최대 처리: {best}")

    # 시각화
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    df.groupby("Treatment")["Score"].mean().plot(kind="bar", ax=axes[0], color="#3498db")
    axes[0].set_title("처리별 평균 점수")
    axes[0].set_ylabel("Mean Score")
    df.groupby("Block")["Score"].mean().plot(kind="bar", ax=axes[1], color="#e67e22")
    axes[1].set_title("블록별 평균 점수")
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "means.png"), dpi=120)
    plt.close()
    print("\n그림 저장: means.png")


if __name__ == "__main__":
    main()

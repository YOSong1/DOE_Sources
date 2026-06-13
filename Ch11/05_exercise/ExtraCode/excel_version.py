# -*- coding: utf-8 -*-
"""
페이지: 11.5 연습 문제 — 반도체 웨이퍼 공정 최적화 - Excel 활용 버전
====================================================================
sample_data.xlsx 를 읽어 표면 거칠기를 최소화하는 공정 조건을 탐색한다.

1. 데이터 구조 확인
2. 회귀 모델 적합 (주효과 + 2차 상호작용)
3. ANOVA 테이블 출력 및 유의 효과 식별
4. 효과 크기, 기여율, 최적(최소 거칠기) 조건 도출
5. 잔차 진단 그림 저장
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(__file__)
XLSX = os.path.join(HERE, "sample_data.xlsx")


def main() -> None:
    df = pd.read_excel(XLSX)

    print("=" * 60)
    print("[1] 데이터 구조")
    print("=" * 60)
    print(df.head())
    print("shape:", df.shape)

    formula = (
        "Surface_Roughness ~ Etching_Time + Plasma_Intensity + Gas_Mixture_Ratio "
        "+ Etching_Time:Plasma_Intensity + Etching_Time:Gas_Mixture_Ratio "
        "+ Plasma_Intensity:Gas_Mixture_Ratio"
    )
    model = smf.ols(formula, data=df).fit()
    anova = sm.stats.anova_lm(model, typ=2)

    print("\n[2] ANOVA 테이블")
    print(anova)

    sig = anova[anova["PR(>F)"] < 0.05].index.tolist()
    print(f"\n  → 유의한 항 (p<0.05): {sig}")

    ss_total = anova["sum_sq"].sum()
    contribution = (anova["sum_sq"] / ss_total * 100).round(2)
    print("\n[3] 기여율(%)")
    print(contribution.to_string())

    # 효과 크기 (high - low)
    print("\n[4] 주효과 크기 (high - low; 거칠기 최소화 목표)")
    for f, (lo, hi) in [
        ("Etching_Time", (15, 30)),
        ("Plasma_Intensity", (200, 300)),
        ("Gas_Mixture_Ratio", (50, 70)),
    ]:
        eff = df.loc[df[f] == hi, "Surface_Roughness"].mean() - df.loc[
            df[f] == lo, "Surface_Roughness"
        ].mean()
        direction = "→ 낮은 수준 유리" if eff > 0 else "→ 높은 수준 유리"
        print(f"  {f:20s}: {eff:+.3f}  {direction}")

    # 평균 거칠기 최소 조건
    grouped = (
        df.groupby(["Etching_Time", "Plasma_Intensity", "Gas_Mixture_Ratio"])
        ["Surface_Roughness"]
        .mean()
        .reset_index()
    )
    best = grouped.loc[grouped["Surface_Roughness"].idxmin()]
    print("\n[5] 최소 거칠기 조건 (실험점 평균 기준)")
    print(best.to_string())

    # 잔차 진단
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].scatter(model.fittedvalues, model.resid, alpha=0.7)
    axes[0].axhline(0, color="red", ls="--")
    axes[0].set_xlabel("예측값")
    axes[0].set_ylabel("잔차")
    axes[0].set_title("잔차 vs 예측값")
    sm.qqplot(model.resid, line="s", ax=axes[1])
    axes[1].set_title("Q-Q Plot")
    plt.tight_layout()
    out = os.path.join(HERE, "diagnostic.png")
    plt.savefig(out, dpi=120)
    print(f"\n잔차 진단 저장: {out}")


if __name__ == "__main__":
    main()

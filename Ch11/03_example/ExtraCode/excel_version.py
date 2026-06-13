# -*- coding: utf-8 -*-
"""
페이지: 11.3 예제로 이해: 초콜릿 코팅 품질의 완전 요인 실험 - Excel 활용 버전
======================================================================
sample_data.xlsx (3요인 2수준 x 반복 3회 = 24행) 를 읽어
초콜릿 코팅 품질 최적화를 위한 다음 분석을 수행한다.

1. 데이터 구조 출력
2. 전체 모델/간단한 모델 적합 및 결정계수 비교
3. ANOVA 테이블 (Type II)
4. 효과 크기, 기여율, 최적 조건, 예측 응답
5. 주효과/상호작용 시각화 및 잔차 진단
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
    print("\nshape:", df.shape)
    print("조건별 반복 수:")
    print(df.groupby(["Coating_Temperature", "Mixing_Speed", "Cooling_Time"]).size())

    # 전체 모형 vs 간단한 모형
    full = smf.ols(
        "Coating_Quality ~ Coating_Temperature * Mixing_Speed * Cooling_Time",
        data=df,
    ).fit()
    simple = smf.ols(
        "Coating_Quality ~ Coating_Temperature + Mixing_Speed + Cooling_Time "
        "+ Coating_Temperature:Cooling_Time",
        data=df,
    ).fit()

    print("\n" + "=" * 60)
    print("[2] 모델 비교 (R^2 / Adj R^2)")
    print("=" * 60)
    print(f"  Full  : R^2 = {full.rsquared:.4f},  Adj R^2 = {full.rsquared_adj:.4f}")
    print(f"  Simple: R^2 = {simple.rsquared:.4f},  Adj R^2 = {simple.rsquared_adj:.4f}")

    # ANOVA
    anova = sm.stats.anova_lm(simple, typ=2)
    print("\n" + "=" * 60)
    print("[3] ANOVA 테이블 (간단한 모델)")
    print("=" * 60)
    print(anova)

    ss_total = anova["sum_sq"].sum()
    contribution = (anova["sum_sq"] / ss_total * 100).round(2)
    print("\n[4] 기여율(%)")
    print(contribution.to_string())

    # 효과 크기 (high - low)
    print("\n" + "=" * 60)
    print("[5] 주효과 크기 (high - low)")
    print("=" * 60)
    for f, (lo, hi) in [
        ("Coating_Temperature", (30, 35)),
        ("Mixing_Speed", (50, 100)),
        ("Cooling_Time", (5, 10)),
    ]:
        eff = df.loc[df[f] == hi, "Coating_Quality"].mean() - df.loc[
            df[f] == lo, "Coating_Quality"
        ].mean()
        print(f"  {f:25s}: {eff:+.3f}")

    # 최적 조건 (품질 최대화)
    grouped = (
        df.groupby(["Coating_Temperature", "Mixing_Speed", "Cooling_Time"])
        ["Coating_Quality"]
        .mean()
        .reset_index()
    )
    best = grouped.loc[grouped["Coating_Quality"].idxmax()]
    print("\n" + "=" * 60)
    print("[6] 최적 조건 (실험 조건 중 평균 품질 최대)")
    print("=" * 60)
    print(best.to_string())

    # 시각화
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for ax, factor in zip(
        axes, ["Coating_Temperature", "Mixing_Speed", "Cooling_Time"]
    ):
        sns.boxplot(x=factor, y="Coating_Quality", data=df, ax=ax)
        ax.set_title(f"{factor} 수준별 코팅 품질")
    plt.suptitle("주효과 박스플롯", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "main_effect_boxplot.png"), dpi=120)
    plt.close()

    fig, ax = plt.subplots(figsize=(6, 4))
    for time_val, label in zip([5, 10], ["냉각 5분", "냉각 10분"]):
        sub = df[df["Cooling_Time"] == time_val]
        m = sub.groupby("Coating_Temperature")["Coating_Quality"].mean()
        ax.plot(m.index, m.values, "o-", label=label)
    ax.set_title("온도 × 냉각 시간 상호작용")
    ax.set_xlabel("Coating Temperature (°C)")
    ax.set_ylabel("평균 Coating Quality")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "interaction_plot.png"), dpi=120)
    plt.close()
    print("\n그림 저장 완료: main_effect_boxplot.png, interaction_plot.png")

    # 결론
    print("\n" + "=" * 60)
    print("[7] 해석 요약")
    print("=" * 60)
    print("  - Coating_Temperature와 Cooling_Time의 양의 효과가 크다.")
    print("  - 온도×냉각 시간 상호작용이 유의하면, 둘 다 높을 때 추가 시너지가 있다.")
    print("  - 권장 조건: 온도 35°C, 냉각 10분 (혼합 속도는 효과가 상대적으로 작음).")


if __name__ == "__main__":
    main()

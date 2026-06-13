# -*- coding: utf-8 -*-
"""
페이지: 11.2 완전 요인 실험의 절차 - Excel 활용 버전
====================================================
sample_data.xlsx (2^3 완전 요인 설계, 반복 2회) 를 읽어
주효과와 2차 상호작용을 포함한 ANOVA 분석을 수행한다.

- 데이터 구조 확인
- ANOVA 테이블 출력 (Type II SS)
- 각 효과의 절대 크기와 기여율 계산
- 최적 조건과 예측 응답 도출
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

XLSX = os.path.join(os.path.dirname(__file__), "sample_data.xlsx")


def main() -> None:
    df = pd.read_excel(XLSX)
    print("=" * 60)
    print("[1] 데이터 구조")
    print("=" * 60)
    print(df.head())
    print(f"\nshape : {df.shape}")
    print(f"factors levels:\n{df[['A','B','C']].apply(pd.unique).to_dict()}")

    # 2차 상호작용까지 포함한 모형
    model = ols("y ~ A + B + C + A:B + A:C + B:C", data=df).fit()
    anova = sm.stats.anova_lm(model, typ=2)

    print("\n" + "=" * 60)
    print("[2] ANOVA 테이블 (Type II)")
    print("=" * 60)
    print(anova)

    # 효과 크기 (high - low) 와 기여율 계산
    print("\n" + "=" * 60)
    print("[3] 주효과 및 상호작용 효과 크기")
    print("=" * 60)
    effects = {}
    for f in ["A", "B", "C"]:
        eff = df.loc[df[f] == 1, "y"].mean() - df.loc[df[f] == -1, "y"].mean()
        effects[f] = eff
    for f1, f2 in [("A", "B"), ("A", "C"), ("B", "C")]:
        eff = (
            df.loc[df[f1] * df[f2] == 1, "y"].mean()
            - df.loc[df[f1] * df[f2] == -1, "y"].mean()
        )
        effects[f"{f1}:{f2}"] = eff

    eff_df = pd.DataFrame(
        {"Effect": effects, "|Effect|": {k: abs(v) for k, v in effects.items()}}
    ).sort_values("|Effect|", ascending=False)
    print(eff_df)

    # 기여율
    ss_total = anova["sum_sq"].sum()
    contribution = (anova["sum_sq"] / ss_total * 100).round(2)
    print("\n[4] 기여율(%)")
    print(contribution.to_string())

    # 최적 조건: 효과가 양이면 +1, 음이면 -1
    print("\n" + "=" * 60)
    print("[5] 최대화 기준 최적 조건")
    print("=" * 60)
    optimum = {f: int(np.sign(effects[f])) for f in ["A", "B", "C"]}
    print(f"  → {optimum}")
    pred = model.predict(pd.DataFrame([optimum]))
    print(f"  예측 응답값(평균): {pred.values[0]:.3f}")

    # 시각화
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
    for ax, f in zip(axes, ["A", "B", "C"]):
        means = df.groupby(f)["y"].mean()
        ax.plot(means.index, means.values, "o-", lw=2)
        ax.set_title(f"주효과: {f}")
        ax.set_xlabel(f"{f} 수준")
        ax.set_xticks([-1, 1])
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("평균 y")
    plt.tight_layout()
    out = os.path.join(os.path.dirname(__file__), "main_effects.png")
    plt.savefig(out, dpi=120)
    print(f"\n그림 저장: {out}")


if __name__ == "__main__":
    main()

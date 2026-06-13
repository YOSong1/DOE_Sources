# -*- coding: utf-8 -*-
"""
페이지: 12.5 연습 문제 — 플라스틱 사출 성형 - Excel 활용 버전
================================================================
sample_data.xlsx (2^(6-2) IV, 16 runs) 를 읽어 인장 강도를 최대화하는
핵심 요인을 스크리닝한다.

1. Generator 검증 (E = A*B*C, F = B*C*D)
2. 주효과 계산 및 |Effect| 순 정렬
3. ANOVA (주효과만 — Resolution IV는 2차 상호작용 끼리 교락)
4. 기여율과 핵심 요인 식별
5. 최대화 최적 조건
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(__file__)
XLSX = os.path.join(HERE, "sample_data.xlsx")
FACTORS = ["A", "B", "C", "D", "E", "F"]


def main() -> None:
    df = pd.read_excel(XLSX)

    print("=" * 60)
    print("[1] 데이터 + Generator 검증")
    print("=" * 60)
    print(df)
    ok_E = (df["E"] == df["A"] * df["B"] * df["C"]).all()
    ok_F = (df["F"] == df["B"] * df["C"] * df["D"]).all()
    print(f"\n  E = A*B*C 검증: {ok_E}")
    print(f"  F = B*C*D 검증: {ok_F}")

    print("\n[2] 주효과 (high - low) — 절대값 큰 순")
    effects = {}
    for f in FACTORS:
        eff = df.loc[df[f] == 1, "Tensile_Strength"].mean() - df.loc[
            df[f] == -1, "Tensile_Strength"
        ].mean()
        effects[f] = eff
    eff_df = (
        pd.DataFrame({"Effect": effects})
        .assign(absEffect=lambda x: x["Effect"].abs())
        .sort_values("absEffect", ascending=False)
    )
    print(eff_df.round(3))

    # 회귀 (주효과만)
    model = ols("Tensile_Strength ~ A + B + C + D + E + F", data=df).fit()
    anova = sm.stats.anova_lm(model, typ=2)

    print("\n[3] ANOVA (주효과만)")
    print(anova.round(4))

    sig = anova[anova["PR(>F)"] < 0.05].index.tolist()
    print(f"\n  → 유의 요인 (p<0.05): {sig}")

    ss_total = anova["sum_sq"].sum()
    contrib = (anova["sum_sq"] / ss_total * 100).round(2)
    print("\n[4] 기여율(%)")
    print(contrib.sort_values(ascending=False).to_string())

    # 핵심 요인 (top 3)
    top3 = eff_df.head(3).index.tolist()
    print(f"\n[5] 스크리닝 결과 — 핵심 요인 Top 3: {top3}")
    print("  다음 단계: 이 요인들에 대해 완전 요인 실험 또는 RSM 적용 권장")

    # 최적 조건
    optimum = {f: int(np.sign(effects[f])) for f in FACTORS}
    pred = model.predict(pd.DataFrame([optimum]))
    print("\n[6] 인장 강도 최대화 조건 (효과 부호 기반)")
    print(f"  {optimum}")
    print(f"  예측 인장 강도: {pred.values[0]:.3f} MPa")

    # 파레토 차트
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(eff_df.index, eff_df["absEffect"], color="#3498db")
    ax.set_xlabel("|Effect| (MPa)")
    ax.set_title("주효과 파레토 차트")
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "pareto.png"), dpi=120)
    plt.close()
    print("\n파레토 차트 저장: pareto.png")


if __name__ == "__main__":
    main()

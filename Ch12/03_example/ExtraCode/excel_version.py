# -*- coding: utf-8 -*-
"""
페이지: 12.3 예제로 이해: 반도체 식각 공정의 부분 요인 실험 - Excel 활용 버전
=============================================================================
sample_data.xlsx 를 읽어 2^(5-2) Resolution III 부분 요인 분석을 수행한다.

1. 코딩 행렬과 실제 단위 열 구조 확인
2. 주효과 계산
3. 회귀 모형 적합 + ANOVA + 회귀계수 (효과/2)
4. 파레토 차트 PNG 저장
5. 교락 구조 출력
6. 최적 조건과 예측 식각률
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
FACTORS = ["A", "B", "C", "D", "E"]


def main() -> None:
    df = pd.read_excel(XLSX)
    print("=" * 60)
    print("[1] 데이터 구조 (코딩 + 실제 단위)")
    print("=" * 60)
    print(df)

    # Generator 검증: D == A*B, E == A*C
    ok_D = (df["D"] == df["A"] * df["B"]).all()
    ok_E = (df["E"] == df["A"] * df["C"]).all()
    print(f"\n  Generator 검증: D = A*B → {ok_D},  E = A*C → {ok_E}")

    # 주효과
    print("\n[2] 주효과 (high - low)")
    effects = {}
    for f in FACTORS:
        eff = df.loc[df[f] == 1.0, "Etch_Rate"].mean() - df.loc[
            df[f] == -1.0, "Etch_Rate"
        ].mean()
        effects[f] = eff
        print(f"  {f}: {eff:+.2f} nm/min")

    # 회귀 모형
    model = ols("Etch_Rate ~ A + B + C + D + E", data=df).fit()
    anova = sm.stats.anova_lm(model, typ=2)

    print("\n[3] ANOVA")
    print(anova)

    print("\n[4] 회귀 계수 (= 효과/2)")
    coefs = model.params.drop("Intercept", errors="ignore")
    pvals = model.pvalues.drop("Intercept", errors="ignore")
    summary = pd.DataFrame(
        {"Effect": [effects[f] for f in FACTORS], "Coef": coefs.values, "p-value": pvals.values},
        index=FACTORS,
    )
    print(summary.round(4))

    # 파레토 차트
    eff_abs = {k: abs(v) for k, v in effects.items()}
    sorted_eff = dict(sorted(eff_abs.items(), key=lambda x: x[1], reverse=True))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(
        list(sorted_eff.keys()),
        list(sorted_eff.values()),
        color=["#e74c3c" if v > 30 else "#3498db" for v in sorted_eff.values()],
    )
    ax.set_xlabel("|Effect|")
    ax.set_title("파레토 차트")
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "pareto.png"), dpi=120)
    plt.close()
    print("\n파레토 차트 저장: pareto.png")

    # 교락 구조
    print("\n[5] 교락 구조 (I = ABD = ACE = BCDE)")
    aliases = {
        "A": ["A", "BD", "CE"],
        "B": ["B", "AD", "ABCE", "CDE"],
        "C": ["C", "AE", "ABCD", "BDE"],
        "D": ["D", "AB", "ACDE", "BCE"],
        "E": ["E", "AC", "ABDE", "BCD"],
    }
    for k, v in aliases.items():
        print(f"  {' = '.join(v)}")

    # 최적 조건
    optimum = {f: int(np.sign(effects[f])) for f in FACTORS}
    pred = model.predict(pd.DataFrame([{f: optimum[f] for f in FACTORS}]))
    print("\n[6] 최적 조건 (식각률 최대화)")
    for f in FACTORS:
        print(f"  {f}: {'+1' if optimum[f] > 0 else '-1'}")
    print(f"  예측 식각률: {pred.values[0]:.2f} nm/min")


if __name__ == "__main__":
    main()

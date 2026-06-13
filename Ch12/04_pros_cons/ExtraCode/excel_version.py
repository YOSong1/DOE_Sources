# -*- coding: utf-8 -*-
"""
페이지: 12.4 부분 요인 실험의 장단점 및 활용 - Excel 활용 버전
================================================================
sample_data.xlsx (2^(5-1) Resolution V 설계, 16 runs, Generator E=ABCD) 를
읽어 Resolution V의 장점인 \"주효과·2차 상호작용 모두 추정 가능\" 을 실증한다.

1. Generator 검증 (E = A*B*C*D)
2. 주효과 + 모든 2차 상호작용 모형 적합
3. ANOVA 및 회귀 계수 출력
4. 효과 크기, 기여율, 최적 조건
"""

import os
import itertools

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

HERE = os.path.dirname(__file__)
XLSX = os.path.join(HERE, "sample_data.xlsx")
FACTORS = ["A", "B", "C", "D", "E"]


def main() -> None:
    df = pd.read_excel(XLSX)

    print("=" * 60)
    print("[1] 데이터 + Generator 검증 (E = A*B*C*D)")
    print("=" * 60)
    print(df)
    ok = (df["E"] == df["A"] * df["B"] * df["C"] * df["D"]).all()
    print(f"\n  검증: {ok}")

    # Resolution V 설계는 주효과 + 모든 2차 상호작용을 모두 추정 가능 (16 obs, 16 params → saturated).
    # 본 분석에서는 주효과만 모형에 포함해 잔차를 확보하고, 2차 상호작용은 별도로 효과 크기로 보여준다.
    model = ols("y ~ " + " + ".join(FACTORS), data=df).fit()
    anova = sm.stats.anova_lm(model, typ=2)

    print("\n[2] ANOVA (주효과만, 잔차 확보)")
    print(anova.round(4))

    sig = anova[anova["PR(>F)"] < 0.05].index.tolist()
    print(f"\n  → 유의 주효과 (p<0.05): {sig}")

    # 2차 상호작용 효과 크기 (모두 계산)
    print("\n[2b] 2차 상호작용 효과 크기 (high - low)")
    for a, b in itertools.combinations(FACTORS, 2):
        prod = df[a] * df[b]
        eff = df.loc[prod == 1, "y"].mean() - df.loc[prod == -1, "y"].mean()
        print(f"  {a}:{b}  effect = {eff:+.3f}")

    print("\n[3] 주효과 크기 (high - low)")
    effects = {}
    for f in FACTORS:
        eff = df.loc[df[f] == 1, "y"].mean() - df.loc[df[f] == -1, "y"].mean()
        effects[f] = eff
        print(f"  {f}: {eff:+.3f}")

    ss_total = anova["sum_sq"].sum()
    contrib = (anova["sum_sq"] / ss_total * 100).round(2)
    print("\n[4] 기여율(%) 상위 5개")
    print(contrib.sort_values(ascending=False).head(5).to_string())

    # 최적 조건
    print("\n[5] 응답 최대화 최적 조건")
    optimum = {f: int(np.sign(effects[f])) for f in FACTORS}
    print(f"  {optimum}")


if __name__ == "__main__":
    main()

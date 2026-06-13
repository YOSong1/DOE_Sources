# -*- coding: utf-8 -*-
"""
페이지: 12.2 부분 요인 실험의 절차 - Excel 활용 버전
====================================================
sample_data.xlsx (2^(4-1), Generator D=ABC, 8 runs) 를 읽어
주효과와 일부 2차 상호작용에 대한 분석을 수행한다.

1. 데이터 구조 확인 및 D=ABC 검증
2. 회귀 모형 적합 + ANOVA
3. 각 효과의 크기와 기여율
4. 교락 구조(별칭) 표시
5. 최적 조건 도출
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


def main() -> None:
    df = pd.read_excel(XLSX)

    print("=" * 60)
    print("[1] 데이터 구조 + 직교성 검증")
    print("=" * 60)
    print(df)
    # D == A*B*C ?
    ok = (df["D"] == df["A"] * df["B"] * df["C"]).all()
    print(f"\n  Generator 검증 (D = A*B*C): {ok}")

    model = ols("y ~ A + B + C + D + A:B + A:C", data=df).fit()
    anova = sm.stats.anova_lm(model, typ=2)

    print("\n[2] ANOVA (주효과 + A:B, A:C)")
    print(anova)

    # 효과 크기
    print("\n[3] 효과 크기 (high - low)")
    effects = {}
    for col in ["A", "B", "C", "D"]:
        eff = df.loc[df[col] == 1, "y"].mean() - df.loc[df[col] == -1, "y"].mean()
        effects[col] = eff
        print(f"  {col}: {eff:+.3f}")

    # 기여율
    ss_total = anova["sum_sq"].sum()
    print("\n[4] 기여율(%)")
    print((anova["sum_sq"] / ss_total * 100).round(2).to_string())

    print("\n[5] 별칭 구조 (I = ABCD)")
    print("  A ↔ BCD")
    print("  B ↔ ACD")
    print("  C ↔ ABD")
    print("  D ↔ ABC")
    print("  AB ↔ CD")
    print("  AC ↔ BD")
    print("  AD ↔ BC")

    # 최적 조건 (응답 최대화 가정)
    optimum = {col: int(np.sign(effects[col])) for col in ["A", "B", "C", "D"]}
    pred = model.predict(pd.DataFrame([optimum]))
    print("\n[6] 응답 최대화 최적 조건")
    print(f"  {optimum}")
    print(f"  예측 응답: {pred.values[0]:.3f}")


if __name__ == "__main__":
    main()

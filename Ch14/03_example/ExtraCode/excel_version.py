# -*- coding: utf-8 -*-
"""
페이지: 14.3 예제로 이해: 온도·압력·시간의 L9 직교배열 최적화 - Excel 활용 버전
==================================================================================
sample_data.xlsx (L9 x 반복 3회 = 27 rows) 를 읽어 망대특성 S/N비를 계산하고,
인자별 주효과·기여율을 분석하여 최적 조건을 도출한다.

1. 데이터 구조 출력
2. 각 Run 별 평균/표준편차/S/N(망대) 계산
3. 인자별 평균 S/N (주효과)
4. ANOVA on S/N (각 인자의 기여율)
5. 최적 조건 예측 + 시각화 PNG 저장
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


def sn_larger(y: np.ndarray) -> float:
    return -10.0 * np.log10(np.mean(1.0 / (y ** 2)))


def main() -> None:
    df = pd.read_excel(XLSX)
    print("=" * 60)
    print("[1] 원시 데이터 (L9 × 반복 3회)")
    print("=" * 60)
    print(df.head(9))
    print(f"\n총 행수: {len(df)}")

    # Run 단위로 집계: 평균, 표준편차, S/N
    summary = (
        df.groupby(["Run", "A_Temp", "B_Pressure", "C_Time"])
        .agg(
            Mean=("Response", "mean"),
            Std=("Response", "std"),
            SN=("Response", lambda x: sn_larger(np.asarray(x))),
        )
        .reset_index()
    )
    print("\n[2] Run 별 평균/표준편차/S/N (망대특성)")
    print(summary.round(4))

    # 인자별 평균 S/N
    print("\n[3] 인자별 평균 S/N")
    for f in ["A_Temp", "B_Pressure", "C_Time"]:
        means = summary.groupby(f)["SN"].mean()
        print(f"\n  {f}:")
        print(means.round(4))

    # ANOVA: S/N ~ A + B + C  (요인을 범주형 처리)
    model = ols("SN ~ C(A_Temp) + C(B_Pressure) + C(C_Time)", data=summary).fit()
    anova = sm.stats.anova_lm(model, typ=2)
    ss_total = anova["sum_sq"].sum()
    anova["contribution(%)"] = (anova["sum_sq"] / ss_total * 100).round(2)
    print("\n[4] ANOVA on S/N - 기여율(%)")
    print(anova.round(4))

    # 최적 수준 = 평균 S/N 최대 수준
    optimum = {}
    for f in ["A_Temp", "B_Pressure", "C_Time"]:
        m = summary.groupby(f)["SN"].mean()
        optimum[f] = int(m.idxmax())
    print("\n[5] 최적 조건 (S/N 최대화)")
    for k, v in optimum.items():
        print(f"  {k} = {v}")

    # 시각화
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
    titles = {
        "A_Temp": "온도 (°C)",
        "B_Pressure": "압력 (bar)",
        "C_Time": "시간 (min)",
    }
    for ax, f in zip(axes, ["A_Temp", "B_Pressure", "C_Time"]):
        m = summary.groupby(f)["SN"].mean()
        ax.plot(m.index, m.values, "o-", lw=2)
        ax.set_xlabel(titles[f])
        ax.set_title(f"{f} 주효과 (S/N)")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("평균 S/N")
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "main_effects_sn.png"), dpi=120)
    plt.close()
    print("\n시각화 저장: main_effects_sn.png")


if __name__ == "__main__":
    main()

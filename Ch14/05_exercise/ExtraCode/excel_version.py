# -*- coding: utf-8 -*-
"""
페이지: 14.5 연습 문제 — 엔진 파라미터 최적화 - Excel 활용 버전
================================================================
sample_data.xlsx (L9, 9 runs) 를 읽어 망대특성 S/N비를 계산하고,
연비 최대화에 가장 유리한 점화 시점/연료 분사압/공기흡입량 조합을 도출한다.

1. 데이터 구조 확인
2. 망대특성 S/N비 계산 (단일 측정 가정: n=1)
3. 인자별 평균 S/N + 평균 연비 비교
4. S/N 최대화 vs 평균 최대화 — 두 기준의 최적 조건
5. 주효과도 PNG 저장
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(__file__)
XLSX = os.path.join(HERE, "sample_data.xlsx")

FACTORS = ["Ignition_Timing", "Fuel_Pressure", "Air_Intake"]


def sn_larger(y: float) -> float:
    return -10.0 * np.log10(1.0 / (y ** 2))


def main() -> None:
    df = pd.read_excel(XLSX)

    print("=" * 60)
    print("[1] L9 실험 데이터")
    print("=" * 60)
    print(df)

    df["SN"] = df["Fuel_Efficiency"].apply(sn_larger)
    print("\n[2] 망대특성 S/N (n=1)")
    print(df[["Run", *FACTORS, "Fuel_Efficiency", "SN"]].round(4))

    # 인자별 평균 비교
    print("\n[3] 인자별 평균 S/N & 평균 연비")
    for f in FACTORS:
        agg = df.groupby(f).agg(SN_mean=("SN", "mean"), FE_mean=("Fuel_Efficiency", "mean"))
        print(f"\n  {f}")
        print(agg.round(4))

    # 최적 조건 (S/N 기준 / 평균 기준)
    optimum_sn = {f: int(df.groupby(f)["SN"].mean().idxmax()) for f in FACTORS}
    optimum_mean = {
        f: int(df.groupby(f)["Fuel_Efficiency"].mean().idxmax()) for f in FACTORS
    }
    print("\n[4] 최적 조건")
    print(f"  S/N 최대화  : {optimum_sn}")
    print(f"  평균 최대화 : {optimum_mean}")

    # 시각화
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
    titles = {
        "Ignition_Timing": "점화 시점 (BTDC)",
        "Fuel_Pressure": "연료 분사압 (bar)",
        "Air_Intake": "공기흡입량 (L/min)",
    }
    for ax, f in zip(axes, FACTORS):
        m = df.groupby(f)["SN"].mean()
        ax.plot(m.index, m.values, "o-", lw=2)
        ax.set_xlabel(titles[f])
        ax.set_title(f"{f} 평균 S/N")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("평균 S/N")
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "sn_effects.png"), dpi=120)
    plt.close()
    print("\nS/N 주효과도 저장: sn_effects.png")


if __name__ == "__main__":
    main()

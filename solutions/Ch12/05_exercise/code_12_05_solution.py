# code_12_05_solution.py
# -*- coding: utf-8 -*-
"""
페이지: 12.5 연습 문제 - 문제 1 해답 (플라스틱 사출 성형 공정 스크리닝)
================================================================
6요인 2수준 부분 요인 실험 2^(6-2) Resolution IV (16 runs) 설계로
인장 강도(Tensile Strength, MPa)를 최대화하는 핵심 요인을 스크리닝한다.

본 스크립트는 자기완결형이다. 문제 본문이 제공하는 데이터 생성 코드
(seed=7)를 그대로 포함하여 그 데이터로 직접 분석하며, 외부 xlsx 파일을
읽지 않는다.

수행 단계:
  [1] 설계 행렬 생성 및 총 실험 횟수 확인          (요구사항 1)
  [2] 교락(Aliasing) 구조 분석 - 생성 함수/별칭 구조 (요구사항 2)
  [3] 데이터 결합 후 주효과 추정 -> 핵심 요인 2~3개 선별 (요구사항 3)
  [4] statsmodels ANOVA로 유의수준 0.05 유의 효과 식별
  [5] 효과 시각화(파레토/주효과) + 잔차 진단
  [6] 인장 강도 최대화(목표 방향) 최적 조건 도출 및 출력
  [7] 다음 단계 실험 설계 제안                      (요구사항 4)
"""

import os
import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from pyDOE3 import fracfact

# ----------------------------------------------------------------------
# 시각화 설정 (matplotlib 전용, seaborn 미사용)
# ----------------------------------------------------------------------
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
FACTORS = ["A", "B", "C", "D", "E", "F"]
ALPHA = 0.05


def build_data():
    """문제 본문 제공 데이터 생성 코드 (seed=7) - 그대로 사용."""
    # Resolution IV 설계: 2^(6-2) = 16회
    # 생성 함수(Generator): E = ABC, F = BCD
    design = fracfact("a b c d abc bcd")
    np.random.seed(7)

    # 가상 인장 강도 데이터 (MPa) - A와 C의 주효과가 크도록 설정
    tensile = (
        45
        + 5 * design[:, 0]    # A (용융 온도)
        + 1 * design[:, 1]    # B (사출 압력)
        + 4 * design[:, 2]    # C (냉각 시간)
        + 0.5 * design[:, 3]  # D (게이트 크기)
        + 1.5 * design[:, 4]  # E (사출 속도)
        - 2 * design[:, 5]    # F (수분 함량)
        + np.random.normal(0, 0.8, 16)
    )

    df = pd.DataFrame(design, columns=FACTORS)
    df["Tensile_Strength"] = tensile
    return df


def main():
    df = build_data()

    # ------------------------------------------------------------------
    # [1] 설계 행렬 + 총 실험 횟수
    # ------------------------------------------------------------------
    print("=" * 64)
    print("[1] 2^(6-2) Resolution IV 부분 요인 설계 (Generator: E=ABC, F=BCD)")
    print("=" * 64)
    print(df.round(3).to_string(index=False))
    print(f"\n  총 실험 횟수(runs): {len(df)}  (완전 요인 2^6 = 64회 대비 1/4)")
    print(f"  요인 수: {len(FACTORS)}개, 수준: 각 2수준(-1 / +1)")

    # 생성 함수 검증: E = A*B*C, F = B*C*D
    ok_E = bool((df["E"] == df["A"] * df["B"] * df["C"]).all())
    ok_F = bool((df["F"] == df["B"] * df["C"] * df["D"]).all())
    print(f"\n  생성 함수 검증  E = A-B-C : {ok_E}")
    print(f"  생성 함수 검증  F = B-C-D : {ok_F}")

    # ------------------------------------------------------------------
    # [2] 교락(Aliasing) 구조 분석
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[2] 교락(Aliasing) 구조 - 주효과와 2차 상호작용의 별칭(alias)")
    print("=" * 64)
    print("  정의 관계(Defining Relation): I = ABCE = BCDF = ADEF")
    print("  (E=ABC -> ABCE=I,  F=BCD -> BCDF=I,  곱 ABCE-BCDF = ADEF)")
    print("  -> 분해능(Resolution) IV: 최단 단어 길이 4")
    print("    - 주효과 <-> 2차 상호작용은 서로 교락되지 않음(주효과 추정 깨끗)")
    print("    - 단, 2차 상호작용끼리는 서로 교락됨\n")

    # 정의 관계로 2차 상호작용의 별칭 쌍을 계산해 출력
    cols = {f: df[f].to_numpy() for f in FACTORS}
    two_factor = list(itertools.combinations(FACTORS, 2))
    seen = set()
    print("  [2차 상호작용 교락 쌍] (같은 열 패턴 = 서로 교락)")
    for i, (a, b) in enumerate(two_factor):
        if (a, b) in seen:
            continue
        sig_ab = cols[a] * cols[b]
        aliases = []
        for (c, d) in two_factor[i + 1:]:
            if np.array_equal(sig_ab, cols[c] * cols[d]):
                aliases.append(c + d)
                seen.add((c, d))
        if aliases:
            print(f"    {a}{b} = " + " = ".join(aliases))
    print("\n  해석: 위 쌍들은 동일한 대비(contrast)를 공유하므로, 만약")
    print("        2차 상호작용이 유의하게 나타나면 어느 쌍의 효과인지")
    print("        단독으로 분리할 수 없다(추가 실험 또는 사전지식 필요).")

    # ------------------------------------------------------------------
    # [3] 주효과 추정 -> 핵심 요인 선별
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[3] 주효과(Main Effect = 高수준평균 - 低수준평균) 추정")
    print("=" * 64)
    effects = {}
    for f in FACTORS:
        hi = df.loc[df[f] == 1, "Tensile_Strength"].mean()
        lo = df.loc[df[f] == -1, "Tensile_Strength"].mean()
        effects[f] = hi - lo
    eff_df = (
        pd.DataFrame({"Effect": effects})
        .assign(abs_Effect=lambda x: x["Effect"].abs())
        .sort_values("abs_Effect", ascending=False)
    )
    print(eff_df.round(3).to_string())

    top_factors = eff_df.head(3).index.tolist()
    print(f"\n  -> |효과| 상위 핵심 요인 Top 3: {top_factors}")
    print("  (설계 시 A-C가 가장 크고 F가 그 다음이 되도록 데이터를 구성)")

    # ------------------------------------------------------------------
    # [4] statsmodels ANOVA - 유의수준 0.05 유의 효과 식별
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[4] ANOVA (주효과 모형) - 유의수준 α = 0.05")
    print("=" * 64)
    print("  Resolution IV에서 주효과는 2차 상호작용과 교락되지 않으므로")
    print("  주효과만으로 모형을 적합한다(완전 포화 모형, 잔차 자유도=9).\n")

    model = ols("Tensile_Strength ~ A + B + C + D + E + F", data=df).fit()
    anova = sm.stats.anova_lm(model, typ=2)
    print(anova.round(4).to_string())

    sig = anova.loc[anova["PR(>F)"] < ALPHA].index.tolist()
    sig = [s for s in sig if s != "Residual"]
    print(f"\n  -> 유의 효과 (p < {ALPHA}): {sig}")

    ss_total = anova["sum_sq"].sum()
    contrib = (anova["sum_sq"] / ss_total * 100).round(2)
    print("\n  [기여율(%) - 내림차순]")
    print(contrib.drop(labels=["Residual"]).sort_values(ascending=False).to_string())

    # ------------------------------------------------------------------
    # [5] 시각화 - 파레토 + 주효과 플롯 + 잔차 진단
    # ------------------------------------------------------------------
    png_effects = os.path.join(HERE, "code_12_05_solution_effects.png")
    png_resid = os.path.join(HERE, "code_12_05_solution_residuals.png")

    # (5-1) 효과 시각화: 파레토 차트 + 주효과 플롯
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # 파레토 차트 (|Effect|, 유의 요인 강조)
    colors = ["#e74c3c" if f in sig else "#95a5a6" for f in eff_df.index]
    axes[0].barh(eff_df.index[::-1], eff_df["abs_Effect"][::-1],
                 color=colors[::-1], edgecolor="black")
    axes[0].set_xlabel("|주효과| (MPa)")
    axes[0].set_title("주효과 파레토 차트 (붉은색 = p<0.05 유의)")
    axes[0].grid(axis="x", alpha=0.3)

    # 주효과 플롯 (각 요인 저/고 수준의 평균 반응)
    grand = df["Tensile_Strength"].mean()
    for f in FACTORS:
        lo = df.loc[df[f] == -1, "Tensile_Strength"].mean()
        hi = df.loc[df[f] == 1, "Tensile_Strength"].mean()
        axes[1].plot([f + "\n(-)", f + "\n(+)"], [lo, hi],
                     marker="o", label=f)
    axes[1].axhline(grand, color="gray", linestyle="--", alpha=0.6,
                    label="전체 평균")
    axes[1].set_ylabel("평균 인장 강도 (MPa)")
    axes[1].set_title("주효과 플롯 (기울기 클수록 영향 큼)")
    axes[1].legend(fontsize=8, ncol=2)
    axes[1].grid(alpha=0.3)

    fig.suptitle("플라스틱 사출 성형 스크리닝 - 효과 분석", fontsize=14)
    plt.tight_layout()
    plt.savefig(png_effects, dpi=120)
    plt.close()

    # (5-2) 잔차 진단: 잔차 vs 적합값, 정규 Q-Q
    resid = model.resid
    fitted = model.fittedvalues

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(fitted, resid, color="#2980b9", edgecolor="black")
    axes[0].axhline(0, color="red", linestyle="--")
    axes[0].set_xlabel("적합값 (Fitted)")
    axes[0].set_ylabel("잔차 (Residual)")
    axes[0].set_title("잔차 vs 적합값")
    axes[0].grid(alpha=0.3)

    sm.qqplot(resid, line="s", ax=axes[1])
    axes[1].set_title("정규 Q-Q 플롯")
    axes[1].grid(alpha=0.3)

    fig.suptitle("잔차 진단 (모형 가정 점검)", fontsize=14)
    plt.tight_layout()
    plt.savefig(png_resid, dpi=120)
    plt.close()

    print(f"\n  효과 시각화 저장: {os.path.basename(png_effects)}")
    print(f"  잔차 진단 저장 : {os.path.basename(png_resid)}")

    # ------------------------------------------------------------------
    # [6] 인장 강도 '최대화' 최적 조건 도출
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[6] 인장 강도 최대화(목표 방향) 최적 조건")
    print("=" * 64)
    print("  각 요인을 효과 부호 방향으로 설정하면 반응을 최대화한다")
    print("  (효과 > 0 이면 고수준 +1, 효과 < 0 이면 저수준 -1).\n")

    level_label = {
        "A": ("220 °C", "250 °C"),
        "B": ("80 bar", "120 bar"),
        "C": ("10 s", "20 s"),
        "D": ("2 mm", "4 mm"),
        "E": ("50 mm/s", "100 mm/s"),
        "F": ("0.1 %", "0.3 %"),
    }
    optimum = {f: int(np.sign(effects[f])) for f in FACTORS}
    print("  최적 설정 (코드수준 / 실제값):")
    for f in FACTORS:
        lv = optimum[f]
        actual = level_label[f][1] if lv == 1 else level_label[f][0]
        mark = "  ← 유의" if f in sig else ""
        print(f"    {f}: {lv:+d}  ({actual}){mark}")

    pred = model.predict(pd.DataFrame([optimum])).values[0]
    print(f"\n  예측 최대 인장 강도: {pred:.3f} MPa")
    print(f"  관측 데이터 내 최대값 : {df['Tensile_Strength'].max():.3f} MPa")

    # ------------------------------------------------------------------
    # [7] 다음 단계 실험 설계 제안 (요구사항 4)
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[7] 다음 단계 제안")
    print("=" * 64)
    print(f"  - 효과 크기-기여율 기준 핵심 요인 {top_factors} 확보(A-C-F가 기여율 90% 이상).")
    print(f"    (참고: 노이즈가 작아 ANOVA 상 {len(sig)}개 모두 p<0.05이나, B-D는 효과-기여율이 미미함)")
    print("  - 효과가 작은 요인(B-D)은 고정하여 차원을 축소한다.")
    print("  - 핵심 2~3요인에 대해 '완전 요인 실험(2^k)'을 수행하면")
    print("    교락 없이 2차 상호작용까지 깨끗이 추정할 수 있다.")
    print("  - 곡률(비선형)이 의심되면 중심점을 추가하고, 유의 시")
    print("    '반응표면법(RSM, 중심합성설계 CCD)'으로 최적점을 정밀 탐색한다.")


if __name__ == "__main__":
    main()

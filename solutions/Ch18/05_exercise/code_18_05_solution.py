# code_18_05_solution.py
"""18.5 연습 문제 해답 — 세 가지 세정제(A, B, C)의 세척 효과 비교.

본 스크립트는 자기완결형(self-contained)으로, 문제에 제시된 데이터 생성
코드(np.random.seed(101))를 그대로 포함하며 외부 xlsx 파일을 사용하지 않는다.

수행 과제
---------
1) 가상 데이터 생성 및 데이터 확인(구조 점검)
2) 반복(replication)을 활용한 순수오차(pure error) 추정
3) 일원분산분석(One-Way ANOVA) 모델 적합 및 결과 해석
4) 유의효과(α=0.05) 식별 및 Tukey HSD 사후검정
5) 반복에 따른 변동 / 적합결여(lack-of-fit) 관점 설명
6) 효과(요인 평균) 및 잔차 진단 시각화
7) 결론 및 망소특성 기준 최적 조건(최적 세정제) 도출·출력

모든 그림은 matplotlib만 사용하며(seaborn 미사용), 같은 폴더에 PNG로 저장된다.
"""

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import f_oneway

import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

warnings.filterwarnings("ignore")

# 한글 폰트 설정
plt.rc("font", family="Malgun Gothic")
plt.rc("axes", unicode_minus=False)

HERE = Path(__file__).resolve().parent
ALPHA = 0.05


# ----------------------------------------------------------------------
# [Step 0] 가상 데이터 생성 (문제 제공 코드 — seed 동일)
# ----------------------------------------------------------------------
def make_data():
    np.random.seed(101)
    contaminant_A = np.random.normal(loc=15, scale=2.5, size=6)
    contaminant_B = np.random.normal(loc=10, scale=2.5, size=6)
    contaminant_C = np.random.normal(loc=12, scale=2.5, size=6)

    df = pd.DataFrame(
        {
            "Detergent": (["A"] * 6) + (["B"] * 6) + (["C"] * 6),
            "Contaminant_mg": np.concatenate(
                [contaminant_A, contaminant_B, contaminant_C]
            ),
        }
    )
    return df


def main():
    print("=" * 64)
    print("[Step 0] 가상 데이터 생성 및 데이터 구조 점검")
    print("=" * 64)
    df = make_data()
    print("\n생성된 데이터 (long format, 총 {}행):".format(len(df)))
    print(df.to_string(index=False))

    desc = df.groupby("Detergent")["Contaminant_mg"].agg(
        ["count", "mean", "std", "min", "max"]
    )
    print("\n세정제별 기술통계 (망소특성: 평균이 낮을수록 우수):")
    print(desc.round(3))

    k = df["Detergent"].nunique()      # 처리 수준 수
    N = len(df)                        # 전체 관측치 수
    print(f"\n처리 수준 수 k = {k},  전체 관측치 수 N = {N}")

    # ------------------------------------------------------------------
    # [Step 1] 반복(replication) 기반 순수오차(pure error) 추정
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[Step 1] 반복을 활용한 순수오차(Pure Error) 추정")
    print("=" * 64)
    # 각 처리 내부의 반복 관측치로부터 군내제곱합(SS_within = SS_pure_error)을 계산
    grand_mean = df["Contaminant_mg"].mean()
    ss_total = ((df["Contaminant_mg"] - grand_mean) ** 2).sum()

    ss_pure = 0.0
    for name, g in df.groupby("Detergent"):
        gm = g["Contaminant_mg"].mean()
        ss_g = ((g["Contaminant_mg"] - gm) ** 2).sum()
        ss_pure += ss_g
        print(f"  세정제 {name}: 그룹평균={gm:.3f}, 군내SS={ss_g:.3f}, "
              f"반복수={len(g)} (df={len(g) - 1})")

    df_pure = N - k                    # 순수오차 자유도
    ms_pure = ss_pure / df_pure        # 순수오차 평균제곱 = 순수오차 분산 추정치
    print(f"\n  순수오차 SS(=군내SS 합)  = {ss_pure:.4f}")
    print(f"  순수오차 자유도 df        = N - k = {N} - {k} = {df_pure}")
    print(f"  순수오차 분산 추정 MS_e   = {ms_pure:.4f}")
    print(f"  순수오차 표준편차 sigma_hat = {np.sqrt(ms_pure):.4f}")
    print("  => 반복(6회)이 없었다면 처리당 자유도가 0이 되어 "
          "순수오차를 추정할 수 없다.")

    # ------------------------------------------------------------------
    # [Step 2] 일원분산분석(One-Way ANOVA) — 모델 적합 및 검정
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[Step 2] 일원분산분석(One-Way ANOVA)")
    print("=" * 64)

    groups = [g["Contaminant_mg"].values for _, g in df.groupby("Detergent")]
    f_stat, p_value = f_oneway(*groups)
    print(f"scipy f_oneway 결과:  F = {f_stat:.4f},  p = {p_value:.6f}")

    # statsmodels OLS 기반 ANOVA 표(동일 결과, 표 형태 제공)
    model = ols("Contaminant_mg ~ C(Detergent)", data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print("\nstatsmodels ANOVA 표:")
    print(anova_table.round(4))

    df_treat = k - 1
    print(f"\n자유도 분해:  처리 df = k-1 = {df_treat},  "
          f"오차 df = N-k = {df_pure},  전체 df = N-1 = {N - 1}")
    print(f"검증:  SS_total = {ss_total:.4f}  "
          f"(처리SS + 오차SS = {ss_total - ss_pure:.4f} + {ss_pure:.4f})")

    # ------------------------------------------------------------------
    # [Step 3] 유의효과 식별 (α=0.05) 및 사후검정
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print(f"[Step 3] 유의효과 식별 (유의수준 alpha = {ALPHA})")
    print("=" * 64)
    if p_value < ALPHA:
        print(f"p = {p_value:.6f} < {ALPHA}  =>  귀무가설 기각.")
        print("=> 세정제 종류(요인)는 잔류 오염물 양에 통계적으로 "
              "유의한 효과가 있다.")
        print("\nTukey HSD 사후검정(어느 쌍이 다른가):")
        tukey = pairwise_tukeyhsd(
            endog=df["Contaminant_mg"], groups=df["Detergent"], alpha=ALPHA
        )
        print(tukey)
    else:
        print(f"p = {p_value:.6f} >= {ALPHA}  =>  귀무가설 채택.")
        print("=> 세정제 종류 간 유의한 차이가 있다고 볼 수 없다.")
        tukey = None

    # ------------------------------------------------------------------
    # [Step 4] 반복에 따른 변동 / 적합결여(Lack-of-Fit) 관점
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[Step 4] 반복에 따른 변동 및 적합결여(Lack-of-Fit) 관점")
    print("=" * 64)
    print("- 일원배치(질적 요인, 3수준)에서 모델은 각 수준의 평균을 그대로")
    print("  추정하므로, 처리평균과 실제 그룹평균이 일치한다.")
    print("  따라서 적합결여(Lack-of-Fit) 제곱합 = 0, 잔차SS는 전부")
    print("  순수오차(반복에 의한 변동)로 구성된다.")
    print(f"  잔차SS = {model.ssr:.4f} == 순수오차SS = {ss_pure:.4f} "
          f"(일치 여부: {np.isclose(model.ssr, ss_pure)})")
    print("- 즉, 반복(replication)이 제공한 자유도(df={}) 덕분에 순수오차를".format(df_pure))
    print("  독립적으로 추정할 수 있고, 이를 분모로 한 F-검정이 가능해진다.")
    print("- (참고) 회귀형 모델(예: 수준에 수치를 부여한 1차/곡선 적합)에서는")
    print("  반복이 있어야 잔차SS = 순수오차SS + 적합결여SS 로 분해하여")
    print("  모델 형태의 타당성(곡률 누락 여부)을 검정할 수 있다.")

    # 그룹별 변동(분산 동질성 참고) — Levene 검정
    lev_stat, lev_p = stats.levene(*groups)
    print(f"\n분산 동질성(Levene) 검정:  통계량={lev_stat:.4f}, p={lev_p:.4f}"
          f"  => {'동질 가정 만족' if lev_p >= ALPHA else '동질 가정 주의'}")

    # ------------------------------------------------------------------
    # [Step 5] 시각화 — 효과 비교 + 잔차 진단
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[Step 5] 시각화 (PNG 저장)")
    print("=" * 64)

    levels = sorted(df["Detergent"].unique())
    means = [df.loc[df["Detergent"] == lv, "Contaminant_mg"].mean()
             for lv in levels]

    # 그림 1: 효과 비교 (Boxplot + 평균 점)
    fig1, ax1 = plt.subplots(figsize=(7.5, 5.5))
    box_data = [df.loc[df["Detergent"] == lv, "Contaminant_mg"].values
                for lv in levels]
    ax1.boxplot(box_data, tick_labels=levels)
    for i, m in enumerate(means, start=1):
        ax1.plot(i, m, marker="D", color="red", markersize=8, zorder=3)
    ax1.plot(range(1, len(levels) + 1), means, color="red",
             linestyle="--", label="그룹 평균")
    ax1.axhline(grand_mean, color="gray", linestyle=":", label="전체 평균")
    ax1.set_title("세정제별 잔류 오염물 양 분포 (낮을수록 우수, 망소특성)")
    ax1.set_xlabel("세정제 종류")
    ax1.set_ylabel("잔류 오염물 (mg)")
    ax1.legend()
    fig1.tight_layout()
    png1 = HERE / "code_18_05_solution_boxplot.png"
    fig1.savefig(png1, dpi=120)
    plt.close(fig1)
    print(f"  저장: {png1.name}")

    # 그림 2: 잔차 진단 (잔차 vs 적합값, Q-Q plot)
    fitted = model.fittedvalues
    resid = model.resid

    fig2, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(fitted, resid, color="steelblue", edgecolor="k")
    axes[0].axhline(0, color="red", linestyle="--")
    axes[0].set_title("잔차 vs 적합값")
    axes[0].set_xlabel("적합값(그룹 평균)")
    axes[0].set_ylabel("잔차")

    sm.qqplot(resid, line="s", ax=axes[1])
    axes[1].set_title("잔차 정규 Q-Q Plot")

    fig2.suptitle("잔차 진단 (모델 가정 점검)")
    fig2.tight_layout()
    png2 = HERE / "code_18_05_solution_residuals.png"
    fig2.savefig(png2, dpi=120)
    plt.close(fig2)
    print(f"  저장: {png2.name}")

    # 잔차 정규성(Shapiro) 참고
    sh_stat, sh_p = stats.shapiro(resid)
    print(f"  잔차 정규성(Shapiro-Wilk): 통계량={sh_stat:.4f}, p={sh_p:.4f}"
          f"  => {'정규성 만족' if sh_p >= ALPHA else '정규성 주의'}")

    # ------------------------------------------------------------------
    # [Step 6] 결론 및 최적 조건 도출
    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[Step 6] 결론 및 최적 조건(최적 세정제) 도출")
    print("=" * 64)
    best = desc["mean"].idxmin()
    best_mean = desc.loc[best, "mean"]
    print(f"- ANOVA 결과: F={f_stat:.4f}, p={p_value:.6f} "
          f"({'유의' if p_value < ALPHA else '비유의'} @ alpha={ALPHA})")
    if p_value < ALPHA:
        print("- 세정제 종류에 따라 세척 성능에 통계적으로 유의한 차이가 있다.")
    else:
        print("- 세정제 종류 간 통계적으로 유의한 차이는 확인되지 않았다.")
    print(f"- 망소특성(잔류 오염물 최소화) 기준 최적 세정제: '{best}' "
          f"(평균 {best_mean:.3f} mg)")
    print("- 반복 실험은 순수오차 자유도(df={})를 확보하여 F-검정 분모를 "
          "제공했고,".format(df_pure))
    print("  이를 통해 처리 효과의 통계적 유의성 판정이 가능해졌다.")
    print("\n분석을 완료했습니다.")


if __name__ == "__main__":
    main()

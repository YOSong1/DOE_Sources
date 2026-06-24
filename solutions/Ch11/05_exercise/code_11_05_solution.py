# code_11_05_solution.py
# -*- coding: utf-8 -*-
"""
페이지: 11.5 연습 문제 — 반도체 웨이퍼 공정 최적화 (해답 코드)
설명: 식각 시간, 플라즈마 강도, 가스 혼합 비율의 3요인 2수준 x 반복 3회
      가상 표면 거칠기 데이터를 자기완결형으로 생성하고, 과제 2)~5)를
      모두 구현한다.

      과제 1) 데이터 생성 (문제 본문 코드, seed=42 동일)
      과제 2) 설계 행렬/데이터 확인
      과제 3) statsmodels OLS 주효과 + 2차 상호작용 모델 적합, 요약/ANOVA,
              유의수준 0.05 유의 효과 식별
      과제 4) 주효과·상호작용·잔차 진단 시각화 (PNG 저장)
      과제 5) 표면 거칠기를 최소화하는 최적 공정 조건 도출 및 출력

      ※ seaborn 미설치 환경이므로 matplotlib만 사용한다.
"""

import os
import itertools

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # 화면 표시 없이 파일 저장 전용 백엔드
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))


def banner(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ---------------------------------------------------------------------------
# 과제 1) 데이터 생성 (문제 본문 코드 그대로, seed 동일 → 자기완결형)
# ---------------------------------------------------------------------------
def generate_data():
    factors_etching = {
        "Etching_Time": [15, 30],
        "Plasma_Intensity": [200, 300],
        "Gas_Mixture_Ratio": [50, 70],
    }

    np.random.seed(42)
    etching_experiment_data = []
    for time, intensity, ratio in itertools.product(
        factors_etching["Etching_Time"],
        factors_etching["Plasma_Intensity"],
        factors_etching["Gas_Mixture_Ratio"],
    ):
        for rep in range(3):
            # -1/+1 코딩
            time_norm = (time - 22.5) / 7.5
            intensity_norm = (intensity - 250) / 50
            ratio_norm = (ratio - 60) / 10
            # 주효과 및 상호작용 가정
            surface_roughness = (
                10
                + 1.5 * time_norm
                - 2.5 * intensity_norm
                + 0.5 * ratio_norm
                - 1.0 * time_norm * intensity_norm
                + np.random.normal(0, 0.5)
            )
            etching_experiment_data.append(
                {
                    "Etching_Time": time,
                    "Plasma_Intensity": intensity,
                    "Gas_Mixture_Ratio": ratio,
                    "Replicate": rep + 1,
                    "Surface_Roughness": surface_roughness,
                }
            )
    return pd.DataFrame(etching_experiment_data)


# ---------------------------------------------------------------------------
# 과제 4) 시각화: 주효과
# ---------------------------------------------------------------------------
def plot_main_effects(df):
    factors = ["Etching_Time", "Plasma_Intensity", "Gas_Mixture_Ratio"]
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    grand_mean = df["Surface_Roughness"].mean()
    for ax, f in zip(axes, factors):
        means = df.groupby(f)["Surface_Roughness"].mean()
        ax.plot(means.index.astype(str), means.values, "o-", color="tab:blue")
        ax.axhline(grand_mean, color="gray", ls="--", lw=1, label="전체 평균")
        ax.set_title(f"주효과: {f}")
        ax.set_xlabel(f"{f} 수준")
        ax.set_ylabel("표면 거칠기 평균 (nm)")
        ax.legend()
    fig.suptitle("주효과 그림 (낮을수록 좋음)", fontsize=13)
    plt.tight_layout()
    out = os.path.join(HERE, "solution_main_effects.png")
    plt.savefig(out, dpi=120)
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# 과제 4) 시각화: 박스 플롯
# ---------------------------------------------------------------------------
def plot_boxplots(df):
    factors = ["Etching_Time", "Plasma_Intensity", "Gas_Mixture_Ratio"]
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    for ax, f in zip(axes, factors):
        levels = sorted(df[f].unique())
        data = [df.loc[df[f] == lv, "Surface_Roughness"].values for lv in levels]
        ax.boxplot(data, labels=[str(lv) for lv in levels])
        ax.set_title(f"박스 플롯: {f}")
        ax.set_xlabel(f"{f} 수준")
        ax.set_ylabel("표면 거칠기 (nm)")
    fig.suptitle("요인별 표면 거칠기 분포", fontsize=13)
    plt.tight_layout()
    out = os.path.join(HERE, "solution_boxplots.png")
    plt.savefig(out, dpi=120)
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# 과제 4) 시각화: 상호작용 그림 (유의한 상호작용 대상)
# ---------------------------------------------------------------------------
def plot_interaction(df, f1, f2):
    fig, ax = plt.subplots(figsize=(6, 4.5))
    levels_f2 = sorted(df[f2].unique())
    for lv2 in levels_f2:
        sub = df[df[f2] == lv2]
        means = sub.groupby(f1)["Surface_Roughness"].mean()
        ax.plot(means.index.astype(str), means.values, "o-", label=f"{f2}={lv2}")
    ax.set_title(f"상호작용 그림: {f1} x {f2}")
    ax.set_xlabel(f"{f1} 수준")
    ax.set_ylabel("표면 거칠기 평균 (nm)")
    ax.legend(title=f2)
    plt.tight_layout()
    out = os.path.join(HERE, "solution_interaction.png")
    plt.savefig(out, dpi=120)
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# 과제 4) 시각화: 잔차 진단
# ---------------------------------------------------------------------------
def plot_residual_diagnostics(model):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].scatter(model.fittedvalues, model.resid, alpha=0.7, color="tab:blue")
    axes[0].axhline(0, color="red", ls="--")
    axes[0].set_xlabel("적합값 (예측값)")
    axes[0].set_ylabel("잔차")
    axes[0].set_title("잔차 vs 적합값")
    sm.qqplot(model.resid, line="s", ax=axes[1])
    axes[1].set_title("Q-Q Plot (정규성)")
    plt.tight_layout()
    out = os.path.join(HERE, "solution_residuals.png")
    plt.savefig(out, dpi=120)
    plt.close(fig)
    return out


def main():
    # -------------------------------------------------------------------
    # 과제 1) 데이터 생성
    # -------------------------------------------------------------------
    banner("[과제 1] 데이터 생성 (seed=42, 2^3 x 반복 3회)")
    df = generate_data()
    print(f"총 관측치 수: {len(df)} (= 2x2x2 조합 8개 x 반복 3회)")

    # -------------------------------------------------------------------
    # 과제 2) 설계 행렬 / 데이터 확인
    # -------------------------------------------------------------------
    banner("[과제 2] 설계 행렬 및 데이터 확인")
    print("처음 10행:")
    print(df.head(10).to_string(index=False))
    print("\n요인 수준 조합별 관측치 수:")
    combo = (
        df.groupby(["Etching_Time", "Plasma_Intensity", "Gas_Mixture_Ratio"])
        .size()
        .reset_index(name="n")
    )
    print(combo.to_string(index=False))
    print("\n각 요인의 수준:")
    for f in ["Etching_Time", "Plasma_Intensity", "Gas_Mixture_Ratio"]:
        print(f"  {f}: {sorted(df[f].unique())}")

    # -------------------------------------------------------------------
    # 과제 3) 통계 모델 구축 및 분석
    # -------------------------------------------------------------------
    banner("[과제 3] OLS 모델 적합 (주효과 + 모든 2차 상호작용)")
    formula = (
        "Surface_Roughness ~ Etching_Time + Plasma_Intensity + Gas_Mixture_Ratio "
        "+ Etching_Time:Plasma_Intensity + Etching_Time:Gas_Mixture_Ratio "
        "+ Plasma_Intensity:Gas_Mixture_Ratio"
    )
    print("모델 식:")
    print("  " + formula)
    model = smf.ols(formula, data=df).fit()

    print("\n--- 모델 요약 ---")
    print(model.summary())

    print(f"\nR-squared      : {model.rsquared:.4f}")
    print(f"Adj. R-squared : {model.rsquared_adj:.4f}")
    print(f"F-statistic    : {model.fvalue:.4f}  (Prob(F) = {model.f_pvalue:.3e})")

    banner("[과제 3] ANOVA 테이블 (Type II)")
    anova = sm.stats.anova_lm(model, typ=2)
    print(anova.to_string())

    alpha = 0.05
    sig_terms = anova[anova["PR(>F)"] < alpha].index.tolist()
    sig_terms = [t for t in sig_terms if t != "Residual"]
    print(f"\n유의수준 alpha={alpha} 에서 유의한 항:")
    if sig_terms:
        for t in sig_terms:
            print(f"  - {t}  (p = {anova.loc[t, 'PR(>F)']:.3e})")
    else:
        print("  (없음)")

    # 효과 크기 (high - low) : 양수면 high 수준에서 거칠기 증가
    print("\n주효과 크기 (high 수준 평균 - low 수준 평균; 거칠기 최소화 목표):")
    for f, (lo, hi) in [
        ("Etching_Time", (15, 30)),
        ("Plasma_Intensity", (200, 300)),
        ("Gas_Mixture_Ratio", (50, 70)),
    ]:
        eff = (
            df.loc[df[f] == hi, "Surface_Roughness"].mean()
            - df.loc[df[f] == lo, "Surface_Roughness"].mean()
        )
        favorable = lo if eff > 0 else hi
        print(f"  {f:20s}: {eff:+.3f} nm  → 거칠기 최소화에 유리한 수준: {favorable}")

    # 기여율
    ss_total = anova["sum_sq"].sum()
    contribution = (anova["sum_sq"] / ss_total * 100).round(2)
    print("\n항별 기여율(%):")
    print(contribution.to_string())

    # -------------------------------------------------------------------
    # 과제 4) 시각적 분석
    # -------------------------------------------------------------------
    banner("[과제 4] 시각화 (PNG 저장)")
    p1 = plot_main_effects(df)
    p2 = plot_boxplots(df)
    print(f"  주효과 그림 저장 : {p1}")
    print(f"  박스 플롯 저장   : {p2}")

    # 유의한 2차 상호작용 그림 (있으면)
    interaction_terms = [t for t in sig_terms if ":" in t]
    if interaction_terms:
        term = interaction_terms[0]
        f1, f2 = term.split(":")
        p3 = plot_interaction(df, f1.strip(), f2.strip())
        print(f"  상호작용 그림 저장: {p3}  (유의 상호작용: {term})")
    else:
        print("  유의한 2차 상호작용 없음 → 상호작용 그림 생략")

    p4 = plot_residual_diagnostics(model)
    print(f"  잔차 진단 저장   : {p4}")

    # -------------------------------------------------------------------
    # 과제 5) 결론 및 최적 조건 제시
    # -------------------------------------------------------------------
    banner("[과제 5] 최적 공정 조건 도출 (표면 거칠기 최소화)")

    # (a) 실험점 평균 기준 최소 조건
    grouped = (
        df.groupby(["Etching_Time", "Plasma_Intensity", "Gas_Mixture_Ratio"])[
            "Surface_Roughness"
        ]
        .mean()
        .reset_index()
    )
    best_obs = grouped.loc[grouped["Surface_Roughness"].idxmin()]
    print("(a) 실험점 평균 거칠기가 최소인 조합:")
    print(f"    Etching_Time      = {int(best_obs['Etching_Time'])} 초")
    print(f"    Plasma_Intensity  = {int(best_obs['Plasma_Intensity'])} W")
    print(f"    Gas_Mixture_Ratio = {int(best_obs['Gas_Mixture_Ratio'])} %")
    print(f"    평균 표면 거칠기  = {best_obs['Surface_Roughness']:.3f} nm")

    # (b) 적합 모델로 모든 조합 예측 → 최소 예측 조건
    levels = {
        "Etching_Time": [15, 30],
        "Plasma_Intensity": [200, 300],
        "Gas_Mixture_Ratio": [50, 70],
    }
    grid = pd.DataFrame(
        list(itertools.product(*levels.values())),
        columns=list(levels.keys()),
    )
    grid["pred_roughness"] = model.predict(grid)
    best_pred = grid.loc[grid["pred_roughness"].idxmin()]
    print("\n(b) 적합 모델 예측 거칠기가 최소인 조합:")
    print(f"    Etching_Time      = {int(best_pred['Etching_Time'])} 초")
    print(f"    Plasma_Intensity  = {int(best_pred['Plasma_Intensity'])} W")
    print(f"    Gas_Mixture_Ratio = {int(best_pred['Gas_Mixture_Ratio'])} %")
    print(f"    예측 표면 거칠기  = {best_pred['pred_roughness']:.3f} nm")

    print("\n[결론]")
    print("  - Plasma_Intensity 가 거칠기에 가장 큰 영향을 주며, 높을수록(300 W)")
    print("    거칠기가 낮아진다.")
    print("  - Etching_Time 은 낮을수록(15 초) 거칠기가 낮아지고,")
    print("    Etching_Time x Plasma_Intensity 상호작용이 유의하다.")
    print("  - Gas_Mixture_Ratio 의 영향은 상대적으로 작다.")
    print("  - 따라서 표면 거칠기를 최소화하는 권장 공정 조건은 위 (b)의 조합이다.")

    banner("분석 완료")


if __name__ == "__main__":
    main()

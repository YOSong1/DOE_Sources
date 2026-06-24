# code_13_05_solution.py
# -*- coding: utf-8 -*-
"""
13.5 연습 문제 해답 — 제빵 공정 최적화 (응답 표면 방법론, RSM)
================================================================
발효 시간(Fermentation_Time)과 굽는 온도(Baking_Temperature) 두 요인이
식빵 부드러움 점수(Softness_Score)에 미치는 영향을 2차 응답 표면 모형으로
분석하고, 부드러움 점수를 최대화하는 최적 공정 조건을 도출한다.

자기완결형 스크립트: 문제에서 제공한 데이터 생성 코드(seed=420)를 그대로
포함하므로 외부 xlsx 파일이 필요 없다.

수행 단계
  [1] 데이터 생성 및 확인
  [2] statsmodels OLS 2차 다항 회귀 모형 적합(주효과+상호작용+제곱항)
  [3] 모형 요약 및 ANOVA, 유의효과(alpha=0.05) 식별
  [4] 등고선도 / 3D 반응 표면 시각화
  [5] 잔차 진단(정규성, 등분산성)
  [6] 정상점(stationary point) 및 최적 조건 도출
"""

import os

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (3D 투영 등록용)

# ----------------------------------------------------------------------
# 한글 폰트 설정
# ----------------------------------------------------------------------
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))

# 요인 수준 범위(데이터 생성 및 격자 시각화 공통 사용)
FT_LO, FT_HI = 60, 120     # 발효 시간 (분)
BT_LO, BT_HI = 180, 220    # 굽는 온도 (°C)
ALPHA = 0.05               # 유의수준


# ======================================================================
# [1] 데이터 생성 (문제 제공 코드, seed 동일)
# ======================================================================
def generate_data():
    np.random.seed(420)          # 결과 재현성을 위한 시드
    n_samples = 30               # 총 실험 횟수 (가상)

    fermentation_time = np.random.uniform(FT_LO, FT_HI, n_samples)
    baking_temperature = np.random.uniform(BT_LO, BT_HI, n_samples)

    true_softness_effect = (
        50
        + 0.3 * (fermentation_time - 90)
        - 0.2 * (baking_temperature - 200)
        - 0.005 * ((fermentation_time - 90) ** 2)
        - 0.008 * ((baking_temperature - 200) ** 2)
        + 0.001 * (fermentation_time - 90) * (baking_temperature - 200)
    )

    noise = np.random.normal(0, 3, n_samples)  # 평균 0, 표준편차 3의 오차
    softness_score = true_softness_effect + noise
    softness_score = np.clip(softness_score, 0, 100)

    df = pd.DataFrame({
        "Fermentation_Time": fermentation_time,
        "Baking_Temperature": baking_temperature,
        "Softness_Score": softness_score,
    })
    return df


# ======================================================================
# [3] 2차 응답 표면 모형 적합
# ======================================================================
def fit_quadratic_model(df):
    formula = (
        "Softness_Score ~ Fermentation_Time + Baking_Temperature "
        "+ I(Fermentation_Time**2) + I(Baking_Temperature**2) "
        "+ Fermentation_Time:Baking_Temperature"
    )
    model = smf.ols(formula, data=df).fit()
    return model


# ======================================================================
# [6] 정상점(stationary point) 계산
# ======================================================================
def stationary_point(model):
    """
    2차 모형  y = b0 + b'x + x'B x  의 정상점 x* = -0.5 * B^{-1} b 를 구한다.
    B 의 고유값 부호로 최대/최소/안장점을 판별한다.
    """
    p = model.params
    b1 = p["Fermentation_Time"]
    b2 = p["Baking_Temperature"]
    b11 = p["I(Fermentation_Time ** 2)"]
    b22 = p["I(Baking_Temperature ** 2)"]
    b12 = p["Fermentation_Time:Baking_Temperature"]

    b = np.array([b1, b2])
    B = np.array([[b11, b12 / 2.0],
                  [b12 / 2.0, b22]])

    x_star = -0.5 * np.linalg.solve(B, b)
    eig = np.linalg.eigvalsh(B)

    if (eig > 0).all():
        kind = "최소점"
    elif (eig < 0).all():
        kind = "최대점"
    else:
        kind = "안장점"

    y_star = model.predict(pd.DataFrame({
        "Fermentation_Time": [x_star[0]],
        "Baking_Temperature": [x_star[1]],
    })).values[0]

    return x_star, y_star, eig, kind, B


# ======================================================================
# 격자 예측(시각화/격자탐색 공통)
# ======================================================================
def predict_grid(model, n=60):
    f_grid = np.linspace(FT_LO, FT_HI, n)
    t_grid = np.linspace(BT_LO, BT_HI, n)
    F, T = np.meshgrid(f_grid, t_grid)
    Yp = model.predict(pd.DataFrame({
        "Fermentation_Time": F.ravel(),
        "Baking_Temperature": T.ravel(),
    })).values.reshape(F.shape)
    return F, T, Yp


# ======================================================================
# [4] 시각화: 등고선 + 3D 표면
# ======================================================================
def plot_response_surface(df, model, x_star, kind):
    F, T, Yp = predict_grid(model, n=60)

    fig = plt.figure(figsize=(14, 6))

    # --- (a) 등고선도 ---
    ax1 = fig.add_subplot(1, 2, 1)
    cs = ax1.contourf(F, T, Yp, levels=15, cmap="viridis")
    fig.colorbar(cs, ax=ax1, label="부드러움 점수")
    ax1.contour(F, T, Yp, levels=15, colors="white", linewidths=0.4, alpha=0.6)
    ax1.scatter(df["Fermentation_Time"], df["Baking_Temperature"],
                c="white", edgecolors="black", s=35, label="관측 실험점")
    if FT_LO <= x_star[0] <= FT_HI and BT_LO <= x_star[1] <= BT_HI:
        ax1.scatter(x_star[0], x_star[1], c="red", marker="*", s=300,
                    edgecolors="black", label=f"정상점({kind})")
    ax1.set_xlabel("발효 시간 (분)")
    ax1.set_ylabel("굽는 온도 (°C)")
    ax1.set_title("등고선도 (Contour)")
    ax1.legend(loc="upper right")

    # --- (b) 3D 표면도 ---
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    ax2.plot_surface(F, T, Yp, cmap="viridis", alpha=0.85,
                     linewidth=0, antialiased=True)
    ax2.scatter(df["Fermentation_Time"], df["Baking_Temperature"],
                df["Softness_Score"], c="red", s=25, label="관측값")
    ax2.set_xlabel("발효 시간 (분)")
    ax2.set_ylabel("굽는 온도 (°C)")
    ax2.set_zlabel("부드러움 점수")
    ax2.set_title("3D 반응 표면 (Surface)")

    fig.suptitle("제빵 공정 응답 표면 분석", fontsize=14)
    fig.tight_layout()
    out = os.path.join(HERE, "code_13_05_solution_surface.png")
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


# ======================================================================
# [5] 잔차 진단
# ======================================================================
def plot_residual_diagnostics(model):
    fitted = model.fittedvalues
    resid = model.resid

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # 잔차 vs 적합값 (등분산성)
    axes[0].scatter(fitted, resid, c="steelblue", edgecolors="k", s=40)
    axes[0].axhline(0, color="red", linestyle="--", linewidth=1)
    axes[0].set_xlabel("적합값 (Fitted)")
    axes[0].set_ylabel("잔차 (Residual)")
    axes[0].set_title("잔차 vs 적합값")

    # Q-Q 플롯 (정규성)
    sm.qqplot(resid, line="45", fit=True, ax=axes[1])
    axes[1].set_title("정규 Q-Q 플롯")

    fig.suptitle("잔차 진단", fontsize=14)
    fig.tight_layout()
    out = os.path.join(HERE, "code_13_05_solution_residuals.png")
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


# ======================================================================
# 메인
# ======================================================================
def main():
    # ------------------------------------------------------------------
    print("=" * 64)
    print("[1] 데이터 생성 및 확인")
    print("=" * 64)
    df = generate_data()
    print("--- 실험 데이터(처음 5행) ---")
    print(df.head().round(3))
    print(f"\n총 데이터 포인트 수: {len(df)}")
    print("\n--- 요약 통계 ---")
    print(df.describe().round(2))

    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[2] 2차 응답 표면 모형 적합 (주효과 + 상호작용 + 제곱항)")
    print("=" * 64)
    model = fit_quadratic_model(df)
    print(model.summary())

    print(f"\n  R^2      = {model.rsquared:.4f}")
    print(f"  Adj R^2  = {model.rsquared_adj:.4f}")
    print(f"  F p-value = {model.f_pvalue:.4g}  "
          f"-> {'모형 유의함' if model.f_pvalue < ALPHA else '모형 유의하지 않음'}")

    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[3] ANOVA (Type II) 및 유의효과 식별 (alpha=0.05)")
    print("=" * 64)
    aov = anova_lm(model, typ=2)
    print(aov.round(4))

    print("\n--- 항별 유의성 (회귀계수 t-검정) ---")
    label = {
        "Intercept": "절편",
        "Fermentation_Time": "발효시간(1차)",
        "Baking_Temperature": "굽는온도(1차)",
        "I(Fermentation_Time ** 2)": "발효시간(제곱)",
        "I(Baking_Temperature ** 2)": "굽는온도(제곱)",
        "Fermentation_Time:Baking_Temperature": "상호작용",
    }
    sig_terms = []
    for term in model.params.index:
        coef = model.params[term]
        pval = model.pvalues[term]
        mark = "유의" if pval < ALPHA else "비유의"
        if pval < ALPHA and term != "Intercept":
            sig_terms.append(label.get(term, term))
        print(f"  {label.get(term, term):14s} "
              f"계수={coef:10.5f}  p={pval:.4f}  [{mark}]")

    print(f"\n  => 유의한 항(alpha=0.05): "
          f"{', '.join(sig_terms) if sig_terms else '없음'}")

    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[4] 정상점(stationary point) 및 최적 조건 도출")
    print("=" * 64)
    x_star, y_star, eig, kind, B = stationary_point(model)
    print(f"  헤시안 고유값      = {eig.round(5)}  -> {kind}")
    print(f"  정상점 발효 시간   = {x_star[0]:.2f} 분")
    print(f"  정상점 굽는 온도   = {x_star[1]:.2f} °C")
    print(f"  정상점 예측 부드러움 = {y_star:.2f}")

    in_region = (FT_LO <= x_star[0] <= FT_HI) and (BT_LO <= x_star[1] <= BT_HI)

    # 실험 영역 내 격자 탐색(정상점이 안장점/영역 밖일 때의 보조 최적화)
    F, T, Yp = predict_grid(model, n=120)
    idx = np.argmax(Yp)
    f_opt_grid, t_opt_grid = F.ravel()[idx], T.ravel()[idx]
    y_opt_grid = Yp.ravel()[idx]

    print("\n--- 실험 영역 내 격자 탐색 최대점 ---")
    print(f"  발효 시간   = {f_opt_grid:.2f} 분")
    print(f"  굽는 온도   = {t_opt_grid:.2f} °C")
    print(f"  예측 부드러움 = {y_opt_grid:.2f}")

    print("\n--- 최종 권장 공정 조건 ---")
    if kind == "최대점" and in_region:
        print(f"  정상점이 영역 내 최대점입니다.")
        print(f"  => 발효 시간 {x_star[0]:.1f}분, 굽는 온도 {x_star[1]:.1f}°C "
              f"(예측 부드러움 {y_star:.1f})")
    else:
        print(f"  정상점이 {kind}이거나 실험 영역을 벗어나, 영역 내 최대점을 채택합니다.")
        print(f"  => 발효 시간 {f_opt_grid:.1f}분, 굽는 온도 {t_opt_grid:.1f}°C "
              f"(예측 부드러움 {y_opt_grid:.1f})")

    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[5] 시각화 및 잔차 진단 그림 저장")
    print("=" * 64)
    p1 = plot_response_surface(df, model, x_star, kind)
    p2 = plot_residual_diagnostics(model)
    print(f"  반응 표면도 저장: {os.path.basename(p1)}")
    print(f"  잔차 진단도 저장: {os.path.basename(p2)}")

    # ------------------------------------------------------------------
    print("\n" + "=" * 64)
    print("[결론]")
    print("=" * 64)
    print("  - 두 제곱항(발효시간^2, 굽는온도^2)이 음(-)의 계수로 작용하여")
    print("    응답 표면이 위로 볼록한 '봉우리' 형태를 띱니다(정상점=최대점).")
    print("  - 따라서 발효 시간과 굽는 온도 모두 중간 수준 부근에서")
    print("    부드러움 점수가 극대화됩니다.")
    print(f"  - 권장 조건: 발효 시간 {x_star[0]:.0f}분 내외, "
          f"굽는 온도 {x_star[1]:.0f}°C 내외")


if __name__ == "__main__":
    main()

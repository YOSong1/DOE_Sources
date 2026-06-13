# -*- coding: utf-8 -*-
"""
페이지: 13.5 연습 문제 — 제빵 공정 RSM - Excel 활용 버전
=========================================================
sample_data.xlsx (30 runs, 두 요인 균일 샘플링) 를 읽어 부드러움 점수를
최대화하는 발효 시간/굽는 온도 조합을 탐색한다.

1. 데이터 구조 확인 및 요약 통계
2. 2차 다항 회귀 모형 적합 (R^2, p-value)
3. 정상점 계산 + 유형 판별 (최대/최소/안장)
4. 등고선도 + 정상점 PNG 저장
5. 권장 공정 조건 출력
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(__file__)
XLSX = os.path.join(HERE, "sample_data.xlsx")


def main() -> None:
    df = pd.read_excel(XLSX)

    print("=" * 60)
    print("[1] 데이터 요약")
    print("=" * 60)
    print(df.head())
    print("\n", df.describe().round(2))

    # 2차 모형 적합
    formula = (
        "Softness_Score ~ Fermentation_Time + Baking_Temperature "
        "+ I(Fermentation_Time**2) + I(Baking_Temperature**2) "
        "+ Fermentation_Time:Baking_Temperature"
    )
    model = smf.ols(formula, data=df).fit()
    print("\n[2] 2차 회귀 모형")
    print(f"  R^2     = {model.rsquared:.4f}")
    print(f"  Adj R^2 = {model.rsquared_adj:.4f}")
    print(f"  F-pvalue= {model.f_pvalue:.4g}")

    # 회귀 계수
    p = model.params
    b1 = p["Fermentation_Time"]
    b2 = p["Baking_Temperature"]
    b11 = p["I(Fermentation_Time ** 2)"]
    b22 = p["I(Baking_Temperature ** 2)"]
    b12 = p["Fermentation_Time:Baking_Temperature"]

    b = np.array([b1, b2])
    B = np.array([[b11, b12 / 2], [b12 / 2, b22]])
    x_star = -0.5 * np.linalg.solve(B, b)
    eig = np.linalg.eigvalsh(B)
    if (eig > 0).all():
        kind = "최소"
    elif (eig < 0).all():
        kind = "최대"
    else:
        kind = "안장점"

    y_star = model.predict(
        pd.DataFrame({"Fermentation_Time": [x_star[0]], "Baking_Temperature": [x_star[1]]})
    ).values[0]

    print("\n[3] 정상점 (실제 단위)")
    print(f"  발효 시간   = {x_star[0]:.2f} 분")
    print(f"  굽는 온도   = {x_star[1]:.2f} °C")
    print(f"  예측 부드러움 = {y_star:.2f}")
    print(f"  고유값 = {eig.round(4)} → {kind}")

    # 등고선도
    f_grid = np.linspace(60, 120, 60)
    t_grid = np.linspace(180, 220, 60)
    F, T = np.meshgrid(f_grid, t_grid)
    Yp = model.predict(
        pd.DataFrame({"Fermentation_Time": F.ravel(), "Baking_Temperature": T.ravel()})
    ).values.reshape(F.shape)

    plt.figure(figsize=(8, 6))
    cs = plt.contourf(F, T, Yp, levels=15, cmap="viridis")
    plt.colorbar(cs, label="Softness Score")
    plt.scatter(
        df["Fermentation_Time"], df["Baking_Temperature"],
        c="white", edgecolors="black", s=30, label="실험점",
    )
    if 60 <= x_star[0] <= 120 and 180 <= x_star[1] <= 220:
        plt.scatter(*x_star, c="red", marker="*", s=200, label=f"정상점({kind})")
    plt.xlabel("Fermentation Time (분)")
    plt.ylabel("Baking Temperature (°C)")
    plt.title("제빵 공정 응답 표면")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "contour.png"), dpi=120)
    plt.close()
    print("\n등고선도 저장: contour.png")

    # 권장 조건
    print("\n[4] 권장 공정 조건")
    if kind == "최대" and 60 <= x_star[0] <= 120 and 180 <= x_star[1] <= 220:
        print(f"  → 발효 {x_star[0]:.1f}분, 굽기 {x_star[1]:.1f}°C 에서 부드러움 최대")
    else:
        # 격자에서 최대 탐색
        idx = np.argmax(Yp)
        f_opt, t_opt = F.ravel()[idx], T.ravel()[idx]
        print(
            f"  정상점이 영역 밖이거나 안장점. 영역 내 최대점 → "
            f"발효 {f_opt:.1f}분, 굽기 {t_opt:.1f}°C"
        )


if __name__ == "__main__":
    main()

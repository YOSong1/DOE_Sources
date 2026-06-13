# -*- coding: utf-8 -*-
"""
페이지: 13.2 응답 표면 방법론의 일반적인 절차 - Excel 활용 버전
================================================================
sample_data.xlsx (2요인 회전가능 CCD, alpha=sqrt(2), 11 runs) 를 읽어
2차 다항 회귀 모형을 적합하고 정상점(Stationary Point) 을 계산한다.

1. 데이터 구조 (factorial / axial / center)
2. 2차 모형 적합 + ANOVA
3. 정상점 좌표 = -0.5 * B^-1 * b
4. 고유값으로 최적점 유형 (max/min/saddle) 판별
5. 등고선도 + 정상점 표시 PNG 저장
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


def classify_eig(eig: np.ndarray) -> str:
    pos = (eig > 0).all()
    neg = (eig < 0).all()
    if pos:
        return "최소(Min)"
    if neg:
        return "최대(Max)"
    return "안장점(Saddle)"


def main() -> None:
    df = pd.read_excel(XLSX)

    print("=" * 60)
    print("[1] CCD 데이터 구조")
    print("=" * 60)
    print(df)
    print(f"\n  factorial: {((df['x1'].abs() == 1) & (df['x2'].abs() == 1)).sum()}")
    print(f"  axial    : {((df['x1'].abs() > 1) | (df['x2'].abs() > 1)).sum()}")
    print(f"  center   : {((df['x1'] == 0) & (df['x2'] == 0)).sum()}")

    model = ols("y ~ x1 + x2 + I(x1**2) + I(x2**2) + x1:x2", data=df).fit()
    print("\n[2] 2차 모형 적합")
    print(f"  R^2     = {model.rsquared:.4f}")
    print(f"  Adj R^2 = {model.rsquared_adj:.4f}")

    anova = sm.stats.anova_lm(model, typ=2)
    print("\n[3] ANOVA")
    print(anova.round(4))

    # 회귀 계수
    p = model.params
    b1, b2 = p["x1"], p["x2"]
    b11, b22 = p["I(x1 ** 2)"], p["I(x2 ** 2)"]
    b12 = p["x1:x2"]

    # 정상점: x* = -0.5 * B^-1 * b
    b_vec = np.array([b1, b2])
    B_mat = np.array([[b11, b12 / 2], [b12 / 2, b22]])
    x_star = -0.5 * np.linalg.solve(B_mat, b_vec)
    y_star = model.predict(
        pd.DataFrame({"x1": [x_star[0]], "x2": [x_star[1]]})
    ).values[0]

    eig = np.linalg.eigvalsh(B_mat)
    kind = classify_eig(eig)

    print("\n[4] 정상점 분석")
    print(f"  x* = ({x_star[0]:.4f}, {x_star[1]:.4f})")
    print(f"  y_hat(x*) = {y_star:.4f}")
    print(f"  B 행렬 고유값: {eig.round(4)} → {kind}")

    # 등고선도
    xs = np.linspace(-1.6, 1.6, 80)
    X1, X2 = np.meshgrid(xs, xs)
    Y = model.predict(
        pd.DataFrame({"x1": X1.ravel(), "x2": X2.ravel()})
    ).values.reshape(X1.shape)

    plt.figure(figsize=(7, 6))
    cs = plt.contourf(X1, X2, Y, levels=20, cmap="viridis")
    plt.colorbar(cs)
    plt.scatter(df["x1"], df["x2"], c="white", edgecolors="black", s=60, label="실험점")
    plt.scatter(*x_star, c="red", marker="*", s=200, label=f"정상점 ({kind})")
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title("반응 표면 등고선")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "contour.png"), dpi=120)
    plt.close()
    print("\n등고선도 저장: contour.png")


if __name__ == "__main__":
    main()

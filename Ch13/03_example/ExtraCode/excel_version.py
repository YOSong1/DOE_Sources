# -*- coding: utf-8 -*-
"""
페이지: 13.3 예제로 이해: 2요인 공정의 응답 표면 분석 - Excel 활용 버전
========================================================================
sample_data.xlsx (5x5 격자, 25 runs) 를 읽어 2차 다항 회귀로 응답 표면을
복원하고 참값(beta_0=5, b1=2, b2=3, b11=1.5, b22=1.0, b12=1.2) 과 비교한다.

1. 데이터 구조
2. 2차 모형 적합 및 R^2
3. 추정 계수 vs 참값 비교
4. 정상점 계산과 유형 판별 (참값 모형은 모든 2차 계수가 양수 → 최소)
5. 3D 응답 표면 + 관측치 시각화
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import statsmodels.formula.api as smf

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(__file__)
XLSX = os.path.join(HERE, "sample_data.xlsx")

TRUE = {"Intercept": 5.0, "x1": 2.0, "x2": 3.0, "x1^2": 1.5, "x2^2": 1.0, "x1x2": 1.2}


def main() -> None:
    df = pd.read_excel(XLSX)
    print("=" * 60)
    print("[1] 데이터 구조 (5x5 격자)")
    print("=" * 60)
    print(df.head())
    print("shape:", df.shape)

    model = smf.ols("y ~ x1 + x2 + I(x1**2) + I(x2**2) + x1:x2", data=df).fit()
    print("\n[2] 2차 모형 적합")
    print(f"  R^2     = {model.rsquared:.4f}")
    print(f"  Adj R^2 = {model.rsquared_adj:.4f}")

    print("\n[3] 추정 계수 vs 참값")
    rename = {
        "Intercept": "Intercept",
        "x1": "x1",
        "x2": "x2",
        "I(x1 ** 2)": "x1^2",
        "I(x2 ** 2)": "x2^2",
        "x1:x2": "x1x2",
    }
    estimated = {rename[k]: v for k, v in model.params.items()}
    comp = pd.DataFrame({"True": TRUE, "Estimated": estimated})
    comp["Error"] = (comp["Estimated"] - comp["True"]).round(4)
    print(comp.round(4))

    # 정상점
    b = np.array([estimated["x1"], estimated["x2"]])
    B = np.array(
        [
            [estimated["x1^2"], estimated["x1x2"] / 2],
            [estimated["x1x2"] / 2, estimated["x2^2"]],
        ]
    )
    x_star = -0.5 * np.linalg.solve(B, b)
    eig = np.linalg.eigvalsh(B)
    if (eig > 0).all():
        kind = "최소(Min)"
    elif (eig < 0).all():
        kind = "최대(Max)"
    else:
        kind = "안장점(Saddle)"
    y_star = model.predict(pd.DataFrame({"x1": [x_star[0]], "x2": [x_star[1]]})).values[0]
    print("\n[4] 정상점 분석")
    print(f"  x* = ({x_star[0]:.4f}, {x_star[1]:.4f})")
    print(f"  y_hat(x*) = {y_star:.4f}")
    print(f"  B 고유값 = {eig.round(4)} → {kind}")

    # 3D 시각화
    xs = np.linspace(-2, 2, 60)
    X1m, X2m = np.meshgrid(xs, xs)
    Yp = model.predict(
        pd.DataFrame({"x1": X1m.ravel(), "x2": X2m.ravel()})
    ).values.reshape(X1m.shape)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection="3d")
    ax.plot_surface(X1m, X2m, Yp, alpha=0.4, cmap="viridis")
    ax.scatter(df["x1"], df["x2"], df["y"], c="red", s=30, label="관측치")
    ax.scatter(*x_star, y_star, c="black", marker="*", s=200, label=f"정상점({kind})")
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_zlabel("y")
    ax.set_title("응답 표면 + 관측치")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, "surface3d.png"), dpi=120)
    plt.close()
    print("\n3D 표면 저장: surface3d.png")


if __name__ == "__main__":
    main()

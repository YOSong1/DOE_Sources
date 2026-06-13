# code_11_03_03.py
# -*- coding: utf-8 -*-
"""
페이지: 11.3 예제로 이해: 초콜릿 코팅 품질의 완전 요인 실험
설명: 주효과 박스플롯, 상호작용 그림, 잔차 진단 시각화 코드.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.stats.anova import anova_lm

# --- 1. 주효과 박스플롯 ---
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, factor in zip(axes, ["Coating_Temperature", "Mixing_Speed", "Cooling_Time"]):
    sns.boxplot(x=factor, y="Coating_Quality", data=df_experiment, ax=ax)
    ax.set_title(f"{factor} 수준별 코팅 품질")
    ax.set_xlabel(factor)
    ax.set_ylabel("Coating Quality")
plt.suptitle("주효과 박스플롯", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.show()

# --- 2. 온도 × 냉각 시간 상호작용 그림 ---
fig, ax = plt.subplots(figsize=(6, 4))
for time_val, label in zip([5, 10], ["냉각 5분", "냉각 10분"]):
    subset = df_experiment[df_experiment["Cooling_Time"] == time_val]
    means = subset.groupby("Coating_Temperature")["Coating_Quality"].mean()
    ax.plot(means.index, means.values, marker="o", label=label)
ax.set_title("온도 × 냉각 시간 상호작용")
ax.set_xlabel("Coating Temperature (°C)")
ax.set_ylabel("평균 Coating Quality")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# --- 3. 잔차 진단: 잔차 vs 예측값, Q-Q Plot ---
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
fitted = model_simple.fittedvalues
residuals = model_simple.resid

axes[0].scatter(fitted, residuals, alpha=0.6)
axes[0].axhline(0, color="red", linestyle="--")
axes[0].set_xlabel("예측값")
axes[0].set_ylabel("잔차")
axes[0].set_title("잔차 vs 예측값")

sm.qqplot(residuals, line="s", ax=axes[1])
axes[1].set_title("Q-Q Plot (잔차 정규성 확인)")
plt.tight_layout()
plt.show()

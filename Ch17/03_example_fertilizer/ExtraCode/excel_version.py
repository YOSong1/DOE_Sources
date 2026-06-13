# Chapter 17.3 Excel 활용 버전
# sample_data.xlsx의 tidy 시트(Fertilizer, Growth_cm)를 읽어
# 그룹별 평균/분산, ANOVA, 효과 크기(η²), 박스플롯을 한 번에 보여 줍니다.

from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import f_oneway
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

xlsx = Path(__file__).with_name("sample_data.xlsx")
df = pd.read_excel(xlsx, sheet_name="tidy")

print("=" * 60)
print("[Step 0] 데이터 구조 점검")
print("=" * 60)
print(df.head())
print(f"\n총 관측치: {len(df)}, 처리 수준: {df['Fertilizer'].nunique()}")

# 그룹별 기술 통계
desc = df.groupby("Fertilizer")["Growth_cm"].describe()[["count", "mean", "std", "min", "max"]]
print("\n[그룹별 기술 통계]")
print(desc)

# ANOVA
groups = [g["Growth_cm"].values for _, g in df.groupby("Fertilizer")]
f_stat, p_value = f_oneway(*groups)

# 효과 크기 η² = SSA / SST 직접 계산 (해석을 돕기 위해)
grand_mean = df["Growth_cm"].mean()
ssa = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in groups)
sst = ((df["Growth_cm"] - grand_mean) ** 2).sum()
eta2 = ssa / sst

print("\n" + "=" * 60)
print("[Step 1] 일원분산분석")
print("=" * 60)
print(f"F-통계량   : {f_stat:.4f}")
print(f"p-value    : {p_value:.4f}")
print(f"η² (효과 크기): {eta2:.3f}  (0.01 작음 / 0.06 중간 / 0.14 큼)")

if p_value < 0.05:
    print("=> α=0.05에서 처리 간 평균 차이가 유의합니다. "
          "이어 사후검정(Tukey HSD 등)을 권장합니다.")
else:
    print("=> α=0.05에서 처리 간 평균 차이가 유의하지 않습니다.")

# 시각화
fig, ax = plt.subplots(figsize=(7, 5))
ax.boxplot([g["Growth_cm"].values for _, g in df.groupby("Fertilizer")],
           tick_labels=sorted(df["Fertilizer"].unique()))
ax.set_title("비료 종류에 따른 식물 성장 (CRD)")
ax.set_xlabel("Fertilizer")
ax.set_ylabel("Growth (cm)")
plt.tight_layout()
plt.show()

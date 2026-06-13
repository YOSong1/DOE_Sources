# Chapter 18.5 Excel 활용 버전
# 세정제 3종 × 6반복 데이터를 Excel에서 읽어
# ANOVA + 효과 크기 + 자유도 해석 + Tukey HSD 사후검정까지 수행합니다.

from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

xlsx = Path(__file__).with_name("sample_data.xlsx")
df = pd.read_excel(xlsx)

print("=" * 60)
print("[Step 0] 데이터 구조 점검")
print("=" * 60)
print(df.head())
print(df.groupby("Detergent")["Contaminant_mg"].describe()[["count", "mean", "std"]])

groups = [g["Contaminant_mg"].values for _, g in df.groupby("Detergent")]
k = len(groups)
N = sum(len(g) for g in groups)

f_stat, p_value = f_oneway(*groups)
print("\n" + "=" * 60)
print(f"[Step 1] 일원 ANOVA   (k={k}, N={N}, df_error={N-k})")
print("=" * 60)
print(f"F={f_stat:.4f}, p={p_value:.4f}")
print(f"=> 반복(6회)이 없었다면 df_error=0이 되어 검정이 불가능합니다.")

if p_value < 0.05:
    print("\n[Step 2] Tukey HSD 사후검정")
    tukey = pairwise_tukeyhsd(endog=df["Contaminant_mg"],
                              groups=df["Detergent"], alpha=0.05)
    print(tukey)

# 망소특성: 평균이 낮을수록 좋음
best = df.groupby("Detergent")["Contaminant_mg"].mean().idxmin()
print(f"\n[해석] 망소특성 기준 평균이 가장 낮은 세정제: {best}")

fig, ax = plt.subplots(figsize=(7, 5))
ax.boxplot([g["Contaminant_mg"].values for _, g in df.groupby("Detergent")],
           tick_labels=sorted(df["Detergent"].unique()))
ax.set_title("세정제별 세척 후 남은 오염물 양 (낮을수록 좋음)")
ax.set_xlabel("Detergent")
ax.set_ylabel("Contaminant (mg)")
plt.tight_layout()
plt.show()

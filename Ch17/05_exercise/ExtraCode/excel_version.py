# Chapter 17.5 Excel 활용 버전
# sample_data.xlsx (Version, Score) tidy 포맷을 읽어
# ANOVA + Tukey HSD 사후검정을 한 번에 보여줍니다.

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
print(df.groupby("Version")["Score"].describe()[["count", "mean", "std"]])

# ANOVA
groups = [g["Score"].values for _, g in df.groupby("Version")]
f_stat, p_value = f_oneway(*groups)

print("\n" + "=" * 60)
print("[Step 1] 일원분산분석 (소프트웨어 버전 효과)")
print("=" * 60)
print(f"F={f_stat:.4f}, p={p_value:.4f}")

if p_value < 0.05:
    print("=> 유의함. 어떤 버전 쌍이 다른지 사후검정으로 확인합니다.")
    print("\n[Step 2] Tukey HSD 사후검정")
    tukey = pairwise_tukeyhsd(endog=df["Score"], groups=df["Version"], alpha=0.05)
    print(tukey)
else:
    print("=> 유의하지 않음. 사후검정 생략.")

# 시각화
fig, ax = plt.subplots(figsize=(7, 5))
ax.boxplot([g["Score"].values for _, g in df.groupby("Version")],
           tick_labels=sorted(df["Version"].unique()))
ax.set_title("교육용 SW 버전별 시험 점수")
ax.set_xlabel("Version")
ax.set_ylabel("Score")
plt.tight_layout()
plt.show()

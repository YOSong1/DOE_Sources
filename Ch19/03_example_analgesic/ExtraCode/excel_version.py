# Chapter 19.3 Excel 활용 버전
# 2x2 교차 설계 데이터를 Excel에서 읽어:
#  (1) 혼합 효과 모형으로 처리/기간 효과 추정
#  (2) 순서 그룹별 평균 시계열 그림으로 이월 효과 가능성 시각 점검
#  (3) 기간 1 데이터만으로도 처리 효과를 단순 비교 (이월 효과 보수적 검토)

from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

xlsx = Path(__file__).with_name("sample_data.xlsx")
df = pd.read_excel(xlsx)

print("=" * 60)
print("[Step 0] 데이터 구조 점검")
print("=" * 60)
print(df.head(6))
print(f"\n피험자 수: {df['Subject'].nunique()}, "
      f"순서 그룹: {df['Sequence'].unique().tolist()}")
print("처리×기간 평균:")
print(df.groupby(["Sequence", "Period"])["Score"].mean().round(2))

# 1. 혼합 효과 모형
model = smf.mixedlm("Score ~ Treatment + Period",
                    data=df, groups=df["Subject"])
result = model.fit()

print("\n" + "=" * 60)
print("[Step 1] 혼합 효과 모형 (피험자 = 랜덤 효과)")
print("=" * 60)
print(result.summary())

# 2. 이월 효과 보수적 점검: 기간 1 데이터만으로 두 순서 그룹 비교
g1 = df[(df["Period"] == 1) & (df["Sequence"] == "A->B")]["Score"]
g2 = df[(df["Period"] == 1) & (df["Sequence"] == "B->A")]["Score"]
# 두 순서 그룹은 기간 1에 각각 A, B를 받음 → 사실상 병행 비교
t, p = ttest_ind(g1, g2)
print("\n" + "=" * 60)
print("[Step 2] 기간 1 데이터만 사용한 단순 처리 비교 (이월 효과가 의심될 때 대안)")
print("=" * 60)
print(f"  Period=1 A(A->B): n={len(g1)}, mean={g1.mean():.2f}")
print(f"  Period=1 B(B->A): n={len(g2)}, mean={g2.mean():.2f}")
print(f"  독립 t-검정: t={t:.3f}, p={p:.4f}")
print("  → 혼합 모형 결과와 방향이 일치하면 이월 효과 영향이 작다고 판단할 수 있음")

# 3. 순서 그룹별 시계열 그림
fig, ax = plt.subplots(figsize=(7, 5))
for seq, g in df.groupby("Sequence"):
    m = g.groupby("Period")["Score"].mean()
    ax.plot(m.index, m.values, marker="o", label=seq)
ax.set_xticks([1, 2])
ax.set_xlabel("Period")
ax.set_ylabel("평균 통증 완화 점수")
ax.set_title("순서 그룹별 기간 평균 (이월 효과 시각 점검)")
ax.legend(title="Sequence")
plt.tight_layout()
plt.show()

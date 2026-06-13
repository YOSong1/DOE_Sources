# Chapter 19.5 Excel 활용 버전
# UI A/B의 2x2 교차 설계 데이터를 읽어
# 혼합 효과 모형 + 순서 그룹 시계열 그림 + 종합 결론 메시지를 한 번에 보여 줍니다.

from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

xlsx = Path(__file__).with_name("sample_data.xlsx")
df = pd.read_excel(xlsx)

print("=" * 60)
print("[Step 0] 데이터 구조 점검")
print("=" * 60)
print(df.head())
print(f"\n피험자 수: {df['Subject'].nunique()}, "
      f"순서 그룹: {sorted(df['Sequence'].unique())}")
print("Sequence × Period 평균 시간:")
print(df.groupby(["Sequence", "Period"])["Time"].mean().round(2))

# 혼합 효과 모형
model = smf.mixedlm("Time ~ Treatment + Period",
                    data=df, groups=df["Subject"])
result = model.fit()

print("\n" + "=" * 60)
print("[Step 1] 혼합 효과 모형 결과")
print("=" * 60)
print(result.summary())

# 효과 추출
coef_B = result.params.get("Treatment[T.B]", None)
p_B = result.pvalues.get("Treatment[T.B]", None)
coef_P = result.params.get("Period", None)
p_P = result.pvalues.get("Period", None)

print("\n[Step 2] 핵심 효과 요약")
if coef_B is not None:
    sign = "단축" if coef_B < 0 else "증가"
    print(f"  Treatment[T.B] = {coef_B:+.2f}초 (p={p_B:.4f})")
    print(f"  → UI B는 UI A 대비 평균 {abs(coef_B):.2f}초 {sign}")
if coef_P is not None:
    print(f"  Period       = {coef_P:+.2f}초 (p={p_P:.4f}) — 학습 효과 추정")

# 순서 그룹별 시계열 그림
fig, ax = plt.subplots(figsize=(7, 5))
for seq, g in df.groupby("Sequence"):
    m = g.groupby("Period")["Time"].mean()
    ax.plot(m.index, m.values, marker="o", label=seq)
ax.set_xticks([1, 2])
ax.set_xlabel("Period")
ax.set_ylabel("평균 과업 완료 시간 (초)")
ax.set_title("UI 교차 설계 — 순서 그룹별 기간 평균")
ax.legend(title="Sequence")
plt.tight_layout()
plt.show()

# 종합 권고
print("\n[종합 권고]")
if coef_B is not None and p_B < 0.05 and coef_B < 0:
    print("  UI B를 채택하는 것이 통계적으로 유의한 시간 단축으로 이어집니다.")
    print("  단, 학습 효과(Period 효과)와 분리되었는지 시계열 그림으로 함께 확인하세요.")
else:
    print("  UI 간 차이가 통계적으로 명확하지 않거나 방향이 반대입니다.")
    print("  추가 사용자 모집 또는 이월 효과 점검이 필요합니다.")

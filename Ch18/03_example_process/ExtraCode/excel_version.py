# Chapter 18.3 Excel 활용 버전
# 처리 수준 × 반복 구조의 Excel 데이터를 읽어
# ANOVA + 잔차 자유도 해석 + 반복의 역할을 출력합니다.

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

xlsx = Path(__file__).with_name("sample_data.xlsx")
df = pd.read_excel(xlsx)

print("=" * 60)
print("[Step 0] 데이터 구조 점검")
print("=" * 60)
print(df.head(8))
n_levels = df["ProcessTimeLevel"].nunique()
n_rep = df.groupby("ProcessTimeLevel").size().iloc[0]
print(f"\n수준 수 k={n_levels}, 처리당 반복 n={n_rep}, 총 관측치 N={len(df)}")

# 기술 통계
desc = df.groupby('ProcessTimeLevel')['Measurement'].agg(
    ['count', 'mean', 'std', 'min', 'max']).round(3)
print("\n[그룹별 기술 통계]")
print(desc)

# ANOVA
model = ols('Measurement ~ C(ProcessTimeLevel)', data=df).fit()
anova = sm.stats.anova_lm(model, typ=2)
print("\n" + "=" * 60)
print("[Step 1] 일원 ANOVA")
print("=" * 60)
print(anova)

# 자유도 해석 (반복의 역할)
df_treat = n_levels - 1
df_error = len(df) - n_levels
print(f"\n[Step 2] 자유도 해석")
print(f"  처리 자유도 df_treat = k - 1 = {df_treat}")
print(f"  오차 자유도 df_error = N - k = {df_error}")
print(f"  → 반복 n={n_rep}이 없었다면 df_error = 0, F-검정 자체가 불가능")

# 오차 평균제곱 → 처리당 표본평균의 표준오차
mse = anova.loc["Residual", "sum_sq"] / df_error
se_per_group = np.sqrt(mse / n_rep)
print(f"\n  MSE = {mse:.3f}, 처리 평균의 표준오차 = sqrt(MSE/n) = {se_per_group:.3f}")
print("  → 반복 n이 늘면 SE가 1/sqrt(n)로 감소 → 정밀도 향상")

# 시각화
plt.figure(figsize=(7, 5))
df.boxplot(by='ProcessTimeLevel', column='Measurement', grid=False)
plt.title('처리 수준별 측정값 분포 (5반복)')
plt.suptitle('')
plt.xlabel('ProcessTimeLevel')
plt.ylabel('Measurement')
plt.tight_layout()
plt.show()

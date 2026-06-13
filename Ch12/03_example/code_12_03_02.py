# code_12_03_02.py
# -*- coding: utf-8 -*-
"""
페이지: 12.3 예제로 이해: 반도체 식각 공정의 부분 요인 실험
설명: 주효과 계산, 교락 구조 분석, 회귀/ANOVA, 주효과도/파레토 차트,
      결과 종합 및 Fold-over 설계까지의 전체 분석 코드.

이 스크립트는 original_01.py 에서 정의된 df_design, factors 를 사용한다.
실제로 실행하려면 두 파일을 통합하거나 함수로 분리하여 호출해야 한다.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt

# ----- 주효과 계산 -----
effects = {}
for factor in factors:
    high = df_design[df_design[factor] == 1.0]['Y'].mean()
    low = df_design[df_design[factor] == -1.0]['Y'].mean()
    effects[factor] = high - low

print("\n주효과 (Main Effects):")
print("-" * 35)
for factor, effect in effects.items():
    print(f"  요인 {factor}: {effect:+.2f} nm/min")

# ----- 교락 구조 -----
print("\n교락(Aliasing) 구조:")
print("=" * 60)
print("정의 관계: I = ABD = ACE = BCDE")
print("-" * 60)

alias_structure = {
    'A': ['A', 'BD', 'CE', 'ABCDE'],
    'B': ['B', 'AD', 'ABCE', 'CDE'],
    'C': ['C', 'ABCD', 'AE', 'BDE'],
    'D': ['D', 'AB', 'ACDE', 'BCE'],
    'E': ['E', 'ABDE', 'AC', 'BCD'],
    'BC': ['BC', 'ACD', 'ABE', 'DE'],
    'BE': ['BE', 'ADE', 'ABC', 'CD'],
}

for effect, aliases in alias_structure.items():
    alias_str = ' = '.join(aliases)
    print(f"  [{alias_str}]")

# ----- 회귀 모형 + ANOVA -----
model = ols('Y ~ A + B + C + D + E', data=df_design).fit()

print("\n회귀 모형 요약:")
print("=" * 60)
print(model.summary())

anova_table = sm.stats.anova_lm(model, typ=2)

print("\nANOVA 테이블:")
print("=" * 60)
print(anova_table.to_string())

# ----- 주효과도 시각화 -----
fig, axes = plt.subplots(1, 5, figsize=(18, 4), sharey=True)
for i, factor in enumerate(factors):
    levels = [-1, 1]
    means = [df_design[df_design[factor] == lv]['Y'].mean() for lv in levels]
    axes[i].plot(levels, means, 'bo-', markersize=8, linewidth=2)
    axes[i].set_title(f'요인 {factor}', fontsize=13)
    axes[i].set_xlabel('수준')
    axes[i].set_xticks([-1, 1])
    axes[i].set_xticklabels(['-1 (낮음)', '+1 (높음)'], fontsize=9)
    axes[i].grid(True, alpha=0.3)

axes[0].set_ylabel('평균 식각률 (nm/min)', fontsize=11)
plt.suptitle('주효과 도표 (Main Effects Plot)', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()

# ----- 파레토 차트 -----
effect_abs = {k: abs(v) for k, v in effects.items()}
sorted_effects = dict(sorted(effect_abs.items(), key=lambda x: x[1], reverse=True))

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(
    list(sorted_effects.keys()),
    list(sorted_effects.values()),
    color=['#e74c3c' if v > 30 else '#3498db' for v in sorted_effects.values()]
)
ax.set_xlabel('효과의 절대값 (|Effect|)', fontsize=12)
ax.set_title('파레토 차트: 요인 효과 크기 비교', fontsize=14, fontweight='bold')
ax.axvline(x=30, color='red', linestyle='--', linewidth=1, label='유의성 기준선')
ax.legend()
ax.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
plt.show()

# ----- 결과 종합 -----
print("\n분석 결과 종합:")
print("=" * 60)
print(f"{'요인':<12} {'효과':<15} {'계수':<15} {'p-value':<12} {'유의성':<8}")
print("-" * 60)

p_values = model.pvalues[1:]  # Intercept 제외
for i, factor in enumerate(factors):
    effect = effects[factor]
    coef = effect / 2
    p_val = p_values.iloc[i]
    sig = "***" if p_val < 0.01 else ("**" if p_val < 0.05 else "ns")
    print(f"  {factor:<10} {effect:>+10.2f}    {coef:>+10.4f}     {p_val:>8.4f}    {sig}")

print("-" * 60)
print("유의성 코드: *** p<0.01, ** p<0.05, ns 유의하지 않음")

# ----- 최적 조건 -----
print("\n최적 조건 (식각률 최대화):")
print("=" * 50)
optimal = {
    'A (RF 전력)': '400 W (+1)',
    'B (가스 압력)': '300 mTorr (+1)',
    'C (가스 유량)': '100 sccm (+1)',
    'D (웨이퍼 온도)': '350 °C (+1)',
    'E (식각 시간)': '15 min (+1)'
}

for factor, value in optimal.items():
    print(f"  {factor}: {value}")

# 최적 조건에서의 예측값
y_pred_optimal = model.predict(pd.DataFrame({
    'A': [1], 'B': [1], 'C': [1], 'D': [1], 'E': [1]
}))
print(f"\n최적 조건에서의 예측 식각률: {y_pred_optimal.values[0]:.2f} nm/min")

# ----- Fold-over 설계 -----
df_foldover = df_design[factors].copy()
df_foldover[factors] = -df_foldover[factors]  # 모든 부호 반전

print("\nFold-over 설계 행렬:")
print(df_foldover.to_string(index=True))
print(f"\n원래 실험: 8회 + Fold-over: 8회 = 총 16회")
print("Fold-over를 통해 Resolution III → Resolution IV로 향상")

# -*- coding: utf-8 -*-
"""
페이지: 9.3 반복 측정 ANOVA
Excel 활용 버전: sample_memory_test.xlsx의 데이터(long format)로
- 와이드 변환과 long 유지 두 형식을 모두 다뤄봄
- Mauchly 구형성 검정 + Greenhouse-Geisser 보정
- 반복 ANOVA + Bonferroni 사후 검정
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import pandas as pd
import matplotlib.pyplot as plt
import pingouin as pg
import matplotlib
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_memory_test.xlsx'))
print(f"[Excel] long-format n = {len(df)} ({df['subject'].nunique()}명 × {df['time'].nunique()}시점)")

# 1) 와이드 변환 (피험자 × 시점)
wide = df.pivot(index='subject', columns='time', values='score')
print("\n와이드 형식:")
print(wide)
print("\n시점별 평균:", df.groupby('time')['score'].mean().to_dict())

# 2) Mauchly 구형성 검정
spher = pg.sphericity(df, dv='score', within='time', subject='subject')
print("\nMauchly 구형성 검정:")
print(spher)
if spher.pval < 0.05:
    print("  → 구형성 위배 → Greenhouse-Geisser 보정 p-값 사용 권장")
else:
    print("  → 구형성 가정 유지")

# 3) 반복 측정 ANOVA
aov = pg.rm_anova(dv='score', within='time', subject='subject',
                  data=df, detailed=True, correction='auto')
print("\n반복 측정 ANOVA:")
print(aov)

# 4) Bonferroni 보정 사후검정
print("\nBonferroni 보정 쌍별 t-검정:")
posthoc = pg.pairwise_tests(dv='score', within='time', subject='subject',
                            data=df, padjust='bonf')
print(posthoc[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']])

# 5) 시각화: 스파게티 + 박스플롯
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for subj in df['subject'].unique():
    sub = df[df['subject'] == subj]
    axes[0].plot(sub['time'], sub['score'], marker='o', alpha=0.4)
means = df.groupby('time')['score'].mean()
axes[0].plot(means.index, means.values, marker='o',
             linewidth=3, color='red', label='평균')
axes[0].set_title('개인별 변화 + 전체 평균')
axes[0].legend(); axes[0].grid(alpha=0.3)

df.boxplot(column='score', by='time', ax=axes[1])
axes[1].set_title('시점별 점수 분포')
axes[1].get_figure().suptitle('')
plt.tight_layout()
plt.show()

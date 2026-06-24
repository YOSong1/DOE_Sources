# code_17_05_solution.py
"""
17.5 연습 문제 해답: 새로운 교육용 소프트웨어의 효과 비교 (완전 무작위 설계, CRD)

세 가지 교육용 소프트웨어 버전(A, B, C)을 30명의 학생에게 10명씩 무작위로
할당한 뒤 얻은 과학 시험 점수를, 완전 무작위 설계(CRD)의 일원배치 모형으로
분석한다.

수행 단계
  [Step 0] 데이터 생성 및 구조 확인 (문제와 동일한 seed=999)
  [Step 1] statsmodels OLS 일원배치 모형 적합 + One-way ANOVA 표
  [Step 2] scipy f_oneway 교차 검증
  [Step 3] 유의수준 0.05 판정 및 결론 서술
  [Step 4] 유의할 경우 Tukey HSD 사후분석
  [Step 5] 시각화: 박스플롯 / 처리 평균 / 잔차 진단(4종)
  [Step 6] 최적 처리(가장 효과적인 버전) 도출 및 출력

라이브러리: numpy, pandas, scipy, statsmodels, matplotlib (seaborn 미사용)
그림은 본 스크립트와 같은 폴더에 PNG로 저장된다.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import f_oneway, shapiro, levene
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# ----------------------------------------------------------------------
# 한글 폰트 설정 (matplotlib 전용, seaborn 사용 안 함)
# ----------------------------------------------------------------------
plt.rc("font", family="Malgun Gothic")
plt.rc("axes", unicode_minus=False)

HERE = Path(__file__).resolve().parent
ALPHA = 0.05


# ======================================================================
# [Step 0] 가상 데이터 생성 및 구조 확인 (문제 코드 조각과 동일한 seed)
# ======================================================================
print("=" * 64)
print("[Step 0] 데이터 생성 및 구조 확인")
print("=" * 64)

np.random.seed(999)  # 재현성: 문제와 동일한 시드

# Version A: 평균 75, 표준편차 8 / B: 평균 82 / C: 평균 77 (각 10명)
score_A = np.random.normal(loc=75, scale=8, size=10)
score_B = np.random.normal(loc=82, scale=8, size=10)
score_C = np.random.normal(loc=77, scale=8, size=10)

# (선택) wide 형태로 데이터 확인
df_wide = pd.DataFrame(
    {"Version A": score_A, "Version B": score_B, "Version C": score_C}
)
print("\n[원자료 wide 형태]")
print(df_wide.round(2))

# 분석에는 tidy(long) 형태가 편하다: Version(처리) / Score(반응)
df = pd.DataFrame(
    {
        "Version": (["A"] * 10) + (["B"] * 10) + (["C"] * 10),
        "Score": np.concatenate([score_A, score_B, score_C]),
    }
)

print("\n[처리별 기술통계]")
desc = df.groupby("Version")["Score"].agg(["count", "mean", "std", "min", "max"])
print(desc.round(3))


# ======================================================================
# [Step 1] statsmodels 일원배치(처리효과) 모형 적합 + One-way ANOVA
# ======================================================================
print("\n" + "=" * 64)
print("[Step 1] 일원배치 모형 적합 및 분산분석(ANOVA)")
print("=" * 64)

# CRD 일원배치 모형: Score ~ C(Version)  (처리효과)
model = smf.ols("Score ~ C(Version)", data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

print("\n[One-way ANOVA 표 (statsmodels, Type II)]")
print(anova_table.round(4))

f_stat_sm = float(anova_table.loc["C(Version)", "F"])
p_value_sm = float(anova_table.loc["C(Version)", "PR(>F)"])
print(f"\n처리효과: F = {f_stat_sm:.4f}, p = {p_value_sm:.4f}")
print(f"결정계수 R^2 = {model.rsquared:.4f}")


# ======================================================================
# [Step 2] scipy f_oneway 교차 검증 (문제 요구사항)
# ======================================================================
print("\n" + "=" * 64)
print("[Step 2] scipy.stats.f_oneway 교차 검증")
print("=" * 64)

f_stat_sp, p_value_sp = f_oneway(score_A, score_B, score_C)
print(f"\nf_oneway 결과: F = {f_stat_sp:.4f}, p = {p_value_sp:.4f}")
print("=> statsmodels ANOVA와 동일한 F/p 값임을 확인 "
      f"(차이 {abs(f_stat_sm - f_stat_sp):.2e}).")


# ======================================================================
# [Step 3] 유의수준 0.05 판정 및 결론 서술
# ======================================================================
print("\n" + "=" * 64)
print("[Step 3] 유의수준 0.05 결과 해석")
print("=" * 64)

is_significant = p_value_sm < ALPHA
if is_significant:
    print(f"\np = {p_value_sm:.4f} < {ALPHA} 이므로 귀무가설(모든 버전의 평균이 같다)을 기각한다.")
    print("=> 소프트웨어 버전 간 평균 시험 점수에 통계적으로 유의미한 차이가 있다.")
else:
    print(f"\np = {p_value_sm:.4f} >= {ALPHA} 이므로 귀무가설을 기각하지 못한다.")
    print("=> 소프트웨어 버전 간 평균 점수 차이가 통계적으로 유의하다고 보기 어렵다.")


# ======================================================================
# [Step 4] 사후분석 (유의할 경우 Tukey HSD)
# ======================================================================
print("\n" + "=" * 64)
print("[Step 4] 사후분석 (Tukey HSD)")
print("=" * 64)

tukey = None
if is_significant:
    tukey = pairwise_tukeyhsd(endog=df["Score"], groups=df["Version"], alpha=ALPHA)
    print("\n[Tukey HSD 다중비교 결과]")
    print(tukey)
    print("\nreject=True 인 쌍이 유의수준 0.05에서 서로 다른 버전 쌍이다.")
else:
    print("\nANOVA가 유의하지 않아 사후분석을 생략한다.")


# ======================================================================
# [Step 5] 시각화: 박스플롯 / 처리 평균 / 잔차 진단
# ======================================================================
print("\n" + "=" * 64)
print("[Step 5] 시각화 및 PNG 저장")
print("=" * 64)

versions = ["A", "B", "C"]
groups = [df.loc[df["Version"] == v, "Score"].values for v in versions]
means = [g.mean() for g in groups]
sems = [g.std(ddof=1) / np.sqrt(len(g)) for g in groups]
colors = ["#4C72B0", "#DD8452", "#55A868"]

# ---- 그림 1: 박스플롯 + 처리 평균(오차막대) ----
fig1, axes = plt.subplots(1, 2, figsize=(12, 5))

bp = axes[0].boxplot(groups, tick_labels=[f"Version {v}" for v in versions],
                     patch_artist=True, showmeans=True)
for patch, c in zip(bp["boxes"], colors):
    patch.set_facecolor(c)
    patch.set_alpha(0.6)
axes[0].set_title("교육용 SW 버전별 시험 점수 분포 (박스플롯)")
axes[0].set_xlabel("소프트웨어 버전")
axes[0].set_ylabel("시험 점수")
axes[0].grid(axis="y", alpha=0.3)

axes[1].bar([f"Version {v}" for v in versions], means, yerr=sems,
            capsize=8, color=colors, alpha=0.8, edgecolor="black")
for i, m in enumerate(means):
    axes[1].text(i, m + 0.5, f"{m:.1f}", ha="center", va="bottom", fontweight="bold")
axes[1].set_title("버전별 평균 점수 (오차막대 = 표준오차)")
axes[1].set_xlabel("소프트웨어 버전")
axes[1].set_ylabel("평균 시험 점수")
axes[1].grid(axis="y", alpha=0.3)

fig1.tight_layout()
png1 = HERE / "code_17_05_solution_boxplot.png"
fig1.savefig(png1, dpi=120)
print(f"  저장: {png1.name}")

# ---- 그림 2: 잔차 진단 (4종) ----
resid = model.resid
fitted = model.fittedvalues

fig2, ax = plt.subplots(2, 2, figsize=(12, 9))

# (1) 적합값 vs 잔차
ax[0, 0].scatter(fitted, resid, color="#4C72B0", alpha=0.8, edgecolor="black")
ax[0, 0].axhline(0, color="red", linestyle="--")
ax[0, 0].set_title("적합값 vs 잔차 (등분산성 점검)")
ax[0, 0].set_xlabel("적합값(처리 평균)")
ax[0, 0].set_ylabel("잔차")
ax[0, 0].grid(alpha=0.3)

# (2) 잔차 Q-Q plot (정규성 점검)
sm.qqplot(resid, line="s", ax=ax[0, 1])
ax[0, 1].set_title("잔차 Q-Q Plot (정규성 점검)")

# (3) 잔차 히스토그램
ax[1, 0].hist(resid, bins=8, color="#55A868", alpha=0.8, edgecolor="black")
ax[1, 0].set_title("잔차 히스토그램")
ax[1, 0].set_xlabel("잔차")
ax[1, 0].set_ylabel("빈도")
ax[1, 0].grid(alpha=0.3)

# (4) 처리별 잔차 (산점도)
for i, v in enumerate(versions):
    r = resid[df["Version"] == v]
    ax[1, 1].scatter([v] * len(r), r, color=colors[i], alpha=0.8, edgecolor="black")
ax[1, 1].axhline(0, color="red", linestyle="--")
ax[1, 1].set_title("처리별 잔차 분포")
ax[1, 1].set_xlabel("소프트웨어 버전")
ax[1, 1].set_ylabel("잔차")
ax[1, 1].grid(alpha=0.3)

fig2.suptitle("잔차 진단 (일원배치 모형 가정 검토)", fontsize=14)
fig2.tight_layout()
png2 = HERE / "code_17_05_solution_residuals.png"
fig2.savefig(png2, dpi=120)
print(f"  저장: {png2.name}")

plt.close("all")

# 참고: 모형 가정 검정(정규성/등분산성) 보조 출력
sw_stat, sw_p = shapiro(resid)
lev_stat, lev_p = levene(*groups)
print(f"\n[모형 가정 점검]")
print(f"  잔차 정규성(Shapiro-Wilk): W={sw_stat:.4f}, p={sw_p:.4f} "
      f"({'정규성 만족' if sw_p >= ALPHA else '정규성 의심'})")
print(f"  등분산성(Levene):          stat={lev_stat:.4f}, p={lev_p:.4f} "
      f"({'등분산 만족' if lev_p >= ALPHA else '등분산 의심'})")


# ======================================================================
# [Step 6] 최적 처리(가장 효과적인 버전) 도출
# ======================================================================
print("\n" + "=" * 64)
print("[Step 6] 최적 처리 도출")
print("=" * 64)

best_idx = int(np.argmax(means))
best_version = versions[best_idx]
best_mean = means[best_idx]

print("\n[버전별 평균 점수]")
for v, m in zip(versions, means):
    mark = "  <== 최고" if v == best_version else ""
    print(f"  Version {v}: {m:.2f}점{mark}")

print(f"\n=> 가장 효과적인 처리: Version {best_version} (평균 {best_mean:.2f}점)")

if is_significant and tukey is not None:
    # Tukey 결과에서 최적 버전이 유의하게 우월한 상대 파악
    summary = tukey.summary()
    rows = summary.data[1:]  # 헤더 제외
    superior_to = []
    for g1, g2, _, _, _, _, reject in rows:
        if str(reject) == "True":
            if g1 == best_version:
                superior_to.append(g2)
            elif g2 == best_version:
                superior_to.append(g1)
    if superior_to:
        print(f"   Tukey HSD 기준 Version {best_version} 은(는) "
              f"Version {', '.join(sorted(set(superior_to)))} 보다 유의하게 높다.")
    else:
        print(f"   다만 Tukey HSD에서 Version {best_version}이 다른 버전보다 "
              "유의하게 높다고 단정하기는 어렵다.")
    print("   -> 통계적 근거와 평균 점수를 종합할 때 이 버전을 채택할 것을 권장한다.")
else:
    print("   다만 ANOVA가 유의하지 않으므로, 평균이 가장 높더라도 "
          "버전 간 차이가 통계적으로 입증되었다고 보기는 어렵다.")

print("\n[완료] 모든 분석 단계가 정상적으로 수행되었습니다.")

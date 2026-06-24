# code_16_05_solution.py
"""16.5 연습 문제 해답: 신소재 인장 강도 최적화를 위한 Box-Behnken 설계(BBD) 분석

이 스크립트는 외부 xlsx 파일에 의존하지 않는 '자기완결형' 해답이다.
문제에서 제시한 데이터 생성 코드(seed=888)를 그대로 포함하여 3요인 BBD
15회 실험 데이터를 재현한 뒤, 다음 과제를 모두 수행한다.

  1) Box-Behnken 설계점/데이터 생성 및 확인
  2) statsmodels OLS 로 2차 응답표면 모델(주효과 + 상호작용 + 제곱항) 적합
  3) ANOVA 표 출력 및 유의효과(alpha=0.05) 식별
  4) 등고선/3D 반응표면 시각화 + 잔차 진단 플롯 (PNG 저장)
  5) 최적 조건(정상점, scipy.optimize) 도출 및 보고

시각화는 matplotlib 만 사용한다(seaborn 미사용). 한글 폰트는 'Malgun Gothic'.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from scipy.optimize import minimize
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path

# --- matplotlib 한글 폰트 및 음수 부호 설정 ---
plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# 그림 저장 위치(이 스크립트와 같은 폴더)
OUT_DIR = Path(__file__).resolve().parent


# ======================================================================
# [1단계] Box-Behnken 설계점 생성 및 데이터 구성
# ======================================================================
print("=" * 64)
print("[1단계] Box-Behnken 설계점 생성 및 실험 데이터 구성")
print("=" * 64)

# --- 1-1. Box-Behnken 설계점 (3요인, 15점 - 코드화된 값) ---
design_points_coded = [
    [-1, -1,  0], [ 1, -1,  0], [-1,  1,  0], [ 1,  1,  0],
    [-1,  0, -1], [ 1,  0, -1], [-1,  0,  1], [ 1,  0,  1],
    [ 0, -1, -1], [ 0,  1, -1], [ 0, -1,  1], [ 0,  1,  1],
    [ 0,  0,  0], [ 0,  0,  0], [ 0,  0,  0]   # 중심점 3회 반복
]
df = pd.DataFrame(design_points_coded, columns=['X1', 'X2', 'X3'])

# --- 1-2. 코드화 값 -> 실제 요인 수준 변환 ---
# 열처리 온도 (X1): 450(-1), 500(0), 550(+1)
df['Heat_Treatment_Temp'] = df['X1'].apply(lambda x: 500 + x * 50)
# 합금 원소 A 첨가량 (X2): 1.0%(-1), 1.5%(0), 2.0%(+1)
df['Alloy_A_Percentage'] = df['X2'].apply(lambda x: 1.5 + x * 0.5)
# 압연 속도 (X3): 5(-1), 10(0), 15(+1) m/min
df['Rolling_Speed'] = df['X3'].apply(lambda x: 10 + x * 5)

# --- 1-3. 가상의 인장 강도(반응값) 생성 (문제와 동일 seed) ---
np.random.seed(888)
base_strength = 650

X1c, X2c, X3c = df['X1'], df['X2'], df['X3']
tensile_strength_values = (
    base_strength
    + 20 * X1c
    + 15 * X2c
    + 5 * X3c
    - 8 * X1c**2
    - 6 * X2c**2
    + 4 * X1c * X2c
    + np.random.normal(0, 5, len(df))
)
df['Tensile_Strength'] = np.round(tensile_strength_values, 1)

# 설계점 + 반응값 확인
print("\n[설계점(코드화) + 실제 수준 + 반응값] 전체 15회 실험:")
print(df[['X1', 'X2', 'X3',
          'Heat_Treatment_Temp', 'Alloy_A_Percentage',
          'Rolling_Speed', 'Tensile_Strength']].to_string(index=False))
print(f"\n총 실험 수: {len(df)} (중심점 3회 포함)")
print(f"반응값 요약: 평균={df['Tensile_Strength'].mean():.2f} MPa, "
      f"표준편차={df['Tensile_Strength'].std():.2f}, "
      f"최소={df['Tensile_Strength'].min():.1f}, "
      f"최대={df['Tensile_Strength'].max():.1f}")


# ======================================================================
# [2단계] 2차 응답표면 모델(RSM) 적합
# ======================================================================
print("\n" + "=" * 64)
print("[2단계] 2차 응답표면 모델 적합 (주효과 + 상호작용 + 제곱항)")
print("=" * 64)

# 코드화 변수(X1, X2, X3)를 그대로 사용한다.
formula = (
    "Tensile_Strength ~ "
    "X1 + X2 + X3 "
    "+ X1:X2 + X1:X3 + X2:X3 "
    "+ I(X1**2) + I(X2**2) + I(X3**2)"
)
model = smf.ols(formula, data=df).fit()
print(model.summary())


# ======================================================================
# [3단계] ANOVA 표 및 유의효과(alpha=0.05) 식별
# ======================================================================
print("\n" + "=" * 64)
print("[3단계] ANOVA 표 및 유의효과 식별 (alpha = 0.05)")
print("=" * 64)

alpha = 0.05

# 타입 II ANOVA 표
anova_tbl = anova_lm(model, typ=2)
print("\n[ANOVA 표 (Type II)]")
print(anova_tbl)

# 회귀계수 기준 유의 항 식별 (절편 제외)
pvals = model.pvalues.drop('Intercept')
sig_terms = pvals[pvals < alpha]
nonsig_terms = pvals[pvals >= alpha]

print(f"\n[유의한 항 (p < {alpha})]")
if len(sig_terms) == 0:
    print("  (유의한 항 없음)")
else:
    for term, p in sig_terms.items():
        print(f"  - {term:<14s}: coef={model.params[term]:+9.4f}, p={p:.4f}")

print(f"\n[유의하지 않은 항 (p >= {alpha})]")
for term, p in nonsig_terms.items():
    print(f"  - {term:<14s}: coef={model.params[term]:+9.4f}, p={p:.4f}")

print(f"\n[모델 적합도]")
print(f"  R-squared      = {model.rsquared:.4f}")
print(f"  Adj. R-squared = {model.rsquared_adj:.4f}")
print(f"  F-statistic    = {model.fvalue:.3f}  (p = {model.f_pvalue:.3e})")
print("  해석: R^2 가 1에 가깝고 모델 F검정 p-값이 작을수록 적합이 우수하다.")
print("        제곱항(X1^2, X2^2)이 유의하면 곡률(최적점)이 존재함을 의미한다.")


# ======================================================================
# [4단계] 최적 조건(정상점) 탐색
# ======================================================================
print("\n" + "=" * 64)
print("[4단계] 인장 강도를 최대화하는 최적 조건 탐색")
print("=" * 64)

b = model.params.to_dict()


def predict_strength(x1, x2, x3):
    """적합 모델로 코드화 조건(x1,x2,x3)의 인장 강도를 예측."""
    return (
        b["Intercept"]
        + b["X1"] * x1 + b["X2"] * x2 + b["X3"] * x3
        + b["X1:X2"] * x1 * x2 + b["X1:X3"] * x1 * x3 + b["X2:X3"] * x2 * x3
        + b["I(X1 ** 2)"] * x1**2
        + b["I(X2 ** 2)"] * x2**2
        + b["I(X3 ** 2)"] * x3**2
    )


# scipy.optimize.minimize 로 -강도 최소화 = 강도 최대화
# 여러 시작점에서 최적화하여 전역 최적에 가깝게 탐색
best = None
for x0 in [(0, 0, 0), (1, 1, 1), (-1, -1, -1), (0.5, 0.5, 0)]:
    res = minimize(lambda v: -predict_strength(*v), x0=x0,
                   bounds=[(-1, 1), (-1, 1), (-1, 1)])
    if best is None or (-res.fun) > (-best.fun):
        best = res

xs = best.x
opt_strength = -best.fun

# 코드화 -> 실제 단위 변환
real_T = 500 + xs[0] * 50
real_A = 1.5 + xs[1] * 0.5
real_S = 10 + xs[2] * 5

print(f"\n[최적 코드화 조건]")
print(f"  X1 = {xs[0]:+.4f}, X2 = {xs[1]:+.4f}, X3 = {xs[2]:+.4f}")
print(f"\n[최적 실제 조건]")
print(f"  열처리 온도   : {real_T:7.2f} °C")
print(f"  합금 A 첨가량 : {real_A:7.3f} %")
print(f"  압연 속도     : {real_S:7.3f} m/min")
print(f"\n[예측 최대 인장 강도] : {opt_strength:.2f} MPa")


# ======================================================================
# [5단계] 시각화 - 등고선 / 3D 반응표면 + 잔차 진단
# ======================================================================
print("\n" + "=" * 64)
print("[5단계] 시각화 및 잔차 진단 (PNG 저장)")
print("=" * 64)

# 그리드 생성 (X3 는 최적값으로 고정)
grid = np.linspace(-1, 1, 60)
G1, G2 = np.meshgrid(grid, grid)
Z = predict_strength(G1, G2, xs[2])

# --- 5-1. 등고선도 + 3D 반응표면 (X1-X2 평면, X3=최적값 고정) ---
fig = plt.figure(figsize=(13, 5.5))

ax1 = fig.add_subplot(1, 2, 1)
cf = ax1.contourf(G1, G2, Z, levels=20, cmap='viridis')
cl = ax1.contour(G1, G2, Z, levels=10, colors='white', linewidths=0.6)
ax1.clabel(cl, inline=True, fontsize=7, fmt='%.0f')
fig.colorbar(cf, ax=ax1, label='예측 인장 강도 (MPa)')
ax1.scatter(xs[0], xs[1], color='red', marker='*', s=220,
            edgecolor='black', zorder=5, label='최적점')
ax1.scatter(df['X1'], df['X2'], color='black', marker='o', s=25,
            alpha=0.6, label='실험 설계점')
ax1.set_xlabel('X1 (열처리 온도, 코드화)')
ax1.set_ylabel('X2 (합금 A 첨가량, 코드화)')
ax1.set_title(f'등고선도 (X3=압연속도 {xs[2]:+.2f} 고정)')
ax1.legend(loc='lower right', fontsize=8)

ax2 = fig.add_subplot(1, 2, 2, projection='3d')
surf = ax2.plot_surface(G1, G2, Z, cmap='viridis', alpha=0.9,
                        linewidth=0, antialiased=True)
ax2.set_xlabel('X1 (온도)')
ax2.set_ylabel('X2 (첨가량)')
ax2.set_zlabel('인장 강도 (MPa)')
ax2.set_title('3D 반응 표면')
fig.colorbar(surf, ax=ax2, shrink=0.6, label='MPa')

fig.suptitle('신소재 인장 강도 응답 표면 (Box-Behnken 설계)', fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.96])
png_rsm = OUT_DIR / 'code_16_05_solution_response_surface.png'
fig.savefig(png_rsm, dpi=120)
plt.close(fig)
print(f"  저장: {png_rsm.name}")

# --- 5-2. 잔차 진단 플롯 ---
resid = model.resid
fitted = model.fittedvalues

fig2, axes = plt.subplots(1, 3, figsize=(15, 4.5))

# (a) 잔차 vs 적합값
axes[0].scatter(fitted, resid, color='steelblue', edgecolor='k')
axes[0].axhline(0, color='red', linestyle='--', linewidth=1)
axes[0].set_xlabel('적합값 (Fitted)')
axes[0].set_ylabel('잔차 (Residual)')
axes[0].set_title('(a) 잔차 vs 적합값')

# (b) 정규 Q-Q 플롯
sm.qqplot(resid, line='45', fit=True, ax=axes[1])
axes[1].set_title('(b) 잔차 정규 Q-Q 플롯')

# (c) 잔차 히스토그램
axes[2].hist(resid, bins=8, color='skyblue', edgecolor='k')
axes[2].set_xlabel('잔차')
axes[2].set_ylabel('빈도')
axes[2].set_title('(c) 잔차 히스토그램')

fig2.suptitle('잔차 진단 (모델 가정 점검)', fontsize=13)
fig2.tight_layout(rect=[0, 0, 1, 0.95])
png_resid = OUT_DIR / 'code_16_05_solution_residuals.png'
fig2.savefig(png_resid, dpi=120)
plt.close(fig2)
print(f"  저장: {png_resid.name}")

# 정규성 검정(Shapiro-Wilk)으로 잔차 진단 보조
sw_stat, sw_p = stats.shapiro(resid)
print(f"\n[잔차 정규성 검정 (Shapiro-Wilk)]")
print(f"  통계량 W = {sw_stat:.4f}, p-값 = {sw_p:.4f}")
if sw_p >= alpha:
    print(f"  -> p >= {alpha}: 잔차가 정규성을 만족한다고 볼 수 있다.")
else:
    print(f"  -> p < {alpha}: 잔차 정규성 가정이 의심된다.")

print("\n" + "=" * 64)
print("[완료] 모든 단계 수행 종료.")
print("=" * 64)

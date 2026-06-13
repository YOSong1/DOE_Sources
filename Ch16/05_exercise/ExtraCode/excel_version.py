# Chapter 16.5 Excel 활용 버전
# sample_data.xlsx에 미리 생성된 15회 BBD 실험 데이터를 읽어
# (1) statsmodels로 2차 다항 회귀 적합
# (2) 유의 항 식별과 R² 보고
# (3) scipy.optimize로 인장 강도를 최대화하는 코드 조건 탐색

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.optimize import minimize
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

xlsx = Path(__file__).with_name("sample_data.xlsx")
df = pd.read_excel(xlsx)

print("=" * 60)
print("[Step 0] 데이터 구조 점검")
print("=" * 60)
print(df.head())
print(f"\n총 실험 수: {len(df)} (중심점 3회 포함 가정)")
print(f"반응값 통계: 평균={df['Tensile_Strength'].mean():.1f} MPa, "
      f"표준편차={df['Tensile_Strength'].std():.1f}")

# 코드화 변수가 이미 시트에 있으므로 그대로 사용
formula = ("Tensile_Strength ~ X1_coded + X2_coded + X3_coded "
           "+ I(X1_coded**2) + I(X2_coded**2) + I(X3_coded**2) "
           "+ X1_coded:X2_coded + X1_coded:X3_coded + X2_coded:X3_coded")
model = smf.ols(formula, data=df).fit()

print("\n" + "=" * 60)
print("[Step 1] 2차 다항 회귀 모형 적합")
print("=" * 60)
print(model.summary())

# 유의 항 (α = 0.05)
sig = model.pvalues[model.pvalues < 0.05]
print("\n[유의한 항 (p < 0.05)]")
print(sig)

# 최적화
b = model.params.to_dict()
def predict(x1, x2, x3):
    return (b["Intercept"]
            + b["X1_coded"]*x1 + b["X2_coded"]*x2 + b["X3_coded"]*x3
            + b["I(X1_coded ** 2)"]*x1**2
            + b["I(X2_coded ** 2)"]*x2**2
            + b["I(X3_coded ** 2)"]*x3**2
            + b["X1_coded:X2_coded"]*x1*x2
            + b["X1_coded:X3_coded"]*x1*x3
            + b["X2_coded:X3_coded"]*x2*x3)

res = minimize(lambda v: -predict(*v),
               x0=[0, 0, 0],
               bounds=[(-1, 1), (-1, 1), (-1, 1)])
xs = res.x

# 실제 단위
real_T = 500 + xs[0] * 50
real_A = 1.5 + xs[1] * 0.5
real_S = 10 + xs[2] * 5

print("\n" + "=" * 60)
print("[Step 2] 인장 강도를 최대화하는 최적 조건")
print("=" * 60)
print(f"  코드: X1={xs[0]:+.3f}, X2={xs[1]:+.3f}, X3={xs[2]:+.3f}")
print(f"  실제: 열처리 온도 {real_T:.1f}°C, 합금 A {real_A:.2f}%, "
      f"압연 속도 {real_S:.2f} m/min")
print(f"  예측 인장 강도: {-res.fun:.1f} MPa")
print(f"  모델 R² = {model.rsquared:.3f}, adj R² = {model.rsquared_adj:.3f}")

print("\n[해석 메시지] R²가 충분히 높고 (>0.9 권장) 잔차가 정규성을 "
      "만족할 때 위 최적 조건의 신뢰도가 가장 높습니다.")

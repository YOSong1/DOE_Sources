# Chapter 16.3 Excel 활용 버전
# sample_data.xlsx에서 BBD 데이터를 읽어 회귀 계수와 최적 조건을 계산하고,
# 효과 크기 / 곡률 부호 / 최적 조건의 실제 단위 환산까지 함께 출력해
# 사고 흐름을 따라가도록 구성했습니다.

from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# 0. 데이터 로드
xlsx = Path(__file__).with_name("sample_data.xlsx")
df = pd.read_excel(xlsx)

print("=" * 60)
print("[Step 0] 데이터 구조 점검")
print("=" * 60)
print(df.head())
print(f"\n총 실험 수: {len(df)}, 중심점 수: {((df['X1_coded']==0) & (df['X2_coded']==0) & (df['X3_coded']==0)).sum()}")

# 1. 설계 행렬
n = len(df)
X = np.ones((n, 10))
X[:, 1] = df["X1_coded"]; X[:, 2] = df["X2_coded"]; X[:, 3] = df["X3_coded"]
X[:, 4] = df["X1_coded"] * df["X2_coded"]
X[:, 5] = df["X1_coded"] * df["X3_coded"]
X[:, 6] = df["X2_coded"] * df["X3_coded"]
X[:, 7] = df["X1_coded"] ** 2
X[:, 8] = df["X2_coded"] ** 2
X[:, 9] = df["X3_coded"] ** 2
Y = df["Y_TasteScore"].values

# 2. 회귀 계수
beta = np.linalg.inv(X.T @ X) @ X.T @ Y
labels = ["β0 (Intercept)", "β1 (Temp)", "β2 (Time)", "β3 (Beans)",
          "β12 (T·t)", "β13 (T·B)", "β23 (t·B)",
          "β11 (T²)", "β22 (t²)", "β33 (B²)"]

print("\n" + "=" * 60)
print("[Step 1] 회귀 계수와 효과 크기")
print("=" * 60)
coef_df = pd.DataFrame({"term": labels, "coef": beta})
coef_df["|coef|"] = coef_df["coef"].abs()
print(coef_df.to_string(index=False))

# 3. 1차 효과 / 2차 효과 / 상호작용 분리 해석
print("\n[해석 메시지]")
linear = coef_df.iloc[1:4]
quad = coef_df.iloc[7:10]
inter = coef_df.iloc[4:7]
top_linear = linear.loc[linear["|coef|"].idxmax(), "term"]
print(f"  - 1차 효과가 가장 큰 항: {top_linear}")
print(f"  - 2차항 부호: T²={beta[7]:+.2f}, t²={beta[8]:+.2f}, B²={beta[9]:+.2f}")
print("    (음수일수록 ∩ 모양 → 중간 최적점 존재)")

# 4. 최적화 (경계 제약 포함)
def neg_yhat(x):
    v = np.array([1, x[0], x[1], x[2],
                  x[0]*x[1], x[0]*x[2], x[1]*x[2],
                  x[0]**2, x[1]**2, x[2]**2])
    return -(v @ beta)

res = minimize(neg_yhat, x0=[0, 0, 0],
               bounds=[(-1, 1), (-1, 1), (-1, 1)])
xs = res.x
y_max = -res.fun

# 5. 실제 단위 환산 (Excel에 들어 있는 범위에서 자동 계산)
def to_real(col_real, col_coded, code):
    lo = df.loc[df[col_coded] == -1, col_real].iloc[0]
    hi = df.loc[df[col_coded] == 1, col_real].iloc[0]
    return lo + (hi - lo) * (code + 1) / 2

real_T = to_real("X1_Temperature_C", "X1_coded", xs[0])
real_t = to_real("X2_Time_sec", "X2_coded", xs[1])
real_B = to_real("X3_Beans_g", "X3_coded", xs[2])

print("\n" + "=" * 60)
print("[Step 2] 경계 제약 하의 최적 조건")
print("=" * 60)
print(f"  코드값: X1={xs[0]:+.3f}, X2={xs[1]:+.3f}, X3={xs[2]:+.3f}")
print(f"  실제값: 온도 {real_T:.2f}°C, 시간 {real_t:.2f}초, 원두 {real_B:.2f}g")
print(f"  예측 맛 점수: {y_max:.2f}")
print("\n[해석 메시지] 무제약 정상점은 설계 영역 밖일 수 있으므로")
print("              반드시 경계 제약 최적화 결과를 채택해야 합니다.")

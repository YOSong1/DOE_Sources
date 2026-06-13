import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.1 이산형 분포 개요 — Excel 활용 버전
# sample_data.xlsx의 'dice' 시트를 읽어 경험적 PMF, 기댓값, 분산을 계산하고
# 이론값(공정한 주사위)과 비교한다.

import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
xlsx = os.path.join(HERE, "sample_data.xlsx")

print("=== [1] Excel 데이터 구조 ===")
df = pd.read_excel(xlsx, sheet_name="dice")
print(df)

# 경험적 PMF
n_total = df["observed"].sum()
df["p_hat"] = df["observed"] / n_total
print(f"\n총 관측 횟수 N = {n_total}")
print(df)

# 항별 분해된 E[X] 계산
print("\n=== [2] 기댓값 항별 계산 (k * p_hat) ===")
df["k*p"] = df["value"] * df["p_hat"]
for _, row in df.iterrows():
    print(f"  {int(row['value'])} * {row['p_hat']:.4f} = {row['k*p']:.4f}")
E_hat = df["k*p"].sum()
print(f"E_hat[X] = {E_hat:.4f}")

# 분산
print("\n=== [3] 분산 항별 계산 ((k-E)^2 * p_hat) ===")
df["sq_dev"] = (df["value"] - E_hat) ** 2
df["term"] = df["sq_dev"] * df["p_hat"]
for _, row in df.iterrows():
    print(f"  (k={int(row['value'])} - E={E_hat:.3f})^2 * {row['p_hat']:.4f} = {row['term']:.4f}")
Var_hat = df["term"].sum()
SD_hat = np.sqrt(Var_hat)
print(f"Var_hat = {Var_hat:.4f}, SD_hat = {SD_hat:.4f}")

# 이론값(공정한 주사위) 비교
E_theo = 3.5
Var_theo = 35/12
print("\n=== [4] 이론값과 비교 (공정한 주사위) ===")
print(f"  E[X]   이론={E_theo:.4f}, 경험={E_hat:.4f}, 차이={E_hat-E_theo:+.4f}")
print(f"  Var(X) 이론={Var_theo:.4f}, 경험={Var_hat:.4f}, 차이={Var_hat-Var_theo:+.4f}")

# PMF 합이 1인지 확인 (정규화 조건)
print(f"\n=== [5] 정규화 확인: sum(p_hat) = {df['p_hat'].sum():.6f} (반드시 1.0) ===")

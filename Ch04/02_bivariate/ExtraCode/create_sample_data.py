"""
4.2 2차원 확률 변수 - 샘플 데이터 생성 스크립트
======================================================
주제: 성인 200명의 키(X, cm)와 몸무게(Y, kg) 측정값
- 2차원 정규 분포에서 표본 추출 (ρ ≈ 0.7, 양의 상관)
- 결합 분포, 주변 분포, 조건부 분포 학습용
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import numpy as np
import pandas as pd

OUTPUT = os.path.join(os.path.dirname(__file__), "sample_data.xlsx")

np.random.seed(42)

mu = [170.0, 65.0]                  # 평균 키 170cm, 몸무게 65kg
sigma_h, sigma_w = 8.0, 10.0
rho = 0.7
cov = [
    [sigma_h ** 2, rho * sigma_h * sigma_w],
    [rho * sigma_h * sigma_w, sigma_w ** 2],
]

samples = np.random.multivariate_normal(mu, cov, size=200)
height = samples[:, 0].round(1)
weight = samples[:, 1].round(1)

df = pd.DataFrame({
    "사람ID": [f"P{i:03d}" for i in range(1, 201)],
    "키_cm": height,
    "몸무게_kg": weight,
})

df.to_excel(OUTPUT, index=False, sheet_name="키몸무게")
print(f"샘플 데이터 저장 완료: {OUTPUT}")
print(df.head())
print(f"\n표본 평균: 키={height.mean():.2f}, 몸무게={weight.mean():.2f}")
print(f"표본 상관계수: {np.corrcoef(height, weight)[0, 1]:.4f}  (목표 ≈ 0.7)")

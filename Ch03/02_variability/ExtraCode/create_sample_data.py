"""
3.2 데이터 변동성 - 샘플 데이터 생성 스크립트
====================================================
주제: 두 공장(A, B)에서 측정한 부품 직경(mm) 데이터
- 두 공장의 평균 직경은 거의 같지만, 변동성(분산/표준편차)이 크게 다름
- A 공장: 정밀 공정 (낮은 변동성)
- B 공장: 일반 공정 (높은 변동성)
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

np.random.seed(2024)

# A 공장: 평균 50mm, 표준편차 0.3 (정밀)
factory_A = np.round(np.random.normal(50.0, 0.3, 25), 3)

# B 공장: 평균 50mm, 표준편차 1.5 (일반)
factory_B = np.round(np.random.normal(50.0, 1.5, 25), 3)

df = pd.DataFrame({
    "측정번호": np.arange(1, 26),
    "A공장_직경_mm": factory_A,
    "B공장_직경_mm": factory_B,
})

df.to_excel(OUTPUT, index=False, sheet_name="공정데이터")
print(f"샘플 데이터 저장 완료: {OUTPUT}")
print(df.head())
print(f"\nA공장 평균: {factory_A.mean():.3f}, 표준편차(표본): {factory_A.std(ddof=1):.3f}")
print(f"B공장 평균: {factory_B.mean():.3f}, 표준편차(표본): {factory_B.std(ddof=1):.3f}")

"""
4.1 1차원 확률 변수 - 샘플 데이터 생성 스크립트
======================================================
주제: 주사위 600회 굴림 실험 결과 (1차원 이산형 확률 변수)
- '눈의 수' X 에 대한 경험적 PMF/CDF/E[X]/Var(X) 추정에 사용
- 이론값(E[X]=3.5, Var(X)=2.9167)과 비교
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

# 공정한 주사위 600회
n_rolls = 600
rolls = np.random.randint(1, 7, size=n_rolls)

df = pd.DataFrame({
    "시행번호": np.arange(1, n_rolls + 1),
    "주사위눈": rolls,
})

# 빈도표
freq = (pd.Series(rolls).value_counts().sort_index()
        .rename_axis("눈의수").reset_index(name="빈도"))
freq["상대빈도"] = freq["빈도"] / n_rolls

with pd.ExcelWriter(OUTPUT) as writer:
    df.to_excel(writer, index=False, sheet_name="굴림결과")
    freq.to_excel(writer, index=False, sheet_name="빈도표")

print(f"샘플 데이터 저장 완료: {OUTPUT}")
print("\n빈도표:")
print(freq)
print(f"\n표본 평균: {rolls.mean():.4f}  (이론값 3.5)")
print(f"표본 분산: {rolls.var(ddof=0):.4f}  (이론값 2.9167)")

"""
3.4 데이터의 표준화 - 샘플 데이터 생성 스크립트
======================================================
주제: 학생 20명의 과목별 점수
- 국어, 영어, 수학, 과학 4과목
- 각 과목 평균/표준편차가 일부러 다르도록 구성 (Z-점수 의미 부각)
  · 국어: 평균 75, 표준편차 5
  · 영어: 평균 60, 표준편차 15  (변동성 큼)
  · 수학: 평균 70, 표준편차 8
  · 과학: 평균 80, 표준편차 4   (변동성 작음)
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

n = 20
korean  = np.clip(np.random.normal(75, 5, n), 0, 100).round(1)
english = np.clip(np.random.normal(60, 15, n), 0, 100).round(1)
math    = np.clip(np.random.normal(70, 8, n), 0, 100).round(1)
science = np.clip(np.random.normal(80, 4, n), 0, 100).round(1)

df = pd.DataFrame({
    "학생ID": [f"S{i:02d}" for i in range(1, n + 1)],
    "국어": korean,
    "영어": english,
    "수학": math,
    "과학": science,
})

df.to_excel(OUTPUT, index=False, sheet_name="과목점수")
print(f"샘플 데이터 저장 완료: {OUTPUT}")
print(df.head())
print("\n과목별 평균/표준편차:")
for col in ["국어", "영어", "수학", "과학"]:
    print(f"  {col}: 평균 {df[col].mean():.2f}, 표준편차 {df[col].std():.2f}")

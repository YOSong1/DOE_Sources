"""
3.3 데이터 관계 분석 - 샘플 데이터 생성 스크립트
======================================================
주제: 공부 시간(시간/주) vs 시험 점수 (총점 100)
- 25명의 학생에 대해 강한 양의 상관관계가 나오도록 구성
- 약간의 노이즈를 섞어 r=0.8~0.9 정도 나오도록
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

np.random.seed(7)

# 공부시간 (주당 시간, 0~30)
study_hours = np.array([5, 10, 15, 20, 25, 8, 12, 18, 22, 28,
                        6, 9, 14, 17, 21, 24, 27, 11, 13, 16,
                        19, 23, 26, 7, 30])

# 점수 = 30 + 2.2 * 공부시간 + 잡음
noise = np.random.normal(0, 6, len(study_hours))
scores = np.clip(30 + 2.2 * study_hours + noise, 0, 100).round(1)

df = pd.DataFrame({
    "학생ID": [f"S{i:02d}" for i in range(1, len(study_hours) + 1)],
    "주당공부시간": study_hours,
    "시험점수": scores,
})

df.to_excel(OUTPUT, index=False, sheet_name="공부시간_점수")
print(f"샘플 데이터 저장 완료: {OUTPUT}")
print(df.head())
print(f"\n표본 상관계수: {np.corrcoef(study_hours, scores)[0, 1]:.4f}")

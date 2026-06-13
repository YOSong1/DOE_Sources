"""
3.4 데이터의 표준화 - Excel 활용 버전
==========================================
sample_data.xlsx의 학생 4과목 점수를 읽어,
Z-점수 표준화와 Min-Max 정규화를 각각 적용하고,
"같은 학생이라도 어느 과목에서 더 잘했는가"를 표준화 점수로 비교한다.

학습 포인트:
- 원점수만 보면 "영어 75점이 국어 75점보다 높다"라고 잘못 판단하기 쉽다.
- Z-점수로 변환하면 각 과목의 평균/표준편차를 반영하여 공정 비교 가능.
- 같은 학생이라도 과목에 따라 상대적 위치가 크게 다를 수 있음을 확인.
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

XLSX = os.path.join(os.path.dirname(__file__), "sample_data.xlsx")
SUBJECTS = ["국어", "영어", "수학", "과학"]


def main():
    df = pd.read_excel(XLSX, sheet_name="과목점수")
    print("=" * 60)
    print("1단계: Excel 데이터 구조")
    print("=" * 60)
    print(f"행/열: {df.shape}")
    print(f"컬럼: {list(df.columns)}")
    print(df.head())

    # 2. 과목별 평균/표준편차 출력
    print("\n" + "=" * 60)
    print("2단계: 과목별 평균과 표준편차 (Z-점수 분모/분자에 사용됨)")
    print("=" * 60)
    means = df[SUBJECTS].mean()
    stds = df[SUBJECTS].std(ddof=0)   # StandardScaler와 동일하게 ddof=0
    for s in SUBJECTS:
        print(f"  {s}: 평균 = {means[s]:7.3f}, 표준편차 = {stds[s]:6.3f}")

    # 3. Z-점수 직접 계산 + sklearn 비교
    print("\n" + "=" * 60)
    print("3단계: Z-점수 표준화 (z = (x - mean) / std)")
    print("=" * 60)
    z_manual = (df[SUBJECTS] - means) / stds
    z_sklearn = pd.DataFrame(
        StandardScaler().fit_transform(df[SUBJECTS]),
        columns=SUBJECTS,
    )
    print("  수기 계산 z (처음 5행):")
    print(z_manual.head().round(4))
    print("\n  sklearn StandardScaler 결과 (처음 5행):")
    print(z_sklearn.head().round(4))
    print(f"\n  → 두 결과의 최대 절대 오차: {np.abs(z_manual.values - z_sklearn.values).max():.2e}")

    # 4. Min-Max 정규화
    print("\n" + "=" * 60)
    print("4단계: Min-Max 정규화 (x' = (x - min) / (max - min))")
    print("=" * 60)
    mm = pd.DataFrame(
        MinMaxScaler().fit_transform(df[SUBJECTS]),
        columns=SUBJECTS,
    )
    print("  결과 (처음 5행):")
    print(mm.head().round(4))
    print(f"\n  각 과목 최솟/최댓값(스케일링 후): 모두 0과 1")
    print(f"  국어: [{mm['국어'].min()}, {mm['국어'].max()}], "
          f"영어: [{mm['영어'].min()}, {mm['영어'].max()}]")

    # 5. 같은 학생 비교
    print("\n" + "=" * 60)
    print("5단계: '같은 점수가 같은 의미인가?' — 학생 한 명의 z-점수 비교")
    print("=" * 60)
    # 첫 번째 학생
    sid = df["학생ID"].iloc[0]
    raw = df[SUBJECTS].iloc[0]
    z_vals = z_manual.iloc[0]
    print(f"  학생 {sid}:")
    for s in SUBJECTS:
        print(f"    {s}: 원점수 {raw[s]:5.1f} → Z = {z_vals[s]:+.3f}")
    best = z_vals.idxmax()
    worst = z_vals.idxmin()
    print(f"\n  → 가장 상대적으로 잘 본 과목: {best} (Z = {z_vals[best]:+.3f})")
    print(f"  → 가장 상대적으로 못 본 과목: {worst} (Z = {z_vals[worst]:+.3f})")
    print(f"  → 원점수만 보면 모르는 '반에서의 상대 위치'를 Z-점수가 알려준다.")

    # 6. 이상치 후보(|z| > 2) 탐지
    print("\n" + "=" * 60)
    print("6단계: 이상치 후보 탐지 (|Z| > 2)")
    print("=" * 60)
    outliers = ((z_manual.abs() > 2)).any(axis=1)
    if outliers.any():
        print(df.loc[outliers, ["학생ID"] + SUBJECTS])
        print("\n  -> 평균에서 2σ 이상 벗어난 학생/과목이 존재.")
    else:
        print("  -> |Z| > 2 인 이상치는 없음.")


if __name__ == "__main__":
    main()

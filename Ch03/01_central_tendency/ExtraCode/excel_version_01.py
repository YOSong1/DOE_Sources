"""
3.1 데이터 중심 척도 - Excel 활용 버전
==========================================
sample_data.xlsx의 학생 시험 점수를 읽어 평균/중앙값/최빈값을 계산하고,
각 척도가 어떻게 다르게 데이터를 요약하는지 단계별로 출력.

학습 포인트:
- 이상치(아주 낮은 점수 2명)가 있을 때 평균은 크게 떨어지지만
  중앙값/최빈값은 거의 영향을 받지 않는다는 점을 직접 확인한다.
"""

import os
import sys
import pandas as pd
import numpy as np
from scipy import stats

# Windows cp949 환경에서도 한글이 깨지지 않도록 UTF-8 stdout 강제
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

XLSX = os.path.join(os.path.dirname(__file__), "sample_data.xlsx")


def main():
    # 1. Excel 읽기
    df = pd.read_excel(XLSX, sheet_name="시험점수")
    print("=" * 60)
    print("1단계: Excel에서 읽은 데이터 구조")
    print("=" * 60)
    print(f"행/열: {df.shape}")
    print(f"컬럼명: {list(df.columns)}")
    print("처음 5행:")
    print(df.head())

    scores = df["점수"].to_numpy()
    n = len(scores)

    # 2. 평균 - 모든 점수를 더해서 n으로 나누기
    print("\n" + "=" * 60)
    print("2단계: 평균(Mean) 계산")
    print("=" * 60)
    total = scores.sum()
    mean_val = total / n
    print(f"  점수 합계 ΣXi = {total}")
    print(f"  데이터 개수 n = {n}")
    print(f"  평균 = ΣXi / n = {total} / {n} = {mean_val:.4f}")
    print(f"  numpy 확인: np.mean = {np.mean(scores):.4f}")

    # 3. 중앙값 - 정렬 후 가운데 값
    print("\n" + "=" * 60)
    print("3단계: 중앙값(Median) 계산")
    print("=" * 60)
    sorted_scores = np.sort(scores)
    if n % 2 == 1:
        median_val = sorted_scores[n // 2]
        print(f"  n={n} (홀수) → 정렬된 데이터의 {n // 2 + 1}번째 값")
        print(f"  중앙값 = {median_val}")
    else:
        mid1 = sorted_scores[n // 2 - 1]
        mid2 = sorted_scores[n // 2]
        median_val = (mid1 + mid2) / 2
        print(f"  n={n} (짝수) → {n // 2}번째({mid1})와 {n // 2 + 1}번째({mid2})의 평균")
        print(f"  중앙값 = ({mid1} + {mid2}) / 2 = {median_val}")
    print(f"  numpy 확인: np.median = {np.median(scores):.4f}")

    # 4. 최빈값 - 가장 자주 등장한 점수
    print("\n" + "=" * 60)
    print("4단계: 최빈값(Mode) 계산")
    print("=" * 60)
    counts = df["점수"].value_counts().sort_values(ascending=False)
    print("  점수별 빈도(상위 5개):")
    for score, cnt in counts.head().items():
        print(f"    점수 {score:>3} → {cnt}회")
    mode_val = counts.idxmax()
    print(f"  최빈값(가장 많이 나온 점수) = {mode_val} ({counts.max()}회)")
    print(f"  scipy 확인: stats.mode = {stats.mode(scores, keepdims=True).mode[0]}")

    # 5. 결과 비교와 해석
    print("\n" + "=" * 60)
    print("5단계: 세 척도 비교 및 해석")
    print("=" * 60)
    print(f"  평균:   {mean_val:.2f}")
    print(f"  중앙값: {median_val:.2f}")
    print(f"  최빈값: {mode_val}")

    # 이상치 영향 분석: 가장 낮은 두 명 제외하고 평균 다시 계산
    main_group = sorted_scores[2:]   # 가장 낮은 두 점수 제외
    mean_no_outlier = main_group.mean()
    print(f"\n  → 이상치(가장 낮은 두 점수) 제외 후 평균: {mean_no_outlier:.2f}")
    print(f"  → 이상치가 평균을 {mean_no_outlier - mean_val:.2f}점이나 끌어내렸음")
    print("  → 중앙값/최빈값은 이상치에 거의 영향을 받지 않는다는 점을 확인할 수 있다.")

    # 분포 형태 진단
    if mean_val < median_val < mode_val:
        shape = "왼쪽으로 치우침(음의 왜도). 평균 < 중앙값 < 최빈값"
    elif mean_val > median_val > mode_val:
        shape = "오른쪽으로 치우침(양의 왜도). 최빈값 < 중앙값 < 평균"
    elif abs(mean_val - median_val) < 1 and abs(median_val - mode_val) < 1:
        shape = "대체로 대칭인 분포"
    else:
        shape = "복합적인 분포"
    print(f"\n  분포 진단: {shape}")


if __name__ == "__main__":
    main()

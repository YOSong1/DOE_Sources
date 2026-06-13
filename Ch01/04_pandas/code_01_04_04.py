# code_01_04_04.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.4 Pandas - 데이터 확인 함수
# =============================================================================
# 페이지: 324259 - 1.4 Pandas
# 설명: head, tail, info, describe, shape, columns, dtypes.
# =============================================================================

import pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Score': [85, 90, 78, 92],
    'Major': ['Math', 'CS', 'Math', 'Eco']
}
df = pd.DataFrame(data)

print(df.head())      # 처음 5개 행 출력
print(df.tail(3))     # 마지막 3개 행 출력
print(df.info())      # 열 이름, 자료형, 결측치 수 요약
print(df.describe())  # 수치형 열의 기술 통계량
print(df.shape)       # (행 수, 열 수)
print(df.columns)     # 열 이름 목록
print(df.dtypes)      # 각 열의 자료형

# code_01_04_05.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.4 Pandas - 열/행 선택과 필터링
# =============================================================================
# 페이지: 324259 - 1.4 Pandas
# =============================================================================

import pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Score': [85, 90, 78, 92],
    'Major': ['Math', 'CS', 'Math', 'Eco']
}
df = pd.DataFrame(data)

# 단일 열 선택 → Series 반환
scores = df['Score']
print(scores)

# 여러 열 선택 → DataFrame 반환
subset = df[['Name', 'Score']]
print(subset)

# df.loc[행 레이블, 열 레이블] — 레이블 기반
print(df.loc[0])             # 인덱스 0인 행
print(df.loc[0:2, 'Name'])   # 인덱스 0~2, Name 열

# df.iloc[행 번호, 열 번호] — 위치(정수) 기반
print(df.iloc[0])          # 첫 번째 행
print(df.iloc[0:2, 0:2])   # 첫 두 행, 첫 두 열

# 조건 필터링
high_scores = df[df['Score'] >= 90]
print(high_scores)

result = df[(df['Score'] >= 80) & (df['Major'] == 'Math')]
print(result)

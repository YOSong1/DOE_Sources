# code_01_04_06.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.4 Pandas - 데이터 추가와 수정
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

# 새 열 추가
df['Grade'] = ['B', 'A', 'C', 'A']

# 조건 기반 열 생성
df['Pass'] = df['Score'] >= 80

# 특정 셀 값 수정
df.loc[0, 'Score'] = 88

# 열 삭제
df = df.drop(columns=['Grade'])

# 행 삭제 (인덱스 2번 행 삭제)
df = df.drop(index=2)

print(df)

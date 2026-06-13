# code_01_04_07.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.4 Pandas - 결측값 처리
# =============================================================================
# 페이지: 324259 - 1.4 Pandas
# =============================================================================

import pandas as pd
import numpy as np

data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Score': [85, np.nan, 78, 92],
    'Major': ['Math', 'CS', None, 'Eco']
}
df = pd.DataFrame(data)

# 결측값 확인
print(df.isna())
print(df.isna().sum())   # 열별 결측값 개수

# 결측값이 있는 행 제거
df_dropped = df.dropna()
print(df_dropped)

# 결측값을 특정 값으로 채우기
df_filled = df.fillna({'Score': df['Score'].mean(), 'Major': '미정'})
print(df_filled)

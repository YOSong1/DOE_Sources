# code_01_04_09.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.4 Pandas - 정렬
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

# Score 기준 내림차순 정렬
df_sorted = df.sort_values('Score', ascending=False)
print(df_sorted)

# 여러 열 기준 정렬 (Major 오름차순, Score 내림차순)
df_multi = df.sort_values(['Major', 'Score'], ascending=[True, False])
print(df_multi)

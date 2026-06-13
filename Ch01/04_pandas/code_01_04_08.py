# code_01_04_08.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.4 Pandas - 그룹 연산
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

# 전공별 평균 점수
major_avg = df.groupby('Major')['Score'].mean()
print(major_avg)

# 전공별 다중 통계량
major_stats = df.groupby('Major')['Score'].agg(['mean', 'sum', 'count'])
print(major_stats)

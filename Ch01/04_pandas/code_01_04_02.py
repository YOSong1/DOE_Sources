# code_01_04_02.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.4 Pandas - DataFrame 생성 (딕셔너리)
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
print(df)

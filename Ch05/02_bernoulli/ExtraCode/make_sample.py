import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.2 베르누이 — 광고 클릭 데이터 생성 (각 행=한 사용자 노출 1회)
import pandas as pd
import numpy as np

np.random.seed(42)
N = 500           # 노출 횟수
true_p = 0.18      # 진짜 클릭률 (CTR)

clicks = np.random.binomial(1, true_p, size=N)
users = [f"user_{i:04d}" for i in range(1, N+1)]
df = pd.DataFrame({
    "user_id": users,
    "clicked": clicks,        # 1=클릭, 0=미클릭
})
df.to_excel("sample_data.xlsx", index=False, sheet_name="ad_clicks")
print(f"Saved sample_data.xlsx with N={N} rows, sum(clicks)={clicks.sum()}")

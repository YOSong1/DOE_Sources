import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.4 포아송 — 콜센터: 24시간 x 30일의 시간당 콜 수 데이터
import pandas as pd
import numpy as np

np.random.seed(7)
lam = 4.5      # 시간당 평균 콜 수
HOURS = 24 * 30
calls = np.random.poisson(lam, size=HOURS)

df = pd.DataFrame({
    "hour_idx": np.arange(HOURS),
    "day": (np.arange(HOURS) // 24) + 1,
    "hour_of_day": np.arange(HOURS) % 24,
    "calls": calls,
})
df.to_excel("sample_data.xlsx", index=False, sheet_name="callcenter")
print(f"Saved sample_data.xlsx, total hours={HOURS}, mean calls/hr={calls.mean():.3f}")

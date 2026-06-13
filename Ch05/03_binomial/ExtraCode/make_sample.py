import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.3 이항 — 100번의 배치 검사, 각 배치에서 n=10개 검사, 불량률 p=0.08
# 한 행 = 한 배치, 열 = (배치번호, 검사 개수 n, 불량 개수 X)
import pandas as pd
import numpy as np

np.random.seed(2026)
NUM_BATCH = 100
n = 10
true_p = 0.08

defects = np.random.binomial(n, true_p, size=NUM_BATCH)
df = pd.DataFrame({
    "batch_id": np.arange(1, NUM_BATCH+1),
    "n_inspected": n,
    "defects": defects,
})
df.to_excel("sample_data.xlsx", index=False, sheet_name="inspections")
print(f"Saved sample_data.xlsx, {NUM_BATCH} batches, mean defects = {defects.mean():.3f}")

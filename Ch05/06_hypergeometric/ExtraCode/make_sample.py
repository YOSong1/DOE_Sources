import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.6 초기하 — 모집단(부품 100개 중 불량 12개), 표본 크기 N=10으로 200번 반복 검사
import pandas as pd
import numpy as np

np.random.seed(33)
M = 100          # 모집단
n = 12           # 불량(성공) 항목
N = 10           # 한 번에 표본 크기
ROUNDS = 200     # 검사 횟수

defects = np.random.hypergeometric(ngood=n, nbad=M-n, nsample=N, size=ROUNDS)

df = pd.DataFrame({
    "round_id": np.arange(1, ROUNDS+1),
    "M_population": M,
    "n_defects_in_pop": n,
    "N_sample_size": N,
    "k_defects_in_sample": defects,
})
df.to_excel("sample_data.xlsx", index=False, sheet_name="hyper_inspect")
print(f"Saved. mean defects in sample = {defects.mean():.3f}, theoretical N*n/M = {N*n/M:.3f}")

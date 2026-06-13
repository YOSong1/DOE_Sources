import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.5 기하 — 게임 가챠: 200명의 유저가 SSR 카드를 처음 뽑기까지 시도한 횟수
import pandas as pd
import numpy as np

np.random.seed(11)
N = 200
true_p = 0.03      # SSR 등급 확률 3%

# numpy geometric: trials until first success, support {1,2,...}
attempts = np.random.geometric(true_p, size=N)
df = pd.DataFrame({
    "user_id": np.arange(1, N+1),
    "trials_to_first_SSR": attempts,
})
df.to_excel("sample_data.xlsx", index=False, sheet_name="gacha")
print(f"Saved sample_data.xlsx, N={N} users, mean trials={attempts.mean():.2f}")

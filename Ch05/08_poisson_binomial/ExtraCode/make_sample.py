import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.8 포아송-이항 — 야구팀 시즌 30경기 일정
# 각 경기마다 상대 전력에 따른 승률 p_i가 다름 (한 시즌 정도 데이터)
import pandas as pd
import numpy as np

np.random.seed(2024)
GAMES = 30
# 상대 전력 (strong/medium/weak)을 임의 배정하고, 승률 매핑
opponents = np.random.choice(["strong", "medium", "weak"], size=GAMES, p=[0.3, 0.4, 0.3])
prob_map = {"strong": 0.30, "medium": 0.50, "weak": 0.75}
p_i = np.array([prob_map[o] for o in opponents])

# 한 시즌 결과(실현치)도 함께 저장
wins = np.random.binomial(1, p_i)

df = pd.DataFrame({
    "game_id": np.arange(1, GAMES+1),
    "opponent_class": opponents,
    "p_i_win_prob": p_i,
    "win": wins,
})
df.to_excel("sample_data.xlsx", index=False, sheet_name="season")
print(f"Saved. sum(p_i)={p_i.sum():.3f}, season wins(실현)={wins.sum()}")

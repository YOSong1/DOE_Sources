import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.1 이산형 확률 분포 개요용 샘플 데이터 생성
# - 주사위/동전/카드 색의 관측 빈도 데이터
import pandas as pd
import numpy as np

np.random.seed(0)

# 주사위 300회 관측 빈도
dice_faces = [1, 2, 3, 4, 5, 6]
dice_obs = np.random.multinomial(300, [1/6]*6).tolist()

# 동전 100회 관측 빈도 (앞=H, 뒤=T)
coin_obs = np.random.multinomial(100, [0.5, 0.5]).tolist()

# 카드 색상 (빨강/검정) 200회 관측 빈도
card_obs = np.random.multinomial(200, [0.5, 0.5]).tolist()

df_dice = pd.DataFrame({"value": dice_faces, "observed": dice_obs})
df_coin = pd.DataFrame({"outcome": ["H", "T"], "observed": coin_obs})
df_card = pd.DataFrame({"color": ["Red", "Black"], "observed": card_obs})

out = "sample_data.xlsx"
with pd.ExcelWriter(out, engine="openpyxl") as w:
    df_dice.to_excel(w, sheet_name="dice", index=False)
    df_coin.to_excel(w, sheet_name="coin", index=False)
    df_card.to_excel(w, sheet_name="card", index=False)

print(f"Saved: {out}")
print(df_dice)
print(df_coin)
print(df_card)

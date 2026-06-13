import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 2.1 확률의 정의 - Excel 활용 버전: 동전/주사위 시행 로그 분석
# =============================================================================
# 책: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
# 페이지: 326983 - 2.1 확률의 정의
#
# sample_data.xlsx의 1000회 동전/주사위 시행 결과를 읽어
# 누적 시행 횟수별로 빈도가 어떻게 이론값에 수렴하는지(대수의 법칙) 확인.
# 각 사건의 확률을 고전적 정의 vs 빈도적 정의로 비교.
# =============================================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

BASE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(BASE, "sample_data.xlsx")

# -----------------------------------------------------------------------------
# 1) Excel 시행 로그 읽기
# -----------------------------------------------------------------------------
coin = pd.read_excel(XLSX, sheet_name="coin_flips")
dice = pd.read_excel(XLSX, sheet_name="dice_rolls")

print("=== 동전 시행 로그 (앞 5개) ===")
print(coin.head())
print(f"총 시행: {len(coin)}회")
print("값 분포:")
print(coin["coin_face"].value_counts())

print("\n=== 주사위 시행 로그 (앞 5개) ===")
print(dice.head())
print(f"총 시행: {len(dice)}회")
print("값 분포:")
print(dice["dice_value"].value_counts().sort_index())

# -----------------------------------------------------------------------------
# 2) 고전적 확률 (Classical) vs 빈도적 확률 (Frequentist)
# -----------------------------------------------------------------------------
print("\n=== 고전적 정의 vs 빈도적 정의 ===")

# (1) 동전 앞면
classical_H = 1 / 2  # 표본공간 {H,T} 중 H 1개
freq_H = (coin["coin_face"] == "H").mean()
print("[동전 앞면 H]")
print(f"  고전적 P(H) = 1/2 = {classical_H:.4f}")
print(f"  빈도적 P(H) = (H 횟수)/{len(coin)} = "
      f"{(coin['coin_face']=='H').sum()}/{len(coin)} = {freq_H:.4f}")

# (2) 주사위 짝수
classical_even = 3 / 6
freq_even = (dice["dice_value"] % 2 == 0).mean()
print("\n[주사위 짝수 (2,4,6)]")
print(f"  고전적 P(짝수) = 3/6 = {classical_even:.4f}")
print(f"  빈도적 P(짝수) = "
      f"{(dice['dice_value'] % 2 == 0).sum()}/{len(dice)} = {freq_even:.4f}")

# -----------------------------------------------------------------------------
# 3) 대수의 법칙: 누적 빈도 수렴 시각화
# -----------------------------------------------------------------------------
# 각 시행 시점까지의 누적 H 비율
is_H = (coin["coin_face"] == "H").astype(int)
cum_freq_H = is_H.cumsum() / np.arange(1, len(is_H) + 1)

is_even = (dice["dice_value"] % 2 == 0).astype(int)
cum_freq_even = is_even.cumsum() / np.arange(1, len(is_even) + 1)

print("\n=== 누적 빈도 (10, 100, 1000회 시점) ===")
for n in [10, 100, 1000]:
    print(f"  n={n:5d} | 동전 P(H)={cum_freq_H.iloc[n-1]:.4f} | "
          f"주사위 P(짝수)={cum_freq_even.iloc[n-1]:.4f}")

# -----------------------------------------------------------------------------
# 4) 시각화
# -----------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].plot(range(1, len(is_H) + 1), cum_freq_H,
             color='steelblue', label='누적 P(H)')
axes[0].axhline(0.5, color='tomato', linestyle='--', label='이론값 0.5')
axes[0].set_xscale('log')
axes[0].set_title('동전 — 누적 앞면 빈도 (log scale)')
axes[0].set_xlabel('시행 횟수')
axes[0].set_ylabel('P(H)')
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].plot(range(1, len(is_even) + 1), cum_freq_even,
             color='seagreen', label='누적 P(짝수)')
axes[1].axhline(0.5, color='tomato', linestyle='--', label='이론값 0.5')
axes[1].set_xscale('log')
axes[1].set_title('주사위 — 누적 짝수 빈도 (log scale)')
axes[1].set_xlabel('시행 횟수')
axes[1].set_ylabel('P(짝수)')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
out = os.path.join(BASE, "law_of_large_numbers.png")
plt.savefig(out, dpi=120)
print(f"\n그래프 저장: {out}")
plt.show()

print("\n[해석] 시행 초기에는 빈도가 이론값 0.5에서 크게 벗어나지만,\n"
      "        시행 횟수가 늘어날수록 빠르게 0.5로 수렴합니다.\n"
      "        이것이 대수의 법칙(Law of Large Numbers)입니다.")

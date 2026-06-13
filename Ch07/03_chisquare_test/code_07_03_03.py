# code_07_03_03.py
# -*- coding: utf-8 -*-
"""
페이지: 7.3 카이제곱 검정 — (3) 관찰 vs 기대 빈도 시각화.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

observed = np.array([18, 22, 19, 21, 15, 25])
expected = np.array([20, 20, 20, 20, 20, 20])
faces = [f"눈 {i}" for i in range(1, 7)]

x = np.arange(len(faces))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x - width/2, observed, width, label="관찰 빈도", color="steelblue")
ax.bar(x + width/2, expected, width, label="기대 빈도", color="coral", alpha=0.7)
ax.set_xticks(x)
ax.set_xticklabels(faces)
ax.set_xlabel("주사위 눈")
ax.set_ylabel("빈도")
ax.set_title("적합도 검정: 관찰 빈도 vs 기대 빈도")
ax.legend()
plt.tight_layout()
plt.show()

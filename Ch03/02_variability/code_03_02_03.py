# code_03_02_03.py
"""
3.2 데이터 변동성 - 원본 코드 #3: 모표준편차/표본표준편차
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

data = np.array([2, 4, 6, 8, 10])

# 모표준편차 (ddof=0)
pop_std = np.std(data, ddof=0)
print(f"모표준편차 (σ): {pop_std:.4f}")

# 표본표준편차 (ddof=1)
sample_std = np.std(data, ddof=1)
print(f"표본표준편차 (s): {sample_std:.4f}")

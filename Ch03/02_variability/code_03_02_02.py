# code_03_02_02.py
"""
3.2 데이터 변동성 - 원본 코드 #2: 모분산/표본분산
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

data = np.array([2, 4, 6, 8, 10])

# 모분산 (ddof=0, 기본값)
pop_var = np.var(data, ddof=0)
print(f"모분산 (σ²): {pop_var}")

# 표본분산 (ddof=1)
sample_var = np.var(data, ddof=1)
print(f"표본분산 (s²): {sample_var}")

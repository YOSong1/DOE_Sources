# code_01_03_08.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.3 Numpy - 배열 형태 변환
# =============================================================================
# 페이지: 324207 - 1.3 Numpy
# 설명: reshape, flatten, 전치(.T).
# =============================================================================

import numpy as np

arr = np.arange(12)
print("원래 형태:", arr.shape)   # (12,)
print(arr)

# 1차원 → 3행 4열 2차원으로 변환
arr_2d = arr.reshape(3, 4)
print("\nreshape(3, 4):")
print(arr_2d)

# 다시 1차원으로 펼치기
arr_flat = arr_2d.flatten()
print("\nflatten():", arr_flat)

# 전치 행렬 (3×4 → 4×3)
print("\n전치 행렬 .T:")
print(arr_2d.T)
print("전치 후 형태:", arr_2d.T.shape)  # (4, 3)

# code_01_03_02.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.3 Numpy - 배열 생성
# =============================================================================
# 페이지: 324207 - 1.3 Numpy
# 설명: np.array, np.zeros, np.ones, np.eye, np.arange, np.linspace 활용.
# =============================================================================

import numpy as np

# 파이썬 리스트로 배열 생성
arr = np.array([1, 2, 3, 4, 5])

# 특수 배열 생성
zeros = np.zeros((3, 4))   # 0으로 채워진 3×4 배열
ones = np.ones((2, 3))     # 1로 채워진 2×3 배열
eye = np.eye(3)            # 3×3 단위행렬

# 연속 숫자 배열 — 0부터 9까지 정수
arr_range = np.arange(10)

# 등간격으로 숫자 생성 — 0과 1 사이를 5개로 나눔
arr_lin = np.linspace(0, 1, 5)

print(arr)        # [1 2 3 4 5]
print(arr_range)  # [0 1 2 3 4 5 6 7 8 9]
print(arr_lin)    # [0.   0.25 0.5  0.75 1.  ]

# code_01_03_07.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.3 Numpy - 난수 생성
# =============================================================================
# 페이지: 324207 - 1.3 Numpy
# =============================================================================

import numpy as np

# 시드 고정 — 실행할 때마다 같은 결과를 얻습니다
np.random.seed(42)

# 정규 분포에서 난수 생성 (평균=0, 표준편차=1)
rand_normal = np.random.normal(loc=0, scale=1, size=5)

# 균등 분포에서 난수 생성 (0 이상 1 미만)
rand_uniform = np.random.uniform(0, 1, size=5)

# 정수 난수 생성 (주사위 시뮬레이션: 1~6)
rand_int = np.random.randint(1, 7, size=10)

print("정규 분포:", rand_normal)
print("균등 분포:", rand_uniform)
print("정수 난수:", rand_int)

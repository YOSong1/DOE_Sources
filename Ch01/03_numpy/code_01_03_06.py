# code_01_03_06.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.3 Numpy - 주요 통계 함수
# =============================================================================
# 페이지: 324207 - 1.3 Numpy
# 설명: mean, median, std, var, max, min, sum, percentile.
# =============================================================================

import numpy as np

scores = np.array([88, 92, 76, 100, 64, 85, 91, 78])

print("평균:   ", np.mean(scores))        # 84.25
print("중앙값: ", np.median(scores))      # 86.5
print("표준편차:", np.std(scores))
print("분산:   ", np.var(scores))
print("최댓값: ", np.max(scores))         # 100
print("최솟값: ", np.min(scores))         # 64
print("합계:   ", np.sum(scores))

# 백분위수 — 하위 25%, 75% 지점
print("Q1:", np.percentile(scores, 25))
print("Q3:", np.percentile(scores, 75))

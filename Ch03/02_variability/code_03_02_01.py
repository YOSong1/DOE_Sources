# code_03_02_01.py
"""
3.2 데이터 변동성 - 원본 코드 #1: 범위(Range)
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

data = np.array([55, 70, 82, 90, 65, 78, 88])

# 내장 함수 사용
range_value = max(data) - min(data)
print(f"범위 (내장 함수): {range_value}")

# numpy 사용
range_np = np.max(data) - np.min(data)
print(f"범위 (numpy): {range_np}")

# numpy의 ptp (peak to peak) 함수 사용
range_ptp = np.ptp(data)
print(f"범위 (np.ptp): {range_ptp}")

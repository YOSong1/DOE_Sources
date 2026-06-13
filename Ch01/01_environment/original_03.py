import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.1 실습 환경 - 환경 검증: 라이브러리 버전 출력
# =============================================================================
# 책: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
# 페이지: 324205 - 1.1 실습 환경
# 설명: 실습 환경이 올바르게 설정되었는지 주요 라이브러리 버전을 출력하여 확인.
# =============================================================================

import numpy as np
import pandas as pd
import scipy
import matplotlib
import matplotlib.pyplot as plt

print("NumPy 버전:", np.__version__)
print("Pandas 버전:", pd.__version__)
print("SciPy 버전:", scipy.__version__)
print("Matplotlib 버전:", matplotlib.__version__)
print("환경 설정 완료!")

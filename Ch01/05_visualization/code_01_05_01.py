# code_01_05_01.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.5 시각화 - Matplotlib 한글 폰트 설정
# =============================================================================
# 페이지: 324260 - 1.5 시각화
# =============================================================================

import matplotlib.pyplot as plt
import platform

# 운영체제에 따라 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'   # 맑은 고딕
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'     # macOS

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

print("한글 폰트 설정 완료:", plt.rcParams['font.family'])

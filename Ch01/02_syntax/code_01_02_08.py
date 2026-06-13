# code_01_02_08.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.2 Python 기본 문법 - if/elif/else
# =============================================================================
# 페이지: 324206 - 1.2 Python 기본 문법
# 설명: 점수에 따른 등급 판정.
# =============================================================================

score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"점수: {score}, 등급: {grade}")

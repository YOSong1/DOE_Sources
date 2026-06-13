# code_01_02_06.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.2 Python 기본 문법 - for 루프
# =============================================================================
# 페이지: 324206 - 1.2 Python 기본 문법
# 설명: range, enumerate, 리스트 컴프리헨션 사용.
# =============================================================================

# range()로 반복
total = 0
for i in range(1, 6):
    total += i
print("합계:", total)

# enumerate()로 인덱스와 값 동시에
fruits = ["apple", "banana", "cherry"]
for idx, fruit in enumerate(fruits):
    print(idx, fruit)

# 리스트 컴프리헨션: 한 줄로 리스트 생성
squares = [x**2 for x in range(1, 6)]
print(squares)

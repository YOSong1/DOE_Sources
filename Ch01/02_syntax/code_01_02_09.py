# code_01_02_09.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.2 Python 기본 문법 - 함수와 lambda
# =============================================================================
# 페이지: 324206 - 1.2 Python 기본 문법
# 설명: def로 함수 정의, lambda로 한 줄 함수 작성.
# =============================================================================

# 기본 함수 정의
def greet(name, greeting="안녕하세요"):
    return f"{greeting}, {name}님!"

print(greet("Alice"))
print(greet("Bob", "반갑습니다"))

# lambda 함수
square = lambda x: x ** 2
print(square(5))

# 정렬 기준으로 자주 활용
pairs = [(1, "b"), (3, "a"), (2, "c")]
pairs.sort(key=lambda p: p[0])
print(pairs)

# code_01_02_03.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.2 Python 기본 문법 - 리스트
# =============================================================================
# 페이지: 324206 - 1.2 Python 기본 문법
# 설명: 리스트 인덱싱, 슬라이싱, append/insert/remove 메서드 사용.
# =============================================================================

scores = [85, 92, 78, 95, 88]

print(scores[0])    # 첫 번째 원소
print(scores[-1])   # 마지막 원소
print(scores[1:3])  # 슬라이싱: 인덱스 1~2

scores.append(100)          # 원소 추가
scores.insert(0, 70)        # 특정 위치에 삽입
scores.remove(78)           # 값으로 삭제
print(scores)

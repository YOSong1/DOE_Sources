# code_01_02_04.py
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.2 Python 기본 문법 - 딕셔너리
# =============================================================================
# 페이지: 324206 - 1.2 Python 기본 문법
# 설명: 키-값 쌍으로 데이터 관리, get() 기본값 활용.
# =============================================================================

student = {"name": "David", "age": 25, "score": 92}

print(student["name"])              # 키로 값 접근
print(student.get("grade", "N/A"))  # 키가 없을 때 기본값 반환

student["grade"] = "A"              # 새 키-값 추가
print(student)

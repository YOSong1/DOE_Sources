# code_17_02_01.py
# Chapter 17.2 완전 무작위 설계의 절차
# 원본 코드: 무작위 배정 예시 (책 본문 page 324459)
# 30개 실험 단위를 3개 처리(A, B, C)에 각 10개씩 무작위로 배정합니다.

import random

units = list(range(1, 31))  # 30개 실험 단위
random.shuffle(units)

# 수준 A: 처음 10개, 수준 B: 다음 10개, 수준 C: 마지막 10개
assignments = {'A': units[:10], 'B': units[10:20], 'C': units[20:]}

for treatment, ids in assignments.items():
    print(f"처리 {treatment}: {sorted(ids)}")

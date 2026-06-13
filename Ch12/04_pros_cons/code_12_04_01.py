# code_12_04_01.py
# -*- coding: utf-8 -*-
"""
페이지: 12.4 부분 요인 실험의 장단점 및 활용
설명: pyDOE3 로 Resolution III / IV / V 설계의 실험 횟수를 비교한다.
"""

from pyDOE3 import fracfact

# Resolution III 설계: 2^(7-4) = 8회
design_III = fracfact('a b c abc bc ac ab')
print(f"Resolution III (7요인): {design_III.shape[0]}회 실험")

# Resolution IV 설계: 2^(6-2) = 16회
design_IV = fracfact('a b c d abc bcd')
print(f"Resolution IV (6요인): {design_IV.shape[0]}회 실험")

# Resolution V 설계: 2^(5-1) = 16회
design_V = fracfact('a b c d abcd')
print(f"Resolution V (5요인): {design_V.shape[0]}회 실험")

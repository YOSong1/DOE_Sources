# code_20_05_01.py
# Chapter 20.05 코드 1: 부분 요인 설계의 alias structure 계산
#
# pyDOE3.fracfact 로 2^(5-2) Resolution III 설계 행렬을 만들고,
# 모든 효과 컬럼의 곱을 비교해 어느 효과가 서로 교락(alias)되는지 자동으로 추출합니다.
# 이 alias 표를 LLM payload 의 일부로 넘겨 검토를 받습니다.

import json
from itertools import combinations

import numpy as np
import pandas as pd
from pyDOE3 import fracfact


# 1) 2^(5-2) 설계 — 생성자: D=AB, E=AC
design = fracfact("a b c ab ac")
factors = ["A", "B", "C", "D", "E"]
df = pd.DataFrame(design, columns=factors)
print("--- 설계 행렬 ---")
print(df)


# 2) 모든 효과 컬럼 만들기 (주효과 + 모든 2차 상호작용)
effect_cols: dict[str, np.ndarray] = {}
for f in factors:
    effect_cols[f] = df[f].values
for a, b in combinations(factors, 2):
    effect_cols[f"{a}{b}"] = df[a].values * df[b].values


# 3) alias 그룹 도출 — 컬럼이 동일한 효과들끼리 묶는다
aliases: list[list[str]] = []
used = set()
labels = list(effect_cols.keys())
for i, lab in enumerate(labels):
    if lab in used:
        continue
    group = [lab]
    for lab2 in labels[i + 1:]:
        if lab2 in used:
            continue
        if np.array_equal(effect_cols[lab], effect_cols[lab2]):
            group.append(lab2)
            used.add(lab2)
    if len(group) > 1:
        aliases.append(group)
    used.add(lab)


# 4) Resolution 추정 — 가장 작은 alias 그룹의 원소 길이 합
def resolution(groups: list[list[str]]) -> str:
    if not groups:
        return "Full"
    lengths = [min(len(name) for name in g) + max(len(name) for name in g) for g in groups]
    r = min(len(name) for g in groups for name in g) + max(len(name) for g in groups for name in g)
    # 간단 휴리스틱: 주효과(1글자) ↔ 2상호작용(2글자)이 교락되면 Resolution III
    has_main_vs_2fi = any(any(len(n) == 1 for n in g) and any(len(n) == 2 for n in g) for g in groups)
    if has_main_vs_2fi:
        return "III"
    has_2fi_vs_2fi = any(all(len(n) == 2 for n in g) and len(g) > 1 for g in groups)
    if has_2fi_vs_2fi:
        return "IV"
    return "V 이상"


payload = {
    "task":   "fractional factorial alias review",
    "goal":   "주효과 추정이 어떤 상호작용과 교락되는지 검토",
    "design": "2^(5-2) fractional factorial",
    "generators": ["D = A*B", "E = A*C"],
    "resolution": resolution(aliases),
    "alias_groups": [" = ".join(g) for g in aliases],
    "questions": [
        "Resolution 등급이 의사결정에 충분한지 알려줘",
        "교락된 효과 때문에 잘못 해석될 위험이 큰 항목을 지적해줘",
        "추가 실험 (fold-over 등) 이 필요하다면 추천해줘",
    ],
}
print("\n--- payload ---")
print(json.dumps(payload, ensure_ascii=False, indent=2))

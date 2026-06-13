# code_20_05_02.py
# Chapter 20.05 코드 2: 부분 요인 실험 — alias 정보를 포함한 payload + LLM 리뷰
#
# 코드 1(code_20_05_01.py)에서 추출한 alias 그룹을 payload 의 alias_groups
# 필드로 LLM 에 넘겨 해석 위험을 검토받습니다.

import json
import os
from itertools import combinations

import numpy as np
import pandas as pd
from pyDOE3 import fracfact

# ---------------------------------------------------------------------------
# 1) alias 그룹 자동 추출 (code_20_05_01.py 와 동일한 알고리즘)
# ---------------------------------------------------------------------------
design = fracfact("a b c ab ac")
factors = ["A", "B", "C", "D", "E"]
df = pd.DataFrame(design, columns=factors)

effect_cols = {f: df[f].values for f in factors}
for a, b in combinations(factors, 2):
    effect_cols[f"{a}{b}"] = df[a].values * df[b].values

aliases, used = [], set()
labels = list(effect_cols)
for i, lab in enumerate(labels):
    if lab in used:
        continue
    group = [lab]
    for lab2 in labels[i + 1:]:
        if lab2 not in used and np.array_equal(effect_cols[lab], effect_cols[lab2]):
            group.append(lab2); used.add(lab2)
    used.add(lab)
    if len(group) > 1:
        aliases.append(group)

# ---------------------------------------------------------------------------
# 2) payload 구성 — alias_groups 포함 (책 20.5.2)
# ---------------------------------------------------------------------------
doe_result = {
    "task": "fractional factorial review",
    "goal": "부분 요인 실험 결과 해석 초안을 검토",
    "design": "2^(5-2)",
    "resolution": "III",
    "replication": False,
    "significant_effects": ["A", "B", "C"],
    "alias_groups": [" = ".join(g) for g in aliases],
    "interpretation_draft": "A, B, C가 모두 유의하므로 세 요인을 높은 수준으로 설정하는 것이 최적이다.",
    "questions": [
        "이 해석이 통계적으로 과도한지 검토해줘",
        "aliasing 때문에 주의할 점이 있는지 설명해줘",
        "확인 실험이나 추가 설계를 제안해줘",
    ],
}
prompt = f"당신은 실험계획법 리뷰어입니다. JSON 으로 답하세요.\n\n{json.dumps(doe_result, ensure_ascii=False, indent=2)}"

print("=== alias_groups ===")
for g in doe_result["alias_groups"]:
    print("  " + g)


# ---------------------------------------------------------------------------
# 3) LLM 호출 — API 키 없으면 mock 응답 (흐름 시연용)
# ---------------------------------------------------------------------------
def call_llm(prompt: str, mock: dict) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return json.dumps(mock, ensure_ascii=False)
    from openai import OpenAI
    return OpenAI().responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5"),
        instructions="summary, risks, next_steps 키의 JSON 으로만 답하세요. 한국어.",
        input=prompt,
        text={"format": {"type": "json_object"}},
    ).output_text


mock_review = {
    "summary": "Resolution III 설계 — A·B·C 가 유의해도 교락된 상호작용 때문일 수 있음.",
    "risks": [
        "주효과 = 순수 효과 라는 단정 위험 (예: A 는 BD 와 교락)",
        "확인 실험 없는 최적 조건 확정 금지",
    ],
    "next_steps": [
        "fold-over 설계로 주효과 분리",
        "유력 조건 확인 실험 수행",
    ],
}

raw = call_llm(prompt, mock_review)


# ---------------------------------------------------------------------------
# 4) 응답 활용 — 요약·위험 신호·다음 단계 추출
# ---------------------------------------------------------------------------
review = json.loads(raw)

print("\n=== LLM 응답 (요약) ===")
print(review["summary"])

risks = review.get("risks", [])
print("\n=== 위험 신호 (" + str(len(risks)) + "건) ===")
for r in risks:
    print("  ⚠️  " + r)

steps = review.get("next_steps", [])
print("\n=== 다음 단계 (" + str(len(steps)) + "건) ===")
for s in steps:
    print("  → " + s)

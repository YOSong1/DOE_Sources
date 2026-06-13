# code_20_08_04.py
# Chapter 20.08 코드 4: 분석 세션 1건 = JSONL 한 줄
#
# 한 번의 (payload → prompt → LLM 호출 → 사람 검토) 사이클을
# 하나의 JSON 객체로 만들어 JSONL 파일에 누적합니다.
# 추후 동일 payload·prompt 가 다른 응답을 낼 때 추적할 수 있고,
# 회귀 테스트(코드 3)의 입력이 됩니다.

import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def make_record(
    *,
    payload: dict,
    prompt: str,
    model: str,
    temperature: float,
    response_text: str,
    review_parsed: dict,
    human_decision: str,
    provider: str = "openai",
) -> dict:
    return {
        "ts":            datetime.now(timezone.utc).isoformat(),
        "provider":      provider,
        "model":         model,
        "temperature":   temperature,
        "payload_hash":  _hash(json.dumps(payload, ensure_ascii=False, sort_keys=True)),
        "prompt_hash":   _hash(prompt),
        "payload":       payload,
        "prompt":        prompt,
        "response_raw":  response_text,
        "review":        review_parsed,
        "human_decision": human_decision,
        "env": {
            "python":   sys.version.split()[0],
            "platform": platform.platform(),
            "openai_sdk":    _try_version("openai"),
            "anthropic_sdk": _try_version("anthropic"),
            "statsmodels":   _try_version("statsmodels"),
        },
    }


def _try_version(pkg: str) -> str | None:
    try:
        mod = __import__(pkg)
        return getattr(mod, "__version__", None)
    except ImportError:
        return None


def append_jsonl(record: dict, path: str = "analysis_log.jsonl") -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# 데모: 1건 기록
if __name__ == "__main__":
    payload = {
        "task": "anova interpretation",
        "anova_table": [{"term": "Treatment", "F": 8.5, "p_value": 0.005}],
    }
    prompt = (
        "당신은 통계 리뷰어입니다. JSON 으로 답하세요.\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )

    record = make_record(
        payload=payload,
        prompt=prompt,
        provider="openai",
        model="gpt-5",
        temperature=0.0,
        response_text='{"summary":"유의","risks":[],"next_steps":["Tukey HSD"]}',
        review_parsed={"summary": "유의", "risks": [], "next_steps": ["Tukey HSD"]},
        human_decision="채택 — 사후 검정 진행",
    )

    log_path = Path("analysis_log.jsonl")
    append_jsonl(record, log_path)
    print(f"기록 적재: {log_path.resolve()}")
    print(f"payload_hash={record['payload_hash']}, prompt_hash={record['prompt_hash']}")

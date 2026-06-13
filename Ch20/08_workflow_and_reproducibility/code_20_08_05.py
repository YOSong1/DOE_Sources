# code_20_08_05.py
# Chapter 20.08 코드 5: 회귀 테스트 — 같은 payload 가 다른 결론을 내는지 감지
#
# CI 에서 야간에 돌리며, 동일 payload·prompt 에 대해 LLM 응답의 핵심 결론이
# 변동되지 않는지 점검합니다. 변동되면 모델 업데이트로 인한 회귀(regression)
# 가능성을 신호로 띄웁니다.

import json
from collections import Counter, defaultdict
from pathlib import Path


def load_jsonl(path: str = "analysis_log.jsonl") -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    out = []
    with p.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def group_by_payload(records):
    groups = defaultdict(list)
    for r in records:
        groups[r["payload_hash"]].append(r)
    return dict(groups)


CRITICAL_KEYS = ("summary",)
WARN_THRESHOLD = 0.5  # 같은 payload 의 응답 중 가장 흔한 결론의 비율이 이 값 이하면 경고


def regression_check(records: list[dict]) -> list[dict]:
    flags = []
    for h, rs in group_by_payload(records).items():
        if len(rs) < 2:
            continue
        for key in CRITICAL_KEYS:
            vals = [r["review"].get(key, "") for r in rs]
            counts = Counter(vals)
            most_common, n = counts.most_common(1)[0]
            ratio = n / len(rs)
            if ratio <= WARN_THRESHOLD:
                flags.append({
                    "payload_hash": h,
                    "key":          key,
                    "n_calls":      len(rs),
                    "majority":     most_common[:80],
                    "majority_ratio": round(ratio, 2),
                    "all_unique":   list(set(vals))[:5],
                })
    return flags


if __name__ == "__main__":
    records = load_jsonl()
    if not records:
        print("로그가 비어 있습니다.")
        raise SystemExit(0)

    flags = regression_check(records)
    if not flags:
        print(f"✅ 회귀 없음 — {len(records)}건 검사 완료")
    else:
        print(f"⚠️  {len(flags)}건 회귀 의심:")
        print(json.dumps(flags, ensure_ascii=False, indent=2))

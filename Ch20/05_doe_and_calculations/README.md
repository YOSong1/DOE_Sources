# 20.05 DOE 결과 검토 — 고유 계산과 LLM 리뷰

DOE 고유 계산(alias 구조·응답 표면 정상점·다구찌 S/N 비)을 Python 으로 직접 수행하고,
그 결과를 payload 로 LLM 에 넘겨 해석 위험을 검토받는 패턴을 다룹니다.
각 파일은 책 본문의 동일 번호 코드 블록(`# code_20_05_NN.py` 주석)과 1:1 매핑됩니다.

## 파일 구성

| 파일 | 내용 |
|------|------|
| `code_20_05_01.py` | `pyDOE3.fracfact` 2^(5-2) 설계의 alias structure 자동 추출 |
| `code_20_05_02.py` | `alias_groups` 를 포함한 payload + LLM 리뷰 (교락 해석 위험 점검) |
| `code_20_05_03.py` | 응답 표면 정상점 계산 + eigenvalue 로 max/min/saddle 판정 + 영역 확인 |
| `code_20_05_04.py` | 다구찌 S/N 비 3종 (Larger / Smaller / Nominal-the-Best) |
| `code_20_05_05.py` | 해석 초안 검토 — 키: `statistically_risky_parts, design_structure_concerns, safer_statement, confirmation_runs` |

## 사용법

```bash
python code_20_05_01.py
python code_20_05_02.py
python code_20_05_03.py
python code_20_05_04.py
python code_20_05_05.py
```

`pyDOE3` 패키지가 필요합니다 (`pip install pyDOE3`).
`OPENAI_API_KEY` 가 없으면 mock 응답으로 흐름이 이어지므로 API 키 없이도 실행할 수 있습니다.

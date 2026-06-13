# 20.08 실무 워크플로와 재현성 로그

사출 성형 공정 개선 시나리오로 **설계 → 분석 → LLM 검토 → 로그 적재 → 회귀 테스트**
전체 흐름을 따라갑니다. 모든 분석 세션은 JSONL 한 줄로 적재합니다.
각 파일은 책 본문의 동일 번호 코드 블록(`# code_20_08_NN.py` 주석)과 1:1 매핑됩니다.

## 파일 구성

| 파일 | 내용 |
|------|------|
| `code_20_08_01.py` | `pyDOE3.ff2n` 4요인 2수준 설계 매트릭스 생성 |
| `code_20_08_02.py` | 사출 성형 DOE 데이터로 statsmodels ANOVA 수행 |
| `code_20_08_03.py` | DOE 결과 payload 구성 + LLM 리뷰 프롬프트 |
| `code_20_08_04.py` | 재현성 로그 — 분석 세션 1건 = JSONL 한 줄 (payload_hash·prompt_hash·환경) |
| `code_20_08_05.py` | 회귀 테스트 — 같은 payload 가 다른 결론을 내는지 감지 (CI 야간 잡) |

## 사용법

```bash
python code_20_08_01.py
python code_20_08_02.py
python code_20_08_03.py
python code_20_08_04.py
python code_20_08_05.py
```

`pyDOE3` 패키지가 필요합니다 (`pip install pyDOE3`).
`code_20_08_05.py` 는 `analysis_log.jsonl` 이 있을 때 검사를 수행합니다 (없으면 안내 후 종료).

# 20.04 회귀·ANOVA 결과 해석과 LLM 응답 검증

회귀·ANOVA 결과를 LLM 에 해석시키는 프롬프트와, 응답을 **4단계로 자동 검증**
(JSON 파싱 → 필수 키 → payload 숫자 일치 → 금지 표현)하는 패턴을 다룹니다.
각 파일은 책 본문의 동일 번호 코드 블록(`# code_20_04_NN.py` 주석)과 1:1 매핑됩니다.

## 파일 구성

| 파일 | 내용 |
|------|------|
| `code_20_04_01.py` | 회귀 해석 프롬프트 — 키: `summary, significant_vars, non_significant_vars, risks` |
| `code_20_04_02.py` | 일원 ANOVA 해석 프롬프트 — 키: `summary, risks, next_steps` + 응답 활용 |
| `code_20_04_03.py` | 이원 ANOVA payload — 상호작용이 유의할 때의 해석 질문 포함 |
| `code_20_04_04.py` | 응답 4단계 검증 함수 (`validate`) — 스키마·숫자 일치·금지 표현 |
| `code_20_04_05.py` | 해석 초안 검토 — 키: `incorrect_parts, safer_statement, additional_analysis_needed` |

## 사용법

```bash
python code_20_04_01.py
python code_20_04_02.py
python code_20_04_03.py
python code_20_04_04.py
python code_20_04_05.py
```

`OPENAI_API_KEY` 가 없으면 mock 응답으로 흐름이 이어지므로 API 키 없이도 실행할 수 있습니다.

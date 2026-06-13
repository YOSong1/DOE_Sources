# 20.03 Python ↔ LLM API 연결과 결과 변환

`statsmodels` 분석 결과를 JSON 직렬화 가능한 payload 로 변환하고(`_safe()` 헬퍼),
OpenAI / Anthropic API 로 JSON 응답을 받아 오는 패턴을 다룹니다.
각 파일은 책 본문의 동일 번호 코드 블록(`# code_20_03_NN.py` 주석)과 1:1 매핑됩니다.

## 파일 구성

| 파일 | 내용 |
|------|------|
| `code_20_03_01.py` | OLS 회귀 결과 → payload 변환 (`_safe()` 로 NaN/Inf·numpy 스칼라 처리) |
| `code_20_03_02.py` | ANOVA 표 → payload 변환 (Residual 행의 NaN 안전 처리) |
| `code_20_03_03.py` | 역할·맥락·요청·출력 형식 4요소를 갖춘 JSON 응답 요청 프롬프트 |
| `code_20_03_04.py` | 참조 구현 — 이원 ANOVA → payload → OpenAI/Anthropic 호출 → 응답 검증 전체 흐름 |
| `code_20_03_05.py` | JSON 응답 강제 두 가지 방법 — OpenAI `json_object`, Anthropic structured outputs(`output_config`) |

## 사용법

```bash
python code_20_03_01.py
python code_20_03_02.py
python code_20_03_03.py
python code_20_03_04.py
python code_20_03_05.py
```

API 키 설정 (없으면 mock 응답으로 흐름 시연):

```bash
export OPENAI_API_KEY=sk-...        # 또는 ANTHROPIC_API_KEY=sk-ant-...
export LLM_PROVIDER=openai          # 또는 anthropic
```

> 참고: Anthropic 의 JSON 강제는 structured outputs(`output_config` 의 JSON 스키마)를 사용합니다.
> 구형 assistant prefill 기법은 Claude Sonnet 4.6 등 최신 모델에서 지원되지 않습니다.

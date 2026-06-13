# Chapter 20. 생성형 AI를 활용한 분석

WikiDocs 책 1914 (Python으로 배우는 확률통계와 실험계획법) 

## 폴더 구성

| 폴더 | 책 절 | 주제 |
|------|------|------|
| (코드 없음) | 20.01 | 생성형 AI와 LLM의 역할 분담 |
| `02_data_structure/` | 20.02 | 분석 결과를 LLM에 전달하는 데이터 구조 |
| `03_api_and_payload/` | 20.03 | Python ↔ LLM API 연결과 결과 변환 |
| `04_regression_and_validation/` | 20.04 | 회귀·ANOVA 결과 해석과 LLM 응답 검증 |
| `05_doe_and_calculations/` | 20.05 | DOE 결과 검토 — 고유 계산과 LLM 리뷰 |
| `06_prompt_engineering/` | 20.06 | 프롬프트 엔지니어링 for 실험계획법 분석 |
| `07_cautions_and_sensitive/` | 20.07 | 주의사항·체크리스트와 민감 데이터 처리 |
| `08_workflow_and_reproducibility/` | 20.08 | 실무 워크플로와 재현성 로그 |
| (코드 없음) | 20.09 | 결론 및 향후 전망 |
| (코드 없음) | 20.10 | 연습 문제 |

## 코드 파일 매핑

각 폴더의 `code_20_NN_MM.py` 는 책 본문의 동일 번호 코드 블록(`# code_20_NN_MM.py` 주석으로 시작) 과 1:1 매핑됩니다.

| 책 코드 블록 | 로컬 파일 | 핵심 내용 |
|------------|----------|----------|
| `code_20_02_01.py` ~ `04.py` | `02_data_structure/` | 회귀·ANOVA·DOE payload 구조 + 함수 빌더 |
| `code_20_03_01.py` ~ `05.py` | `03_api_and_payload/` | OLS/ANOVA → payload 변환, 프롬프트, OpenAI/Anthropic 호출 |
| `code_20_04_01.py` ~ `05.py` | `04_regression_and_validation/` | 회귀/ANOVA/이원 해석 + 4단계 응답 검증 |
| `code_20_05_01.py` ~ `05.py` | `05_doe_and_calculations/` | alias 자동 추출, 정상점+eigenvalue, S/N 비 |
| `code_20_06_01.py` ~ `04.py` | `06_prompt_engineering/` | 회귀/ANOVA/DOE/보고서 작성 템플릿 |
| `code_20_07_01.py` ~ `02.py` | `07_cautions_and_sensitive/` | 변수명 익명화, 요약 통계 전송 |
| `code_20_08_01.py` ~ `05.py` | `08_workflow_and_reproducibility/` | 워크플로 + JSONL 로그 + 회귀 테스트 |

## 실행 환경

```bash
pip install pandas statsmodels scipy numpy pyDOE3 openai anthropic
```

API 키가 설정되어 있지 않을 때도 mock 응답으로 흐름이 끊기지 않습니다.

```bash
# OpenAI 사용
export OPENAI_API_KEY=sk-...
export LLM_PROVIDER=openai

# Anthropic 사용
export ANTHROPIC_API_KEY=sk-ant-...
export LLM_PROVIDER=anthropic
```

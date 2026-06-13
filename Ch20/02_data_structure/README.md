# 20.02 분석 결과를 LLM에 전달하는 데이터 구조

회귀·ANOVA·DOE 분석 결과를 LLM 에 전달하기 좋은 **구조화된 payload(dict)** 로 정리하는 패턴을 다룹니다.
각 파일은 책 본문의 동일 번호 코드 블록(`# code_20_02_NN.py` 주석)과 1:1 매핑됩니다.

## 파일 구성

| 파일 | 내용 |
|------|------|
| `code_20_02_01.py` | 다중 회귀 결과 payload — 계수·p-value·모형 적합도·질문 목록 |
| `code_20_02_02.py` | 일원 ANOVA 결과 payload + LLM 호출·응답 활용 (요약/위험/다음 단계) |
| `code_20_02_03.py` | 부분 요인 실험(DOE) 결과 payload — resolution·alias·해석 초안 포함 |
| `code_20_02_04.py` | 같은 형식을 반복 생성하는 payload 빌더 함수 (`build_anova_payload`) |

## 사용법

```bash
python code_20_02_01.py
python code_20_02_02.py
python code_20_02_03.py
python code_20_02_04.py
```

`OPENAI_API_KEY` 가 없으면 mock 응답으로 흐름이 이어지므로 API 키 없이도 실행할 수 있습니다.

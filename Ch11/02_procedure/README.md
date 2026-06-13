# 11.2 완전 요인 실험의 절차

## 원본 코드

- `code_11_02_01.py`: `itertools.product`로 3요인 2수준 ($2^3$) 설계 행렬을 생성하는 예시.
- `code_11_02_02.py`: 8개 처리 조합의 가상 응답값으로 ANOVA 분석을 수행하는 예시.

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

3요인 2수준 완전 요인 설계에 반복 2회를 더해 총 16개 행을 가진다.

| 컬럼 | 설명 |
|---|---|
| A, B, C | 요인 (-1, +1 코딩) |
| Replicate | 반복 번호 (1, 2) |
| y | 모의 응답값 (효과: y = 35 + 5A + 3B + 4C + 2AB + 잡음) |

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

`pandas.read_excel`로 데이터를 로드한 뒤 다음을 수행한다.

1. 데이터 구조와 요인 수준 출력
2. `statsmodels.ols` 로 주효과 + 2차 상호작용 모형 적합
3. ANOVA 테이블 (Type II SS) 출력
4. 효과 크기 (high - low) 와 |Effect| 정렬 표
5. 각 효과의 기여율(%) 계산
6. 효과 부호로부터 최적 조건과 예측 응답 도출
7. 주효과도 PNG (`ExtraCode/main_effects.png`) 저장

## 실행

```bash
python ExtraCode/excel_version.py
```


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

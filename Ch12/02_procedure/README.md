# 12.2 부분 요인 실험의 절차

## 원본 코드

- `code_12_02_01.py`: 2^(4-1) 부분 요인 설계 행렬 구성 (Generator D = ABC) 및 정의 관계 출력.
- `code_12_02_02.py`: 예시 데이터 (`y`) 에 대해 주효과 + 일부 2차 상호작용 ANOVA 분석.

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

2^(4-1) 설계 8 runs. D = A·B·C 의 생성식을 만족한다.

| 컬럼 | 설명 |
|---|---|
| A, B, C, D | 요인 (-1/+1) — D는 ABC로 정의됨 |
| y | 가상 응답값 (효과: 60 + 8A + 5B − 3C + 4D + 2AB + 잡음) |

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

1. Generator 검증 (D == A*B*C)
2. 주효과 + 선택적 2차 상호작용 ANOVA
3. 효과 크기 및 기여율
4. 별칭(교락) 구조 출력
5. 응답 최대화 기준 최적 조건과 예측값


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

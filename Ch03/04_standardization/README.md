# 3.4 데이터의 표준화 (Standardization)

## 파일 구성

| 파일 | 설명 |
|------|------|
| `code_03_04_01.py` | `StandardScaler` Z-점수 표준화 (매출/방문자) |
| `code_03_04_02.py` | `MinMaxScaler` 정규화 (생산량/불량률) |
| `code_03_04_03.py` | 표준화 전후 히스토그램 비교 (키/체중) |
| `ExtraCode/create_sample_data.py` | 학생 20명 × 4과목(국영수과) 점수 Excel 생성 |
| `ExtraCode/sample_data.xlsx` | 생성된 샘플 데이터 |
| `ExtraCode/excel_version_01.py` | Z-점수/Min-Max 직접 계산 + sklearn 비교 + 한 학생 분석 |

## 실행 방법

```bash
python ExtraCode/create_sample_data.py
python ExtraCode/excel_version_01.py
```

## 학습 포인트

- 각 과목의 평균/표준편차를 일부러 다르게 만들어, 같은 원점수라도 과목에 따라 **상대 위치**가 다르다는 점을 Z-점수가 어떻게 드러내는지 직접 확인.
- 수기 계산식 `z = (x − μ) / σ`과 `sklearn StandardScaler` 결과가 일치함을 비교.
- |Z| > 2 기준으로 이상치 후보를 자동 탐지하는 코드 포함.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

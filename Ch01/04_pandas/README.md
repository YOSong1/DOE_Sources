# 1.4 Pandas

## 페이지 정보
- **책**: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
- **페이지 ID**: 324259
- **주제**: DataFrame 생성, 선택, 필터링, 결측값 처리, groupby, 정렬

## 파일 구성

| 파일 | 내용 |
|------|------|
| `code_01_04_01.py` | pandas import |
| `code_01_04_02.py` | 딕셔너리로 DataFrame 생성 |
| `code_01_04_03.py` | CSV/Excel 읽기 (참조용 주석) |
| `code_01_04_04.py` | head/info/describe/shape 등 데이터 확인 |
| `code_01_04_05.py` | 열/행 선택, loc/iloc, 조건 필터링 |
| `code_01_04_06.py` | 열 추가/수정/삭제 |
| `code_01_04_07.py` | 결측값 처리 (isna/dropna/fillna) |
| `code_01_04_08.py` | groupby 집계 |
| `code_01_04_09.py` | sort_values 정렬 |
| `ExtraCode/sample_data.xlsx` | customers(8명, 결측 포함), transactions(15건) |
| `ExtraCode/excel_version_01.py` | 두 시트 merge → 결측 처리 → 그룹 집계까지 통합 분석 |

## 샘플 데이터
- **customers**: Name, Score(일부 NaN), Major(일부 None), Region
- **transactions**: 15건의 거래 (tx_id, customer, amount, category)

## 사용법

```bash
python code_01_04_07.py             # 결측값 처리
python ExtraCode/excel_version_01.py        # 통합 분석 (merge 포함)
```

## 학습 포인트
- 책의 4행짜리 단순 데이터를 실무에 가까운 두 시트 구조(고객/거래)로 확장하여 `merge`까지 자연스럽게 학습할 수 있습니다.
- 결측값 처리 시 평균값을 명시적으로 출력해보면 fillna의 효과를 더 깊이 이해할 수 있습니다.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

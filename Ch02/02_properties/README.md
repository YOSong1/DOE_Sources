# 2.2 확률의 기본 성질

## 페이지 정보
- **책**: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
- **페이지 ID**: 326984
- **주제**: 콜모고로프 공리, 공사건/여사건/합사건의 확률

## 파일 구성

| 파일 | 내용 |
|------|------|
| `code_02_02_01.py` | 100,000회 주사위 시뮬레이션으로 공리적 성질 검증 |
| `ExtraCode/sample_data.xlsx` | 2000회 주사위 시행 + 사건 컬럼 (dice_events) |
| `ExtraCode/excel_version_01.py` | 5가지 공리/성질을 명시적으로 단계별 검증 |

## 샘플 데이터
- **dice_events**: trial, value, is_even(A=짝수), is_mult3(B=3의배수), is_odd(A^c)

## 사용법

```bash
python code_02_02_01.py
python ExtraCode/excel_version_01.py    # 단계별 검증 + 결과 요약
```

## 학습 포인트
- 사건 컬럼(A, B, A^c)을 Excel에 미리 만들어 두면 `mean()` 한 번으로 확률이 추정됩니다.
- 덧셈 법칙은 교집합/합집합 컬럼을 별도로 계산해 비교하면 공식의 의미가 명확해집니다.
- 5가지 검증 결과를 OK/FAIL로 요약 출력하여 자가 진단할 수 있습니다.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

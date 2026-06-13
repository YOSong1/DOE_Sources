# 2.1 확률의 정의

## 페이지 정보
- **책**: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
- **페이지 ID**: 326983
- **주제**: 확률의 세 가지 해석, 표본공간/사건, 대수의 법칙

## 파일 구성

| 파일 | 내용 |
|------|------|
| `code_02_01_01.py` | 동전/주사위 시뮬레이션으로 대수의 법칙 확인 |
| `ExtraCode/sample_data.xlsx` | 1000회 동전(coin_flips), 1000회 주사위(dice_rolls) 시행 로그 |
| `ExtraCode/excel_version_01.py` | 시행 로그를 누적하여 빈도 수렴 그래프(log scale) 출력 |

## 샘플 데이터
- **coin_flips**: 1000개의 H/T 결과 (trial, coin_face)
- **dice_rolls**: 1000개의 1~6 결과 (trial, dice_value)

## 사용법

```bash
python code_02_01_01.py
python ExtraCode/excel_version_01.py    # ExtraCode/law_of_large_numbers.png 생성
```

## 학습 포인트
- 고전적 정의는 **표본공간 분석**(분자/분모)으로, 빈도적 정의는 **반복 실험 데이터**로 확률을 구합니다.
- 누적 빈도를 log scale로 시각화하면 대수의 법칙을 한눈에 확인할 수 있습니다.
- 동일한 시드(42)로 생성한 Excel 데이터를 사용해 책의 결과를 재현합니다.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

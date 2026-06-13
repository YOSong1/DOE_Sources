# 2.3 확률의 기본 법칙

## 페이지 정보
- **책**: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
- **페이지 ID**: 327108
- **주제**: 덧셈 법칙, 곱셈 법칙, 여사건 법칙

## 파일 구성

| 파일 | 내용 |
|------|------|
| `code_02_03_01.py` | 100,000회 카드/주사위 시뮬레이션으로 법칙 검증 |
| `ExtraCode/sample_data.xlsx` | cards(2000회), two_dice(2000회) |
| `ExtraCode/excel_version_01.py` | 시행 로그로 덧셈/곱셈/여사건 법칙을 단계별 분해 |

## 샘플 데이터
- **cards**: trial, suit, rank, is_spade(A), is_ace(B)
- **two_dice**: trial, dice1, dice2, any_six (적어도 한 번 6)

## 사용법

```bash
python code_02_03_01.py
python ExtraCode/excel_version_01.py
```

## 학습 포인트
- 덧셈 법칙의 각 항(P(A), P(B), P(A∩B))을 분리해서 출력하면 공식의 의미를 더 명확히 이해할 수 있습니다.
- 카드 무늬와 숫자의 독립성은 `P(A∩B) ≒ P(A)·P(B)`로 즉시 검증됩니다.
- 여사건 법칙은 "직접 계산하기 어려운 사건"을 "단순한 사건"으로 바꿔주는 핵심 도구입니다.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

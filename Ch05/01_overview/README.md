# 5.1 이산형 확률 분포의 개요

이산 확률 변수의 정의, PMF의 성질, 기댓값/분산의 일반 공식을 정리한 절의 코드.

## 파일
- `code_05_01_01.py` - 책 코드: 주사위 한 개의 E[X], Var(X), SD(X) 계산
- `ExtraCode/make_sample.py` - 주사위 300회, 동전 100회, 카드 200회 관측 빈도 생성
- `ExtraCode/sample_data.xlsx` - 위 데이터 (`dice`, `coin`, `card` 시트)
- `ExtraCode/excel_version_01.py` - Excel `dice` 시트로부터 경험적 PMF → 기댓값/분산 항별 분해 → 이론값과 비교

## 실행
```
python ExtraCode/make_sample.py
python code_05_01_01.py
python ExtraCode/excel_version_01.py
```


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

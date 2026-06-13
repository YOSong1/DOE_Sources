# 4.1 1차원 확률 변수

## 파일 구성

| 파일 | 설명 |
|------|------|
| `code_04_01_01.py` | 이산형 예제: 주사위 PMF와 CDF 시각화 (scipy.stats.randint) |
| `code_04_01_02.py` | 연속형 예제: 표준 정규 분포 PDF와 CDF (scipy.stats.norm) |
| `ExtraCode/create_sample_data.py` | 주사위 600회 시뮬레이션 결과 + 빈도표 Excel 생성 |
| `ExtraCode/sample_data.xlsx` | 굴림결과 시트 + 빈도표 시트 |
| `ExtraCode/excel_version_01.py` | 경험적 PMF/CDF/E[X]/Var(X)를 정의식으로 단계별 계산하고 이론값과 비교 |

## 실행 방법

```bash
python ExtraCode/create_sample_data.py
python ExtraCode/excel_version_01.py
```

## 학습 포인트

- 600회 굴림 실험 결과로 `P̂(X=k)` 를 계산하고 이론 PMF `1/6` 과 비교.
- `E[X]`, `Var(X)` 를 두 가지 공식(편차² 합산 vs `E[X²] − (E[X])²`)으로 동시에 계산하여 일치 확인.
- 표본 크기를 10, 50, 100, 300, 600 으로 늘려가며 **대수의 법칙**을 직접 관찰.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

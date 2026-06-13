# 4.2 2차원 확률 변수

## 파일 구성

| 파일 | 설명 |
|------|------|
| `code_04_02_01.py` | 이산형 결합 분포에서 E[X], E[Y], Cov, ρ 계산 |
| `code_04_02_02.py` | 2차원 정규 분포 시뮬레이션 + 산점도 + 등고선 |
| `ExtraCode/create_sample_data.py` | 키(cm) × 몸무게(kg) 200명 Excel 생성 (ρ ≈ 0.7) |
| `ExtraCode/sample_data.xlsx` | 생성된 샘플 데이터 |
| `ExtraCode/excel_version_01.py` | 결합/주변/조건부 PMF + 독립성 + 공분산/상관계수 + 단위 변환 실험 |

## 실행 방법

```bash
python ExtraCode/create_sample_data.py
python ExtraCode/excel_version_01.py
```

## 학습 포인트

- 연속형 (키, 몸무게)를 구간(bin)으로 묶어 **이산형 결합 PMF**로 변환하는 흐름을 직접 시연.
- 주변 PMF = 행/열 합, 조건부 PMF = 행/열 정규화로 손쉽게 구할 수 있음을 확인.
- 독립 가정 P(X)·P(Y) 와 실제 P(X,Y) 의 차이로 **종속성**을 즉시 시각화.
- 키를 cm → m 로 바꾸면 **공분산은 1/100로 줄지만 상관계수는 그대로**임을 확인.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

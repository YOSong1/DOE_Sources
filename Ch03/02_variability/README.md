# 3.2 데이터 변동성 (Variability)

## 파일 구성

| 파일 | 설명 |
|------|------|
| `code_03_02_01.py` | 범위(Range) 계산 |
| `code_03_02_02.py` | 모분산/표본분산 (ddof) |
| `code_03_02_03.py` | 모표준편차/표본표준편차 |
| `code_03_02_04.py` | A/B 공장 품질 비교 |
| `code_03_02_05.py` | Q1/Q3/IQR 및 이상치 탐지 |
| `code_03_02_06.py` | 변동계수(CV) — 키 vs 체중 비교 |
| `code_03_02_07.py` | 히스토그램 + 박스플롯 |
| `code_03_02_08.py` | 종합 예제: 매출액 모든 변동성 척도 |
| `ExtraCode/create_sample_data.py` | 두 공장 부품 직경 25회 측정 Excel 생성 |
| `ExtraCode/sample_data.xlsx` | 생성된 샘플 데이터 |
| `ExtraCode/excel_version_01.py` | Excel 데이터 → 5가지 변동성 척도 단계별 계산 |

## 실행 방법

```bash
python ExtraCode/create_sample_data.py
python ExtraCode/excel_version_01.py
```

## 학습 포인트

- A 공장(σ=0.3)과 B 공장(σ=1.5)의 평균은 거의 같지만 변동성이 5배 차이.
- 분모 `n` vs `n-1`(자유도)에 따른 분산값 차이를 직접 확인.
- IQR과 변동계수 비교로 정밀공정/일반공정의 품질 차이를 정량화.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

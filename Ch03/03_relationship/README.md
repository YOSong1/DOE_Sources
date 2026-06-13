# 3.3 데이터 관계 분석 (Covariance & Correlation)

## 파일 구성

| 파일 | 설명 |
|------|------|
| `code_03_03_01.py` | 산점도 + 추세선 (기온 vs 아이스크림 판매량) |
| `code_03_03_02.py` | 공분산/상관계수 계산 (np.cov, np.corrcoef, scipy.stats.pearsonr) |
| `ExtraCode/create_sample_data.py` | 학생 25명의 주당 공부시간 vs 시험점수 Excel 생성 |
| `ExtraCode/sample_data.xlsx` | 생성된 샘플 데이터 |
| `ExtraCode/excel_version_01.py` | Excel 데이터 → 공분산/상관계수 단계별 직접 계산 + 단위 변환 실험 |

## 실행 방법

```bash
python ExtraCode/create_sample_data.py
python ExtraCode/excel_version_01.py
```

## 학습 포인트

- 단계별 식: `Cov = Σ(xi-x̄)(yi-ȳ) / (n-1)`, `r = Cov / (sx · sy)` 를 손계산하듯 표시.
- 공부시간 단위를 **시간 → 분**으로 바꾸면 공분산이 60배가 되지만, 상관계수는 그대로.
  → 상관계수의 **단위 무차원성**을 직접 체험.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

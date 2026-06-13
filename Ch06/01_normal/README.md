# 6.1 정규 분포 — 실습 자료

## 파일
- `code_06_01_01.py` — 책 본문 코드 (μ=70, σ=10 가정).
- `ExtraCode/sample_scores.xlsx` — 200명의 시험 점수 샘플 (정규분포에서 생성).
- `ExtraCode/excel_version_01.py` — Excel 데이터를 읽어 표본 평균/표준편차를 추정한 뒤,
  추정된 모수로 동일한 확률 계산을 재현하고 관측 히스토그램과 정규 PDF를 함께 그린다.

## 학습 포인트
1. 책에서는 μ, σ를 고정값으로 가정했지만, 실제로는 표본에서 추정해야 한다.
2. 표준화 변환 z = (x-μ̂)/σ̂를 직접 계산해 PDF 공식의 의미를 체득한다.
3. "관측 비율"과 "정규근사 확률"을 비교해 가정의 타당성을 점검한다.

## 실행
```
python code_06_01_01.py
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

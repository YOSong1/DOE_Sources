# 5.3 이항 분포

## 파일
- `code_05_03_01.py` - n=20, p=0.05 불량품 검사 (PMF, CDF, SF)
- `code_05_03_02.py` - n=20에서 p=0.1/0.3/0.5 PMF 시각화
- `ExtraCode/make_sample.py` - 100배치 x n=10 검사 데이터 생성 (true p=0.08)
- `ExtraCode/sample_data.xlsx` - `inspections` 시트
- `ExtraCode/excel_version_01.py` - p MLE 추정, 표본통계와 이론값 비교, 카이제곱 적합도


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

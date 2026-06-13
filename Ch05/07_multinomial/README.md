# 5.7 다항 분포

## 파일
- `code_05_07_01.py` - 주사위 100회 시뮬레이션, 관측 vs 기대 빈도
- `ExtraCode/make_sample.py` - 객관식 5지선다 500명 응답 (true p=[.1,.2,.35,.25,.1])
- `ExtraCode/sample_data.xlsx` - `responses` (원시), `frequency` (빈도)
- `ExtraCode/excel_version_01.py` - p_i MLE, 다항 PMF, 카이제곱 적합도 검정


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

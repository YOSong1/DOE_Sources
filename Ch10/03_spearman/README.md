# 10.3 스피어만 순위 상관계수 — 실습 자료

- `code_10_03_01.py` — 이상치 포함 데이터에서 피어슨 vs 스피어만.
- `code_10_03_02.py` — 원본/순위 산점도 비교.
- `ExtraCode/sample_with_outlier.xlsx` — 10개 (이상치 1개 포함).
- `ExtraCode/excel_version_01.py` — ρ를 1-6Σd²/(n(n²-1)) 공식으로 직접 계산하고, 이상치 제거 효과를 r/ρ로 비교.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

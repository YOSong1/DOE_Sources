# 7.3 카이제곱 검정 — 실습 자료

- `code_07_03_01.py` — 적합도 검정 (주사위).
- `code_07_03_02.py` — 독립성 검정 (광고 유형 vs 구매).
- `code_07_03_03.py` — 관찰/기대 빈도 비교 시각화.
- `ExtraCode/sample_categorical.xlsx` — 주사위 raw 시행 120회 + 광고-구매 raw 200건.
- `ExtraCode/excel_version_01.py` — raw → crosstab 자동 생성, χ² 수동 검산, Cramer's V 효과 크기 추가.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

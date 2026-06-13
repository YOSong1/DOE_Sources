# 7.4 Z-검정 — 실습 자료

- `code_07_04_01.py` — 단일표본 Z검정 (수면시간).
- `code_07_04_02.py` — 단일비율 Z검정 (캠페인 전환율).
- `code_07_04_03.py` — 두 비율 Z검정 (광고 A vs B).
- `ExtraCode/sample_ztest.xlsx` — 수면시간, AB광고전환 시트.
- `ExtraCode/excel_version_01.py` — raw 클릭 로그를 직접 집계해 두 비율 Z 검정, 수동 검산, 신뢰구간 산출.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

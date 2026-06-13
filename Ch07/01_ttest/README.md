# 7.1 t-검정 — 실습 자료

- `code_07_01_01.py` — 단일표본 t검정 (부품 길이).
- `code_07_01_02.py` — 독립표본(Welch) t검정 (신약 vs 기존약).
- `code_07_01_03.py` — 대응표본 t검정 (운동 전후 혈압).
- `ExtraCode/sample_tests.xlsx` — 세 시트: 부품길이, 약물효과, 운동전후혈압.
- `ExtraCode/excel_version_01.py` — 세 유형의 t검정을 모두 수행하고 Cohen's d 효과 크기까지 추가 계산.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

# 7.2 F-검정 — 실습 자료

- `code_07_02_01.py` — 분산비 F검정 (두 라인).
- `code_07_02_02.py` — 일원 ANOVA (세 비료).
- `ExtraCode/sample_variance_anova.xlsx` — 생산라인, 비료성장 두 시트.
- `ExtraCode/excel_version_01.py` — F = MS_between/MS_within을 SS 분해로 직접 검산하고 Levene 비교.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

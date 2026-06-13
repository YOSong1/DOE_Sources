# 9.1 일원배치 ANOVA — 실습 자료

- `code_09_01_01.py` — Levene + scipy ANOVA + statsmodels ANOVA 표.
- `code_09_01_02.py` — 박스플롯 + 집단 평균 막대.
- `code_09_01_03.py` — Tukey HSD 사후검정.
- `ExtraCode/sample_teaching_methods.xlsx` — 24명 (교수법 A/B/C, 시험점수).
- `ExtraCode/excel_version_01.py` — Levene → ANOVA → Tukey HSD → η² 효과 크기까지 모두 수행.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

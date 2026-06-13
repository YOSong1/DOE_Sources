# 9.4 MANOVA — 실습 자료

- `code_09_04_01.py` — MANOVA (Wilks, Pillai, ...).
- `code_09_04_02.py` — Box's M 공분산 동질성.
- `code_09_04_03.py` — 사후 단변량 ANOVA + Tukey HSD.
- `code_09_04_04.py` — 집단별 산점도.
- `ExtraCode/sample_education_scores.xlsx` — 45명 (education, math, reading).
- `ExtraCode/excel_version_01.py` — 종속변수 상관 점검, MANOVA, 단변량 ANOVA + η², 시각화 종합.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

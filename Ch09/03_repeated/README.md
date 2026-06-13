# 9.3 반복 측정 ANOVA — 실습 자료

- `code_09_03_01.py` — pingouin rm_anova + Mauchly 구형성 검정.
- `code_09_03_02.py` — 스파게티 + 박스플롯 시각화.
- `code_09_03_03.py` — Bonferroni 보정 사후검정.
- `ExtraCode/sample_memory_test.xlsx` — 10명 × 3시점 = 30행 long format.
- `ExtraCode/excel_version_01.py` — long↔wide 변환, 구형성 점검, GG 보정, 사후검정, 시각화 통합.

학습 포인트: 반복 측정 데이터 구조(long format), 구형성 가정, 보정 절차.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

# 6.4 t 분포 — 실습 자료

- `code_06_04_01.py` — 본문: 10명 환자 데이터 단일표본 t검정.
- `code_06_04_02.py` — 자유도별 t분포 PDF + 표준정규분포 비교.
- `ExtraCode/sample_blood_pressure.xlsx` — 신약 투여 후 25명의 혈압.
- `ExtraCode/excel_version_01.py` — 표본 통계량으로 t = (x̄-μ₀)/(s/√n)을 직접 계산하고
  scipy 결과와 비교한 뒤 95% 신뢰구간으로 H₀ 판정.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

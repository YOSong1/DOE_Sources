# 6.6 감마 분포 — 실습 자료

- `code_06_06_01.py` — α=3, β=2 보험 청구 대기시간 예제.
- `code_06_06_02.py` — α별 PDF 비교.
- `ExtraCode/sample_insurance_claims.xlsx` — 청구 간격(일) 200건.
- `ExtraCode/excel_version_01.py` — 적률추정(MoM)과 MLE로 α, β를 추정해 PDF 적합과 핵심 확률을 재계산.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

# 8.1 단순 선형 회귀 — 실습 자료

- `code_08_01_01.py` — 광고비 vs 매출 가상 데이터로 선형 회귀 적합 + statsmodels 요약.
- `ExtraCode/sample_ad_sales.xlsx` — 50개 관측치 (광고비, 매출).
- `ExtraCode/excel_version_01.py` — Excel 데이터로 β₀, β₁을 정규방정식으로 직접 계산해 OLS와 비교,
  4-패널 잔차 진단 (적합선, 잔차-예측값, Q-Q, 히스토그램) 수행.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

# 6.8 Cauchy 분포 — 실습 자료

- `code_06_08_01.py` — Cauchy vs Normal PDF, 꼬리 확률 비교.
- `code_06_08_02.py` — 누적 표본 평균이 수렴하지 않음을 시뮬레이션.
- `ExtraCode/sample_stock_returns.xlsx` — Cauchy로 생성한 일간 수익률 500일.
- `ExtraCode/excel_version_01.py` — 누적 평균/중앙값 비교, Cauchy vs Normal 적합 PDF 시각화.

학습 포인트: 무한 분산 분포에서 평균의 비안정성, 중앙값/IQR이 더 적절한 추정량인 이유.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

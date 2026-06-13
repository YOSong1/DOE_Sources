# 6.7 Weibull 분포 — 실습 자료

- `code_06_07_01.py` — k=2, λ=1000 시간 가정한 전구 수명 예제 + k별 PDF 비교.
- `ExtraCode/sample_bulb_lifetime.xlsx` — 전구 수명 200개 (Weibull(2,1000) 샘플).
- `ExtraCode/excel_version_01.py` — MLE 적합으로 k̂, λ̂를 구하고 평균·표준편차를 감마함수로 검산,
  생존함수를 시각화하여 신뢰도 공학 관점에서 해석.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

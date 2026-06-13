# 6.2 지수 분포 — 실습 자료

- `code_06_02_01.py` — 책 본문 코드 (λ=2 고정 예시).
- `ExtraCode/sample_call_intervals.xlsx` — 콜센터 통화 간격(분) 300건 (지수분포 샘플).
- `ExtraCode/excel_version_01.py` — 실데이터 평균으로 λ̂=1/x̄을 추정해 확률을 재계산하고 PDF를 적합한다.

학습 포인트: SciPy의 `scale = 1/λ` 관례, 적률추정 절차, 관측 비율과 이론 확률 비교.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

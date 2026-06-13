# 8.2 다중 회귀 — 실습 자료

- `code_08_02_01.py` — 가상 자동차 데이터 다중회귀 + VIF.
- `ExtraCode/sample_car_price.xlsx` — 100대 (마력, 연비, 연식, 가격).
- `ExtraCode/excel_version_01.py` — β̂=(X'X)⁻¹X'y 행렬식 직접 계산, 조정된 R², VIF, 실제·잔차 시각화.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

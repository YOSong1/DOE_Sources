# 10.5 점-이계열 상관계수 — 실습 자료

- `code_10_05_01.py` — r_pb 계산.
- `code_10_05_02.py` — 박스플롯 시각화.
- `ExtraCode/sample_pass_score.xlsx` — 20명 (시험점수, 합격여부).
- `ExtraCode/excel_version_01.py` — r_pb = (M₁-M₀)/s·√(pq) 공식 직접 계산,
  pearsonr/pointbiserialr/독립 t-검정의 수학적 동등성을 확인.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

# 10.2 피어슨 상관계수 — 실습 자료

- `code_10_02_01.py` — scipy/pandas로 r 계산.
- `code_10_02_02.py` — 산점도 + 회귀선.
- `ExtraCode/sample_study_score.xlsx` — 10명 (공부시간, 시험점수).
- `ExtraCode/excel_version_01.py` — r을 공분산/표준편차로 직접 계산, Fisher Z 변환으로 95% CI 산출, R² 해석.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

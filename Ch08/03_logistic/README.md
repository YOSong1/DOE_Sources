# 8.3 로지스틱 회귀 — 실습 자료

- `code_08_03_01.py` — 가상 스팸 분류 + 혼동행렬/ROC + statsmodels Logit 요약.
- `ExtraCode/sample_spam.xlsx` — 500건 (단어수, 링크수, 대문자비율, 스팸여부).
- `ExtraCode/excel_version_01.py` — Excel 데이터 학습, 시그모이드 손계산, 임계값별 정밀도/재현율 비교, PR 곡선 추가.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

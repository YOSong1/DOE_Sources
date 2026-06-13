# 6.3 카이제곱 분포 — 실습 자료

- `code_06_03_01.py` — 책 본문: 성별 x 감염 교차표를 직접 입력해 chi2_contingency 실행.
- `code_06_03_02.py` — 자유도별 카이제곱 PDF 비교 시각화.
- `ExtraCode/sample_infection.xlsx` — 200명 raw 환자 데이터 (성별, 감염여부).
- `ExtraCode/excel_version_01.py` — raw 데이터에서 `pd.crosstab`으로 교차표를 만든 뒤
  카이제곱 통계량을 셀별로 손계산해 chi2_contingency 결과와 일치하는지 검산한다.

학습 포인트: 분할표 작성, 기대빈도 공식 E = (행합×열합)/총계, Σ(O-E)²/E의 의미.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

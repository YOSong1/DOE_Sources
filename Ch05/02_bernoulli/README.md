# 5.2 베르누이 분포

## 파일
- `code_05_02_01.py` - 책 코드: scipy.stats.bernoulli로 PMF/기댓값/분산/난수
- `code_05_02_02.py` - 책 코드: p=0.3/0.5/0.7 PMF 시각화
- `ExtraCode/make_sample.py` - 광고 클릭 0/1 데이터 500행 생성 (true p=0.18)
- `ExtraCode/sample_data.xlsx` - ad_clicks 시트
- `ExtraCode/excel_version_01.py` - p MLE 추정, 표본 통계량/이론값 비교, 95% CI

## 실행
```
python ExtraCode/make_sample.py && python code_05_02_01.py && python ExtraCode/excel_version_01.py
```


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

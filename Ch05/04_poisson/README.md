# 5.4 포아송 분포

## 파일
- `code_05_04_01.py` - λ=3 콜센터 예시 (PMF, mean=var, sf)
- `code_05_04_02.py` - λ=1,3,5,10 PMF 비교 시각화
- `ExtraCode/make_sample.py` - 24h*30d=720시간의 시간당 콜수 (true λ=4.5)
- `ExtraCode/sample_data.xlsx` - `callcenter` 시트
- `ExtraCode/excel_version_01.py` - λ MLE, 평균/분산 비교, 적합도, 운영 분위수


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

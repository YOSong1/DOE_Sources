# 5.5 기하 분포

## 파일
- `code_05_05_01.py` - p=0.3 상담원 연결 (PMF/CDF/PPF/mean/var)
- `code_05_05_02.py` - p=0.1/0.3/0.5 PMF 라인 비교 시각화
- `ExtraCode/make_sample.py` - 200명 가챠 첫 SSR까지 시도 횟수 (true p=0.03)
- `ExtraCode/sample_data.xlsx` - `gacha` 시트
- `ExtraCode/excel_version_01.py` - p MLE, 적합도, 무기억성 점검, 분위수


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

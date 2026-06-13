# 5.6 초기하 분포

## 파일
- `code_05_06_01.py` - 불량품 검사(M=20,n=5,N=5) + 로또(45/6)
- `code_05_06_02.py` - 불량품 검사 PMF 시각화
- `ExtraCode/make_sample.py` - M=100,n=12,N=10 검사를 200회 반복
- `ExtraCode/sample_data.xlsx` - `hyper_inspect` 시트
- `ExtraCode/excel_version_01.py` - 표본 통계량 vs 초기하/이항 이론, 유한 모집단 보정계수


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

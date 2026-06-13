# 5.8 포아송-이항 분포

## 파일
- `code_05_08_01.py` - DP 알고리즘으로 PMF 계산 (10경기 예시)
- `code_05_08_02.py` - PMF 시각화
- `ExtraCode/make_sample.py` - 30경기 시즌 일정 + 경기별 승률 p_i + 실현 승패
- `ExtraCode/sample_data.xlsx` - `season` 시트
- `ExtraCode/excel_version_01.py` - 포아송-이항 vs 이항 근사 vs 포아송 근사 PMF 비교, Le Cam 상한


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

# 6.5 F 분포 — 실습 자료

- `code_06_05_01.py` — 본문: 두 라인 품질 점수 양측 F검정.
- `code_06_05_02.py` — 자유도 조합별 F PDF 비교.
- `ExtraCode/sample_quality.xlsx` — Line_A / Line_B 시트 (각 30 배치).
- `ExtraCode/excel_version_01.py` — Excel 시트별로 표본분산을 구한 뒤 양측 p-value(비대칭 처리)와 분산비 신뢰구간을 계산.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

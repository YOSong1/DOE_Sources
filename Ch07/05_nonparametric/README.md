# 7.5 비모수 검정 — 실습 자료

- `code_07_05_01.py` — Mann-Whitney U (A/B 그룹).
- `code_07_05_02.py` — Wilcoxon 부호 순위 (명상 전후).
- `code_07_05_03.py` — Kruskal-Wallis (세 식단).
- `ExtraCode/sample_nonparam.xlsx` — 클릭시간, 명상스트레스, 식단감량 세 시트.
- `ExtraCode/excel_version_01.py` — Shapiro로 정규성을 진단해 비모수 사용을 정당화하고, 같은 데이터에 모수 검정도 적용해 결과를 대비.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

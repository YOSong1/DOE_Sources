# 10.4 켄달의 타우 — 실습 자료

- `code_10_04_01.py` — 두 평가자 순위로 τ 계산 + 스피어만 비교.
- `code_10_04_02.py` — 순위 막대 비교 시각화.
- `ExtraCode/sample_movie_ranks.xlsx` — 영화 8편 (평가자 A, B 순위).
- `ExtraCode/excel_version_01.py` — 모든 쌍을 itertools로 enumerate, 일치/불일치/동점 직접 세고 τ_a 손계산.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

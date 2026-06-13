# 17.2 완전 무작위 설계의 절차

## 원본 코드

- `code_17_02_01.py` — 책 본문(page 324459)의 `random.shuffle` 예시. 30개 실험 단위를 A/B/C 세 처리에 10개씩 무작위로 배정합니다.

## 샘플 데이터

`ExtraCode/sample_data.xlsx`는 UnitID 1–30 한 컬럼만 들어 있는 단순한 시트입니다. Excel 활용 버전이 실행되면 `assignment`라는 새 시트가 자동 추가됩니다.

## Excel 활용 버전

`ExtraCode/excel_version.py`는 다음을 수행합니다.

1. `pd.read_excel`로 실험 단위 풀 로드
2. `random.Random(SEED)`로 재현 가능한 무작위화 수행 (SEED=2026)
3. 처리 A/B/C 배정 결과를 출력
4. 결과 배정표를 `assignment` 시트로 같은 xlsx에 저장 → 무작위화 절차의 문서화

원본 코드와의 차이는 (a) 시드 고정으로 재현성을 확보하고 (b) 결과를 Excel에 보관해 사후 검증이 가능하다는 점입니다.

## 실행

```bash
python code_17_02_01.py
python ExtraCode/excel_version.py
```

필요 패키지: `pandas`, `openpyxl`.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

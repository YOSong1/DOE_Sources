# 17.5 연습 문제: 교육용 SW의 효과 비교 (CRD)

## 원본 코드

- `code_17_05_01.py` — `np.random.seed(999)` 기반 시험 점수 데이터 생성. Version A/B/C 그룹당 10명, 평균 75/82/77, 표준편차 8.

## 샘플 데이터

`ExtraCode/sample_data.xlsx`는 `Version`, `Score` 두 컬럼의 tidy format (30행)입니다.

## Excel 활용 버전

`ExtraCode/excel_version.py`는 연습 문제 5단계를 모두 다룹니다.

1. Excel 로드와 그룹별 기술 통계
2. `f_oneway`로 일원분산분석
3. p < 0.05인 경우 **자동으로 Tukey HSD 사후검정** 호출 → "어떤 버전 쌍이 다른가" 답변
4. 박스플롯 시각화

## 실행

```bash
python code_17_05_01.py
python ExtraCode/excel_version.py
```

필요 패키지: `pandas`, `scipy`, `statsmodels`, `matplotlib`, `openpyxl`.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

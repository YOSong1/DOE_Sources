# 16.5 연습 문제: 신소재 인장 강도 최적화 (Box-Behnken)

## 원본 코드

- `code_16_05_01.py` — 책 본문(page 324336)에서 제공하는 `np.random.seed(888)` 기반 가상 데이터 생성 코드. 3요인 × 3수준 BBD 15회 실험을 생성합니다.

## 샘플 데이터

`ExtraCode/sample_data.xlsx`에는 `code_16_05_01.py`가 생성하는 데이터와 동일한 15행이 저장돼 있으며, 코드화 변수(`X1_coded`, `X2_coded`, `X3_coded`)와 실제 단위(`Heat_Treatment_Temp`, `Alloy_A_Percentage`, `Rolling_Speed`)가 함께 들어 있어 회귀 적합과 최적 조건 해석을 같은 시트에서 수행할 수 있습니다.

## Excel 활용 버전

`ExtraCode/excel_version.py`는 다음 흐름으로 분석합니다.

1. `pd.read_excel`로 데이터 로드 후 기술 통계 출력
2. `statsmodels.formula.api.ols`로 2차 다항 회귀 모형 적합 (주효과 + 2차항 + 모든 2-요인 상호작용)
3. `model.summary()` 출력과 유의 항(p < 0.05) 자동 추출
4. `scipy.optimize.minimize`로 `[-1, +1]³` 안에서 인장 강도 최대화
5. 코드값 → 실제 단위로 변환하여 보고

## 실행

```bash
python code_16_05_01.py
python ExtraCode/excel_version.py
```

필요 패키지: `numpy`, `pandas`, `statsmodels`, `scipy`, `matplotlib`, `openpyxl`.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

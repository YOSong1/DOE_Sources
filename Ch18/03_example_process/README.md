# 18.3 예제로 이해: 공정 처리 시간의 반복 실험 분석

## 원본 코드

- `code_18_03_01.py` — 3수준(A/B/C) × 5반복 가상 데이터 생성 (`np.random.seed(42)`)
- `code_18_03_02.py` — 기술 통계와 박스플롯
- `code_18_03_03.py` — `statsmodels.formula.api.ols` + `anova_lm`으로 일원 ANOVA

세 파일 모두 책 본문(page 324299) 코드 그대로입니다.

## 샘플 데이터

`ExtraCode/sample_data.xlsx`에 다음 컬럼이 들어 있습니다.

| 컬럼 | 의미 |
|---|---|
| ProcessTimeLevel | 처리 수준 (A / B / C) |
| Replication | 처리 내 반복 번호 (1–5) |
| Measurement | 측정값 |

총 15행 = 3수준 × 5반복.

## Excel 활용 버전

`ExtraCode/excel_version.py`는 \"반복 실험\" 챕터의 핵심 메시지에 맞춰 구성했습니다.

1. 데이터 구조 점검: 수준 수 k와 처리당 반복 n을 자동 추출
2. 그룹별 평균·표준편차
3. ANOVA 결과 출력
4. **자유도 분해**: `df_treat = k-1`, `df_error = N-k` 직접 계산 → 반복이 없으면 검정 자체 불가
5. **처리 평균의 표준오차** SE = √(MSE/n) 계산 → 반복 n을 늘리면 정밀도가 1/√n 비율로 향상되는 점을 수치로 확인

## 실행

```bash
python code_18_03_01.py
python code_18_03_02.py
python code_18_03_03.py
python ExtraCode/excel_version.py
```

필요 패키지: `numpy`, `pandas`, `statsmodels`, `matplotlib`, `openpyxl`.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

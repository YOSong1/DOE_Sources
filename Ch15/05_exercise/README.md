# 15.5 연습 문제 — 서로 다른 학습 방법의 효과 비교 (RCBD)

## 원본 코드

- `code_15_05_01.py`: 3 블록(성취 수준) × 3 처리(학습 방법) × 반복 2회 = 18행 가상 데이터 생성.

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

| 컬럼 | 설명 |
|---|---|
| Block | Block1_High / Block2_Mid / Block3_Low |
| Treatment | A / B / C |
| Score | 문제 해결 능력 점수 (0~100) |

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

1. 데이터 구조 + 블록×처리 평균 표
2. RCBD ANOVA (Type II) — 처리/블록 효과 유의성
3. 블록화 효율: ε = MSE_CRD / MSE_RCBD
4. Tukey HSD 사후 검정으로 처리 쌍별 유의 차이 식별
5. 학습 방법별 평균 점수 + 95% CI 시각화 (`ExtraCode/treatment_means.png`)
6. 평균 점수가 가장 높은 학습 방법 자동 추천

## 실행

```bash
python ExtraCode/excel_version.py
```


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

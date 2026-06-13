# 15.3 예제로 이해: 조미료 선호도의 난괴법 분석

## 원본 코드

- `code_15_03_01.py`: 4 블록 × 3 처리 RCBD 데이터 구성, ANOVA, 처리별/블록별 평균 시각화의 전체 코드.

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

책의 표 데이터 (12 rows) 를 그대로 담는다.

| 컬럼 | 설명 |
|---|---|
| Block | Block1~Block4 (소비자 집단) |
| Treatment | A / B / C (조미료) |
| Score | 선호도 점수 (1~10) |

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

1. 데이터 구조 + 블록×처리 cross-tab
2. RCBD ANOVA (Type II)
3. 블록화 효율: ε = MSE_CRD / MSE_RCBD
   - >1 이면 블록화가 정밀도 향상에 기여
4. Tukey HSD 사후 검정으로 처리 쌍별 유의 차이 식별
5. 평균 점수 최대 처리 자동 출력
6. 처리별/블록별 평균 막대그래프 PNG (`ExtraCode/means.png`)

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

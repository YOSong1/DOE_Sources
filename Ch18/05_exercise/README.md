# 18.5 연습 문제: 세정제 3종의 세척 효과 비교

## 원본 코드

- `code_18_05_01.py` — `np.random.seed(101)` 기반 데이터 생성 (세정제 A/B/C × 6반복, 평균 15/10/12 mg, 망소특성)

## 샘플 데이터

`ExtraCode/sample_data.xlsx` 컬럼:

| 컬럼 | 의미 |
|---|---|
| Detergent | 세정제 종류 (A / B / C) |
| Replication | 반복 번호 (1–6) |
| Contaminant_mg | 세척 후 남은 오염물 양 (낮을수록 좋음) |

총 18행 = 3종 × 6반복.

## Excel 활용 버전

`ExtraCode/excel_version.py`는 연습 문제의 모든 요구사항을 다룹니다.

1. 기술 통계와 데이터 구조 확인
2. `f_oneway`로 ANOVA, `df_error = N - k` 직접 계산
3. p < 0.05인 경우 Tukey HSD 사후검정 자동 수행
4. 망소특성 해석: 평균 오염물이 가장 적은 세정제 자동 출력
5. 박스플롯 시각화

## 실행

```bash
python code_18_05_01.py
python ExtraCode/excel_version.py
```

필요 패키지: `numpy`, `pandas`, `scipy`, `statsmodels`, `matplotlib`, `openpyxl`.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

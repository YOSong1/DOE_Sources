# 12.3 예제로 이해: 반도체 식각 공정의 부분 요인 실험

## 원본 코드

- `code_12_03_01.py`: `pyDOE2.fracfact('a b c ab ac')` 로 2^(5-2) 설계 행렬 생성, 실제 단위 변환, 식각률 결과 데이터 매핑.
- `code_12_03_02.py`: 주효과 계산, 교락 구조, 회귀/ANOVA, 주효과도, 파레토 차트, 결과 종합, Fold-over 설계까지의 전체 분석 코드 (단일 세션으로 실행).

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

책의 표 (`Etch_Rate` = [155, 320, 190, 365, 175, 340, 205, 410]) 을 그대로 담고, 실제 단위 5개 열을 추가했다.

| 컬럼 | 설명 |
|---|---|
| A, B, C, D, E | 코딩 수준 (-1/+1). D = A·B, E = A·C |
| Etch_Rate | 식각률 (nm/min) |
| RF_Power_W, Gas_Pressure_mTorr, Gas_Flow_sccm, Wafer_Temp_C, Etch_Time_min | 실제 단위 |

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

1. Generator (D=AB, E=AC) 검증
2. 주효과 계산
3. 회귀 + ANOVA + 효과/계수/p값 통합표
4. 파레토 차트 PNG 저장 (`ExtraCode/pareto.png`)
5. 교락 구조 출력
6. 효과 부호로부터 최대화 최적 조건과 예측 응답

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

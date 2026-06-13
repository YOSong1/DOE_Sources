# 11.3 예제로 이해: 초콜릿 코팅 품질의 완전 요인 실험

## 원본 코드

- `code_11_03_01.py`: 3요인 2수준 ($2^3$) × 반복 3회의 가상 실험 데이터 생성.
- `code_11_03_02.py`: 전체 모델 (모든 상호작용) 과 간단한 모델 비교 적합.
- `code_11_03_03.py`: 주효과 박스플롯, 상호작용 그림, 잔차 진단 시각화.
- `code_11_03_04.py`: 간단한 모델의 ANOVA 테이블 출력.

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

책의 데이터 생성 로직과 동일한 시드(`seed=42`)를 사용해 24개 행을 생성한다.

| 컬럼 | 설명 |
|---|---|
| Coating_Temperature | 30 / 35 °C |
| Mixing_Speed | 50 / 100 rpm |
| Cooling_Time | 5 / 10 분 |
| Replicate | 1, 2, 3 |
| Coating_Quality | 0~100점 모의 품질 점수 |

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

다음을 한 단계 더 사고할 수 있도록 출력한다.

1. 데이터 구조 및 조건별 반복 수 확인
2. 전체 모형 / 간단한 모형 R^2 비교
3. ANOVA 테이블 (Type II)
4. 각 항의 기여율(%)
5. 주효과 크기 (high - low) 와 최적 조건
6. 주효과 박스플롯, 상호작용 플롯 PNG 저장
7. 해석 요약 메시지 (권장 조건)

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

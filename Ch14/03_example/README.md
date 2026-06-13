# 14.3 예제로 이해: 온도·압력·시간의 L9 직교배열 최적화

## 원본 코드

- `code_14_03_01.py`: L9 직교배열 구성, 가상 출력값 생성, 망대특성 S/N 비 계산, 인자별 주효과 분석 및 시각화 (책의 코드를 단일 파일로 통합).

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

L9(3⁴) 직교배열에 각 조건당 반복 3회를 더한 27행. S/N 비 계산을 의미있게 하기 위해 반복을 포함.

| 컬럼 | 설명 |
|---|---|
| Run | 1~9 (L9 배열 번호) |
| A_Temp | 온도 (180, 200, 220) |
| B_Pressure | 압력 (1, 2, 3) |
| C_Time | 시간 (10, 15, 20) |
| Rep | 반복 (1~3) |
| Response | 가상 출력값 |

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

1. 원시 데이터 + Run 단위 평균/표준편차/S/N(망대) 집계
2. 인자별 평균 S/N (주효과)
3. ANOVA on S/N — 기여율(%) 자동 계산
4. S/N 최대화 기준 최적 조건 도출
5. 인자별 주효과도 PNG (`ExtraCode/main_effects_sn.png`)

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

# 14.5 연습 문제 — 엔진 파라미터 최적화

## 원본 코드

- `code_14_05_01.py`: L9 직교배열로 3요인 3수준 (점화 시점/연료 분사압/공기흡입량) 가상 연비 데이터 생성.

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

L9 9 runs. 책의 효과 사전(`effect_A/B/C`)을 재현한 가상 연비.

| 컬럼 | 설명 |
|---|---|
| Run | 1~9 |
| Ignition_Timing | 점화 시점 (10, 12, 14 BTDC°) |
| Fuel_Pressure | 연료 분사압 (100, 120, 140 bar) |
| Air_Intake | 공기흡입량 (300, 350, 400 L/min) |
| Fuel_Efficiency | 연비 (km/L) |

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

1. 데이터 구조 확인
2. 망대특성 S/N비 계산 (n=1 가정)
3. 인자별 평균 S/N 및 평균 연비 비교
4. S/N 최대화 vs 평균 최대화 — 두 기준의 최적 조건 비교
5. 인자별 S/N 주효과도 PNG (`ExtraCode/sn_effects.png`)

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

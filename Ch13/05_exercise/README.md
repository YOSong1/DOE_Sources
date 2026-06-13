# 13.5 연습 문제 — 제빵 공정 최적화 (응답 표면 분석)

## 원본 코드

- `code_13_05_01.py`: 발효 시간(60~120분)과 굽는 온도(180~220°C) 두 요인의 30개 가상 실험점과 부드러움 점수를 생성.

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

| 컬럼 | 설명 |
|---|---|
| Fermentation_Time | 발효 시간 (분, 60~120 균일 샘플) |
| Baking_Temperature | 굽는 온도 (°C, 180~220 균일 샘플) |
| Softness_Score | 부드러움 점수 (0~100, 높을수록 좋음) |

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

1. 데이터 요약 통계
2. 2차 다항 회귀 모형 적합 (R², F-test)
3. 정상점 (실제 단위) 계산 + 고유값으로 유형 판별
4. 등고선도 (실험점 + 정상점) PNG (`ExtraCode/contour.png`)
5. 권장 공정 조건 출력 (정상점이 영역 밖이면 격자 최대점 사용)

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

# 13.3 예제로 이해: 2요인 공정의 응답 표면 분석

## 원본 코드

- `code_13_03_01.py`: 5x5 격자 실험점 생성, 가상 2차 식으로 반응값 시뮬레이션, OLS로 적합, 3D 표면 시각화의 전체 코드를 한 파일에 모았다.

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

x1, x2 범위 [-2, 2] 의 5x5 격자 (25 runs). 참(true) 모형:

`y = 5 + 2 x1 + 3 x2 + 1.5 x1² + 1.0 x2² + 1.2 x1 x2 + ε,  ε ~ N(0, 0.5²)`

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

1. 데이터 구조 확인
2. 2차 다항 회귀 적합 R², Adj R²
3. 추정 계수 vs 참값 비교 표 (오차)
4. 정상점 계산 + 고유값으로 유형 판별
5. 3D 응답 표면 PNG (`ExtraCode/surface3d.png`)

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

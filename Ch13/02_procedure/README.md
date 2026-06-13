# 13.2 응답 표면 방법론의 일반적인 절차

## 원본 코드

- `code_13_02_01.py`: 2요인 CCD 예시 데이터로 2차 모형 적합 + ANOVA.
- `code_13_02_02.py`: 가상의 2차 모형의 반응 표면 등고선도 시각화.

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

2요인 회전가능 CCD (α = √2). 11 runs:
- factorial points: 4개 (±1, ±1)
- axial points: 4개 (±√2, 0), (0, ±√2)
- center points: 3개 (0, 0)

| 컬럼 | 설명 |
|---|---|
| x1, x2 | 코딩 수준 |
| y | 가상 응답값 (참 표면: 90 − 5x1² − 3x2² + 2x1x2 + x1 + 2x2) |

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

1. CCD 데이터 구조 분류 (factorial/axial/center)
2. 2차 모형 적합 R², Adj R²
3. ANOVA 테이블
4. 회귀 계수로부터 정상점 `x* = -0.5 B^-1 b` 계산
5. B 행렬 고유값으로 최적점 유형 (Max/Min/Saddle) 판별
6. 등고선도와 정상점 PNG 저장

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

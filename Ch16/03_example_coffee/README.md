# 16.3 예제로 이해: 커피 머신 조건의 Box-Behnken 최적화

## 원본 코드

- `code_16_03_01.py` — 데이터 입력, 설계 행렬 X 구성, β = (XᵀX)⁻¹XᵀY로 회귀 계수 계산, 3D 반응 표면 시각화
- `code_16_03_02.py` — `scipy.optimize.minimize`로 경계 제약 [−1, 1]³ 안에서 최적 조건 탐색

두 파일 모두 책 본문(page 324368)의 코드 블록을 그대로 옮긴 것입니다.

## 샘플 데이터

`ExtraCode/sample_data.xlsx` 단일 시트에 다음 컬럼이 들어 있습니다.

| 컬럼 | 의미 |
|---|---|
| Run | 실험 번호 (1–15) |
| X1_Temperature_C | 물의 온도 (실제 단위, °C) |
| X2_Time_sec | 추출 시간 (실제 단위, 초) |
| X3_Beans_g | 원두의 양 (실제 단위, g) |
| X1_coded / X2_coded / X3_coded | 코드화 수준 (−1, 0, +1) |
| Y_TasteScore | 측정된 맛 점수 |

15행 = 모서리 중점 12개 + 중심점 3개로, 3요인 Box-Behnken 설계의 표준 구조입니다.

## Excel 활용 버전

`ExtraCode/excel_version.py`는 단순 복사가 아닌, 다음 순서로 사고를 돕도록 작성했습니다.

1. `pd.read_excel`로 데이터 로드 후 head/중심점 개수 확인
2. 코드화 컬럼으로 설계 행렬 X 생성 → β 계산
3. β를 1차/상호작용/2차로 분리하고 |coef| 기준 가장 큰 1차 효과 출력
4. 2차항 부호로 곡률 형태(U 또는 ∩) 자동 진단
5. `minimize`로 경계 제약 최적점 도출
6. 실제 단위 변환은 Excel의 (실제값, 코드값) 쌍에서 자동으로 lo/hi를 읽어 계산

## 실행

```bash
python code_16_03_01.py
python code_16_03_02.py
python ExtraCode/excel_version.py
```

필요 패키지: `numpy`, `pandas`, `scipy`, `matplotlib`, `openpyxl`.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

# 1.3 Numpy

## 페이지 정보
- **책**: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
- **페이지 ID**: 324207
- **주제**: 배열 생성, 인덱싱, 벡터화, 통계 함수, 난수, 형태 변환

## 파일 구성

| 파일 | 내용 |
|------|------|
| `code_01_03_01.py` | NumPy import |
| `code_01_03_02.py` | 배열 생성 (array, zeros, ones, eye, arange, linspace) |
| `code_01_03_03.py` | 1차원 인덱싱/슬라이싱 |
| `code_01_03_04.py` | 2차원 인덱싱 |
| `code_01_03_05.py` | 벡터화 연산과 내적 |
| `code_01_03_06.py` | 주요 통계 함수 (mean, median, std, var, ...) |
| `code_01_03_07.py` | 난수 생성 (normal, uniform, randint) |
| `code_01_03_08.py` | reshape / flatten / 전치 |
| `ExtraCode/sample_data.xlsx` | 제품 12개 측정값 행렬(products), 학생 8명 점수(scores) |
| `ExtraCode/excel_version_01.py` | Excel → NumPy 변환, z-score 표준화, 통계 일괄 적용, 가중 내적 |

## 샘플 데이터
- **products 시트**: 제품 12개의 length_mm, diameter_mm, weight_g (정규분포 기반)
- **scores 시트**: 책 원본 점수 `[88, 92, 76, 100, 64, 85, 91, 78]`

## 사용법

```bash
python code_01_03_06.py            # 통계 함수
python ExtraCode/excel_version_01.py       # Excel 활용 통합 분석
```

## 학습 포인트
- DataFrame을 `.to_numpy()`로 변환하면 NumPy의 모든 기능을 사용할 수 있습니다.
- z-score 표준화는 브로드캐스팅의 대표 예제로, (n×3) 배열에서 (3,) 평균/표준편차를 빼고 나누는 연산이 자동으로 처리됩니다.
- `np.percentile`로 사분위수를 구하면 IQR을 통해 이상치 탐지의 기초를 만들 수 있습니다.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

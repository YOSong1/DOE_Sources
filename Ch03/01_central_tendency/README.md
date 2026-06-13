# 3.1 데이터 중심 척도 (Central Tendency)

## 파일 구성

| 파일 | 설명 |
|------|------|
| `code_03_01_01.py` | 책 본문 코드: numpy/scipy로 평균/중앙값/최빈값 계산 |
| `code_03_01_02.py` | 책 본문 코드: 히스토그램 위에 세 척도 시각화 |
| `ExtraCode/create_sample_data.py` | 학생 시험 점수 30명 Excel 샘플 생성 (이상치 2명 포함) |
| `ExtraCode/sample_data.xlsx` | 생성된 샘플 데이터 |
| `ExtraCode/excel_version_01.py` | Excel 데이터를 읽어 평균/중앙값/최빈값을 단계별로 계산 |

## 실행 방법

```bash
python ExtraCode/create_sample_data.py    # 샘플 Excel 생성
python code_03_01_01.py
python code_03_01_02.py
python ExtraCode/excel_version_01.py
```

## 학습 포인트

- `ExtraCode/sample_data.xlsx`에는 의도적으로 매우 낮은 점수 2명(15점, 20점)을 포함시켰다.
- `ExtraCode/excel_version_01.py`를 실행하면 이상치가 **평균**을 얼마나 끌어내리는지,
  반면 **중앙값/최빈값**은 거의 영향을 받지 않는다는 점을 확인할 수 있다.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

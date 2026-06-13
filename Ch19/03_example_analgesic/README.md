# 19.3 예제로 이해: 진통제 효과 비교의 2×2 교차 설계

## 원본 코드

- `code_19_03_01.py` — 10명 피험자 2×2 교차 설계 가상 데이터 생성 (`np.random.seed(42)`, A=10/B=12, 기간2=-1, 개인차 N(0, 1.5²), 노이즈 N(0, 1))
- `code_19_03_02.py` — `smf.mixedlm`으로 혼합 효과 모형 적합
- `code_19_03_03.py` — 박스플롯 시각화

모두 책 본문(page 324314) 코드 그대로입니다.

## 샘플 데이터

`ExtraCode/sample_data.xlsx` 컬럼:

| 컬럼 | 의미 |
|---|---|
| Subject | 피험자 ID (1–10) |
| Period | 1차 / 2차 기간 |
| Sequence | 처리 순서 그룹 (`A->B` 또는 `B->A`) |
| Treatment | 해당 기간에 받은 처리 (A / B) |
| Score | 통증 완화 점수 (높을수록 좋음) |

총 20행 = 10명 × 2기간.

## Excel 활용 버전

`ExtraCode/excel_version.py`는 19장의 핵심 위험 요소까지 다룹니다.

1. 데이터 구조 점검 (피험자 수, 순서 그룹, 처리×기간 평균)
2. **혼합 효과 모형**으로 처리/기간 고정 효과 + 피험자 랜덤 효과 추정
3. **이월 효과 보수적 검토**: 기간 1 데이터만 사용한 두 순서 그룹의 독립 t-검정 → 혼합 모형 결과와 방향이 일치하는지 확인
4. **순서 그룹별 시계열 그림**: 이월 효과/순서 효과를 시각적으로 점검

## 실행

```bash
python code_19_03_01.py
python code_19_03_02.py
python code_19_03_03.py
python ExtraCode/excel_version.py
```

필요 패키지: `numpy`, `pandas`, `scipy`, `statsmodels`, `matplotlib`, `openpyxl`.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

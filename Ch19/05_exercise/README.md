# 19.5 연습 문제: UI A/B의 2×2 교차 설계 사용성 비교

## 원본 코드

- `code_19_05_01.py` — 12명 피험자 2×2 교차 설계 가상 데이터 생성 (`np.random.seed(101)`). UI B는 평균 15초 단축, 2차 기간은 학습 효과로 10초 단축, 개인차 N(0, 10²).

## 샘플 데이터

`ExtraCode/sample_data.xlsx` 컬럼:

| 컬럼 | 의미 |
|---|---|
| Subject | 피험자 ID (1–12) |
| Period | 1차 / 2차 기간 |
| Sequence | `A->B` 또는 `B->A` |
| Treatment | 해당 기간 UI (A / B) |
| Time | 과업 완료 시간 (초, 낮을수록 좋음) |

총 24행 = 12명 × 2기간.

## Excel 활용 버전

`ExtraCode/excel_version.py`는 연습 문제 5단계를 종합합니다.

1. 구조 점검: 피험자 수, 순서 그룹, Sequence×Period 평균
2. `smf.mixedlm`으로 혼합 효과 모형 적합
3. Treatment[T.B] 계수와 Period 계수를 추출해 \"UI B가 몇 초 단축\", \"학습 효과 몇 초\"로 자연어 출력
4. 순서 그룹별 평균 시간 라인 플롯 (이월 효과/순서 효과 시각 점검)
5. 종합 권고 메시지 자동 출력

## 실행

```bash
python code_19_05_01.py
python ExtraCode/excel_version.py
```

필요 패키지: `numpy`, `pandas`, `statsmodels`, `matplotlib`, `openpyxl`.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

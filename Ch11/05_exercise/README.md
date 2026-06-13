# 11.5 연습 문제 — 반도체 웨이퍼 공정 최적화

## 원본 코드

- `code_11_05_01.py`: 반도체 식각 공정의 3요인 2수준 × 반복 3회 가상 데이터 생성.

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

책의 데이터 생성 코드와 동일한 시드(`seed=42`)로 24행을 생성한다.

| 컬럼 | 설명 |
|---|---|
| Etching_Time | 15 / 30 초 |
| Plasma_Intensity | 200 / 300 W |
| Gas_Mixture_Ratio | 50 / 70 % |
| Replicate | 1, 2, 3 |
| Surface_Roughness | 표면 거칠기 (nm) — 낮을수록 좋음 |

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

1. 데이터 구조 확인
2. 주효과 + 2차 상호작용 회귀 모형 적합
3. ANOVA 테이블 출력, 유의 효과 (p<0.05) 자동 식별
4. 각 항의 기여율(%)
5. 효과 크기로부터 거칠기 최소화에 유리한 수준 추천
6. 실험점 중 평균 거칠기 최소 조건 출력
7. 잔차 진단 그림 (`ExtraCode/diagnostic.png`) 저장

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

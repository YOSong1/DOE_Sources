# 12.4 부분 요인 실험의 장단점 및 활용

## 원본 코드

- `code_12_04_01.py`: pyDOE2 로 Resolution III (2^(7-4)=8회), IV (2^(6-2)=16회), V (2^(5-1)=16회) 설계의 실험 횟수 비교.

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

2^(5-1) Resolution V 설계 16 runs. E = A·B·C·D 의 5차 상호작용으로 정의되므로 주효과·2차 상호작용 모두 교락 없이 추정 가능.

| 컬럼 | 설명 |
|---|---|
| A, B, C, D, E | 요인 (-1/+1) — E는 ABCD로 정의됨 |
| y | 가상 응답값 |

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

1. Generator E=ABCD 검증
2. 주효과만 포함한 ANOVA (16 obs / 6 params → 잔차 자유도 10 확보)
3. 2차 상호작용 효과 크기 별도 계산 (모두 추정 가능 — Resolution V의 장점)
4. 효과 크기·기여율 출력
5. 응답 최대화 최적 조건

> 주효과 + 모든 2차 상호작용을 한꺼번에 ANOVA로 넣으면 saturated (잔차 df=0) 가 되어 p-value를 산출할 수 없으므로, 주효과 ANOVA + 상호작용 효과 크기로 분리해 출력한다.

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

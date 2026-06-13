# 12.5 연습 문제 — 플라스틱 사출 성형 공정 스크리닝

## 원본 코드

- `code_12_05_01.py`: 6요인 2수준의 2^(6-2) Resolution IV 설계 (E=ABC, F=BCD) 데이터 생성.

## 샘플 데이터 (`ExtraCode/sample_data.xlsx`)

| 컬럼 | 설명 |
|---|---|
| A | 용융 온도 (코딩 -1/+1 → 220/250 °C) |
| B | 사출 압력 (80/120 bar) |
| C | 냉각 시간 (10/20 s) |
| D | 게이트 크기 (2/4 mm) |
| E | 사출 속도 — 생성식 E = ABC |
| F | 원료 수분 함량 — 생성식 F = BCD |
| Tensile_Strength | 인장 강도 (MPa) |

## Excel 활용 버전 (`ExtraCode/excel_version.py`)

1. Generator E=ABC, F=BCD 검증
2. 주효과 (|Effect|) 정렬 표
3. ANOVA 및 유의 요인 식별
4. 기여율 분석
5. 스크리닝 결과 — 핵심 요인 Top 3 자동 추출
6. 최대화 최적 조건과 예측 인장 강도
7. 파레토 차트 PNG 저장

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

# 2.4 조건부 확률

## 페이지 정보
- **책**: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
- **페이지 ID**: 326986
- **주제**: 조건부 확률, 독립 사건, 전확률의 법칙, 베이즈 정리

## 파일 구성

| 파일 | 내용 |
|------|------|
| `code_02_04_01.py` | 스팸/의료 진단 베이즈 수치 계산 및 100,000 시뮬레이션 검증 |
| `ExtraCode/sample_data.xlsx` | medical_test(5000명), spam_mail(5000개) |
| `ExtraCode/excel_version_01.py` | 데이터로 조건부 확률 정의 → 전확률 법칙 → 베이즈 정리를 단계별 분해 |

## 샘플 데이터
- **medical_test**: patient_id, has_disease(유병률 1%), test_positive(민감도 99% / 특이도 95%)
- **spam_mail**: mail_id, is_spam(30%), contains_discount(P(할인|스팸)=0.9, P(할인|일반)=0.2)

## 사용법

```bash
python code_02_04_01.py
python ExtraCode/excel_version_01.py
```

## 학습 포인트
- 베이즈 정리를 그냥 공식으로 외우는 대신, **(1)교집합 확률 → (2)조건부 확률 → (3)전확률의 법칙 → (4)베이즈** 4단계로 분해해 코드로 확인하면 의미가 또렷해집니다.
- 의료 진단 예제에서 "양성 판정자 중 실제 환자가 ~17%"라는 결과는 직관과 다르므로, 데이터로 직접 확인해보는 것이 매우 유효합니다.
- 동일한 분석 절차(스팸 vs 의료)를 통해 베이즈 정리의 범용성을 체감할 수 있습니다.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

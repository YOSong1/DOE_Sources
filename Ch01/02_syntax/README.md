# 1.2 Python 기본 문법

## 페이지 정보
- **책**: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
- **페이지 ID**: 324206
- **주제**: 변수, 자료형, 자료구조, 제어문, 함수, 평균/분산 실습

## 파일 구성

| 파일 | 내용 |
|------|------|
| `code_01_02_01.py` | 변수와 자료형 (int/float/str/bool) |
| `code_01_02_02.py` | 형변환 함수 |
| `code_01_02_03.py` | 리스트 인덱싱/슬라이싱/메서드 |
| `code_01_02_04.py` | 딕셔너리 사용 |
| `code_01_02_05.py` | 튜플 (불변 시퀀스) |
| `code_01_02_06.py` | for 루프 + 리스트 컴프리헨션 |
| `code_01_02_07.py` | while 루프 |
| `code_01_02_08.py` | if/elif/else 등급 판정 |
| `code_01_02_09.py` | 함수와 lambda |
| `code_01_02_10.py` | 실습: 평균/분산 직접 계산 vs NumPy |
| `ExtraCode/sample_data.xlsx` | 학생 10명의 점수, 전공 데이터 (students 시트) |
| `ExtraCode/excel_version_01.py` | Excel 데이터를 읽어 자료형 확인 → 리스트 변환 → 등급 부여 → 평균/분산 계산 |

## 샘플 데이터
- **students 시트**: student_id, name, score(0~10), subject — 책 원본의 `[4,8,6,5,3,2,8,9,2,5]`를 학생 데이터로 재구성

## 사용법

```bash
# 원본 코드 실행 (각각)
python code_01_02_10.py

# Excel 활용 버전 — 한 단계 더 깊이 사고하기
python ExtraCode/excel_version_01.py
```

## 학습 포인트
- 책의 단순 리스트를 실제 Excel 시트로 옮기면 "데이터 ↔ 코드"의 관계를 더 명확히 이해할 수 있습니다.
- 평균/분산을 직접 구현해보면 NumPy 함수 내부가 어떻게 동작하는지 알 수 있습니다.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

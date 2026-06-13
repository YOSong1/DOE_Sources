# 1.5 시각화

## 페이지 정보
- **책**: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
- **페이지 ID**: 324260
- **주제**: Matplotlib/Seaborn 기초, 히스토그램·막대·산점도·박스 플롯

## 파일 구성

| 파일 | 내용 |
|------|------|
| `code_01_05_01.py` | 한글 폰트 설정 |
| `code_01_05_02.py` | 히스토그램 (정규분포 100명 점수) |
| `code_01_05_03.py` | 히스토그램 + KDE |
| `code_01_05_04.py` | 막대 그래프 (학과별 평균) |
| `code_01_05_05.py` | 산점도 + 추세선 (공부시간 vs 점수) |
| `code_01_05_06.py` | 박스 플롯 (학과별 분포) |
| `code_01_05_07.py` | subplots로 4종 그래프 배치 |
| `code_01_05_08.py` | Seaborn 통합 (histplot/boxplot/scatterplot) |
| `ExtraCode/sample_data.xlsx` | monthly_sales, dept_scores, study_vs_score 시트 |
| `ExtraCode/excel_version_01.py` | Excel 3개 시트로 4종 그래프 통합 + 추세선 식 표시 |

## 샘플 데이터
- **monthly_sales**: 12개월 매출 (사인파 + 노이즈)
- **dept_scores**: 3개 학과 90명 점수
- **study_vs_score**: 20명의 공부시간/시험점수

## 사용법

```bash
python code_01_05_07.py             # 책 원본 4종 그래프
python ExtraCode/excel_version_01.py        # 실제 Excel 데이터로 그래프 + 통계 출력
```

실행 시 `excel_4grid.png` 이미지가 같은 폴더에 저장됩니다.

## 학습 포인트
- 한글 폰트 설정(`plt.rcParams['font.family'] = 'Malgun Gothic'`)을 코드 상단에 두는 습관이 중요합니다.
- 산점도에 추세선과 상관계수를 함께 표시하면 시각화와 정량 분석을 한 화면에서 볼 수 있습니다.
- 박스 플롯 + groupby는 ANOVA 등 그룹 비교 분석의 첫 단계입니다.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

# Sources — 책 코드 + Excel 활용 버전

**대상 책**: Python으로 배우는 확률통계와 실험계획법 — 분석부터 LLM 활용까지
**WikiDocs**: https://wikidocs.net/book/1914

## 폴더 구조

```
Sources/
├── Chapter_00_intro/              00. 들어가기
├── Chapter_01_python/             01. Python 기초 (5절)
├── Chapter_02_probability/        02. 확률 기초 (4절)
├── Chapter_03_statistics/         03. 통계 기초 (4절)
├── Chapter_04_random_variable/    04. 확률 변수 (2절)
├── Chapter_05_discrete_dist/      05. 이산형 확률 분포 (8절)
├── Chapter_06_continuous_dist/    06. 연속형 확률 분포 (8절)
├── Chapter_07_hypothesis_test/    07. 가설 검정 (5절)
├── Chapter_08_regression/         08. 회귀 분석 (3절)
├── Chapter_09_anova/              09. 분산 분석 (4절)
├── Chapter_10_correlation/        10. 상관 분석 (4절, 개요 제외)
├── Chapter_11_full_factorial/     11. 완전 요인 실험
├── Chapter_12_fractional_factorial/ 12. 부분 요인 실험
├── Chapter_13_response_surface/   13. 응답 표면 방법론
├── Chapter_14_taguchi/            14. 다구찌 방법
├── Chapter_15_block_design/       15. 블록 설계
├── Chapter_16_box_behnken/        16. Box-Behnken 설계
├── Chapter_17_crd/                17. 완전 무작위 설계
├── Chapter_18_replication/        18. 반복 실험
├── Chapter_19_crossover/          19. 교차 설계
├── Chapter_20_genai/              20. 생성형 AI를 활용한 분석
```

## 각 페이지 폴더 구성

코드 블록이 있는 페이지는 다음 구조로 정리되어 있습니다.

```
NN_topic/
├── code_<chapter>_<section>_<NN>.py   # 책 본문 코드 (먼저 실행)
├── README.md                          # 학습 포인트와 실행 가이드
└── ExtraCode/                         # 추가 연습 — 책 본문 학습 후 진행
    ├── sample_data.xlsx       (또는 sample_*.xlsx)
    ├── create_sample_data.py  / make_sample.py  (있는 경우)
    └── excel_version*.py      # Excel을 읽어 한 단계 더 사고를 유도하는 분석
```

- **`code_<chapter>_<section>_<NN>.py`** — WikiDocs 책 본문의 ```python``` 코드를 그대로 추출 (각 블록 1개당 파일 1개).
  파일명은 `code_<챕터>_<단락>_<코드순서>.py` 규칙(예: `code_11_03_02.py` = 11장 3절의 두 번째 코드 블록)을 따르며,
  각 파일 최상단에는 동일한 파일명이 `# code_XX_YY_NN.py` 주석으로 적혀 있어 책 본문 코드 블록과 1:1로 매핑됩니다.
- **`ExtraCode/sample_data.xlsx`** — 해당 페이지 주제에 맞는 의미 있는 샘플 데이터
- **`ExtraCode/excel_version*.py`** — Excel을 읽어 동일 분석을 수행하되, 수식의 각 항을 명시적으로 계산하여 의미를 드러내는 버전
- **`README.md`** — 페이지별 학습 포인트와 실행 가이드

**진행 순서**: 먼저 `code_*.py`를 실행해 책 본문 코드를 이해한 뒤, `ExtraCode/` 안의 추가 연습으로 넘어갑니다.

코드 블록이 없는 페이지(개요/장단점/연습 문제 등)는 폴더가 생성되지 않거나 README만 있습니다.


## Excel 버전의 설계 의도

원본 코드는 보통 `np.random.normal(...)` 등으로 데이터를 그 자리에서 생성한 뒤 분석합니다. Excel 버전은 다음과 같이 한 단계 더 사고를 유도합니다.

1. **외부 데이터를 읽어** (`pd.read_excel(...)`) 분석에 투입
2. **수식의 각 항을 명시적으로 계산** 후 출력 (예: 편차제곱합, 카이제곱 셀 기여도, Fisher Z 변환 등)
3. **결과의 의미를 print 메시지로 설명** (이상치가 평균에 미치는 영향, 효과 크기 해석 등)
4. **보강 분석 추가** (Cohen's d, Cramer's V, η², 95% CI, VIF, 잔차 진단 등)

## 실행 환경

- Python 3.10+
- 주요 패키지: numpy, pandas, scipy, matplotlib, seaborn, statsmodels, scikit-learn, pyDOE2, openpyxl
- Chapter 9/10 일부 페이지: `pingouin` 추가 필요
- Chapter 20: `pyDOE3`, `openai`, `anthropic` 추가 필요 (API 키가 없어도 mock 응답으로 실행 가능)
- 모든 Python 파일은 UTF-8 인코딩. Windows cp949 콘솔 호환을 위해 `sys.stdout.reconfigure(encoding='utf-8')` 가드 포함
- matplotlib 한글 폰트: `plt.rcParams['font.family'] = 'Malgun Gothic'`



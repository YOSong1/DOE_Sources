# 17.3 예제로 이해: 비료 종류에 따른 식물 성장률 비교

## 원본 코드

- `code_17_03_01.py` — `np.random.seed(42)` 기반 가상 데이터 생성 (비료 A/B/C × 10반복)
- `code_17_03_02.py` — `scipy.stats.f_oneway`로 일원분산분석 수행
- `code_17_03_03.py` — 박스플롯 시각화

세 파일 모두 책 본문(page 324553) 코드 블록 원본입니다.

## 샘플 데이터

`ExtraCode/sample_data.xlsx`는 두 시트로 구성됩니다.

- `tidy` — `Fertilizer`(범주), `Growth_cm`(반응) 두 컬럼의 long format (30행)
- `wide` — `Fertilizer_A/B/C` 세 컬럼의 wide format (10행)

원본 코드가 매번 시드를 다시 돌리는 대신, 미리 생성된 데이터를 그대로 활용할 수 있습니다.

## Excel 활용 버전

`ExtraCode/excel_version.py`는 단순 ANOVA 호출에 그치지 않고:

1. tidy 시트 로드 후 행수/처리 수 점검
2. `groupby().describe()`로 그룹별 평균·표준편차·범위 출력
3. `f_oneway`로 F, p-value 계산
4. **η² (효과 크기)** 를 SSA/SST로 직접 계산하여 유의성과 효과 크기를 분리해 해석
5. 박스플롯 시각화

## 실행

```bash
python code_17_03_01.py
python code_17_03_02.py
python code_17_03_03.py
python ExtraCode/excel_version.py
```

필요 패키지: `numpy`, `pandas`, `scipy`, `matplotlib`, `openpyxl`.


<!-- extracode-note -->
## 추가 연습 코드 (`ExtraCode/`)

`ExtraCode/` 폴더에는 책 본문 코드를 익힌 뒤 진행할 수 있는 **Excel 샘플 데이터 기반 추가 연습**이 들어 있습니다. 샘플 데이터 생성 스크립트(`create_sample_data.py` / `make_sample.py`), 엑셀 파일, `excel_version*.py`가 함께 포함됩니다.

```bash
cd ExtraCode
# (필요 시) python create_sample_data.py  또는  python make_sample.py
python excel_version.py            # 또는 excel_version_01.py
```

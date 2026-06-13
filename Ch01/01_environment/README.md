# 1.1 실습 환경

## 페이지 정보
- **책**: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
- **페이지 ID**: 324205
- **주제**: VS Code / Google Colab 실습 환경 구축

## 파일 구성

| 파일 | 내용 |
|------|------|
| `original_01.py` | Hello, Statistics! 첫 코드 실행 |
| `original_02.py` | 가상환경 venv 생성 명령 (참조용 주석) |
| `original_03.py` | 주요 라이브러리(NumPy/Pandas/SciPy/Matplotlib) 버전 출력 |

## 사용법

```bash
# 라이브러리 설치 (한 번만)
pip install numpy pandas scipy matplotlib seaborn openpyxl

# 환경 검증
python original_03.py
```

## 샘플 데이터 (Excel)

이 페이지는 **환경 설정에 관한 내용**이므로 Excel 샘플 데이터가 필요하지 않습니다.
실제 분석 코드는 1.2절 이후의 폴더에 존재합니다.

## 학습 포인트
- VS Code는 로컬에 직접 환경을 구축할 때 사용합니다.
- Colab은 별도 설치 없이 브라우저만으로 즉시 실습할 수 있습니다.
- 환경 검증을 위해 라이브러리 버전을 한 번 출력해보는 습관을 들이면 좋습니다.

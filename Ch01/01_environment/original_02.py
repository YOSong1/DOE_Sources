import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.1 실습 환경 - 가상환경(venv) 생성 명령
# =============================================================================
# 책: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
# 페이지: 324205 - 1.1 실습 환경
# 설명: 본 파일은 실제 실행용이 아닌 터미널 명령 모음입니다.
# =============================================================================

# 터미널에서 실행
# python -m venv .venv

# Windows
# .venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate

# 가상환경 활성화 후 다음 명령으로 라이브러리 설치
# pip install numpy pandas scipy matplotlib seaborn

print("이 파일은 터미널 명령 참조용입니다. 위 주석을 셸에서 실행하세요.")

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# =============================================================================
# 1.5 시각화 - Excel 활용 버전: 실제 데이터로 4종 그래프 통합
# =============================================================================
# 책: Python으로 배우는 확률통계와 실험계획법 (book_id 1914)
# 페이지: 324260 - 1.5 시각화
#
# sample_data.xlsx의 세 시트를 사용:
#   - monthly_sales: 월별 매출 → 막대 그래프 (1.5.3)
#   - dept_scores: 학과별 점수 → 박스 플롯 (1.5.5)
#   - study_vs_score: 공부시간 vs 점수 → 산점도 (1.5.4)
# 추가로 히스토그램(1.5.2)을 dept_scores 전체에 적용.
# =============================================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

BASE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(BASE, "sample_data.xlsx")

# -----------------------------------------------------------------------------
# 1) Excel 읽기
# -----------------------------------------------------------------------------
sales = pd.read_excel(XLSX, sheet_name="monthly_sales")
dept = pd.read_excel(XLSX, sheet_name="dept_scores")
study = pd.read_excel(XLSX, sheet_name="study_vs_score")

print("=== monthly_sales ===")
print(sales)
print(f"\n매출 평균: {sales['sales_million_krw'].mean():.2f}백만원")
print(f"최고 매출 월: "
      f"{sales.loc[sales['sales_million_krw'].idxmax(), 'month']}")

print("\n=== dept_scores 요약 ===")
print(dept.groupby("department")["score"].describe().round(2))

print("\n=== study_vs_score 상관계수 ===")
corr = study[["study_hours", "exam_score"]].corr().iloc[0, 1]
print(f"공부 시간 vs 시험 점수 상관계수: {corr:.4f}")

# -----------------------------------------------------------------------------
# 2) 2x2 서브플롯에 4종 그래프 통합 — 1.5.6
# -----------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("Excel 데이터로 그린 4종 그래프", fontsize=14)

# (0,0) 히스토그램 + KDE (전체 점수)
all_scores = dept["score"].values
axes[0, 0].hist(all_scores, bins=15, density=True,
                color='steelblue', edgecolor='white', alpha=0.6)
# KDE
try:
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(all_scores)
    x = np.linspace(all_scores.min(), all_scores.max(), 200)
    axes[0, 0].plot(x, kde(x), color='tomato', linewidth=2, label='KDE')
    axes[0, 0].legend()
except ImportError:
    pass
axes[0, 0].set_title("히스토그램 — 전체 점수 분포")
axes[0, 0].set_xlabel("점수")
axes[0, 0].set_ylabel("밀도")

# (0,1) 막대 그래프 — 월별 매출
axes[0, 1].bar(sales["month"], sales["sales_million_krw"],
               color="seagreen", edgecolor="white")
axes[0, 1].set_title("막대 그래프 — 월별 매출")
axes[0, 1].set_ylabel("매출 (백만원)")
axes[0, 1].tick_params(axis='x', rotation=45)

# (1,0) 산점도 + 추세선 — 공부시간 vs 점수
axes[1, 0].scatter(study["study_hours"], study["exam_score"],
                   color="steelblue", s=70, alpha=0.8)
z = np.polyfit(study["study_hours"], study["exam_score"], 1)
p = np.poly1d(z)
xs = np.linspace(study["study_hours"].min(),
                 study["study_hours"].max(), 100)
axes[1, 0].plot(xs, p(xs), color="tomato", linestyle="--",
                label=f"y = {z[0]:.2f}x + {z[1]:.2f}")
axes[1, 0].set_title(f"산점도 — 공부 시간 vs 점수 (r={corr:.3f})")
axes[1, 0].set_xlabel("공부 시간 (시간)")
axes[1, 0].set_ylabel("시험 점수")
axes[1, 0].legend()

# (1,1) 박스 플롯 — 학과별 점수
groups = [g["score"].values for _, g in dept.groupby("department")]
labels = list(dept.groupby("department").groups.keys())
axes[1, 1].boxplot(groups, tick_labels=labels, patch_artist=True,
                   boxprops=dict(facecolor='steelblue', alpha=0.6))
axes[1, 1].set_title("박스 플롯 — 학과별 점수")
axes[1, 1].set_ylabel("점수")

plt.tight_layout()

# 결과 이미지 저장
out_png = os.path.join(BASE, "excel_4grid.png")
plt.savefig(out_png, dpi=120)
print(f"\n그래프 저장: {out_png}")
plt.show()

print("\n[해석] 같은 4종 그래프를 책의 가상 데이터가 아니라\n"
      "        실제 Excel 데이터에 적용하여, 자료 변환→시각화 흐름을 익혔습니다.")

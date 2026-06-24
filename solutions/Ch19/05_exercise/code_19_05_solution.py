# code_19_05_solution.py
"""19.5 연습 문제 해답: 두 가지 UI(A/B)의 사용성 비교 (2x2 교차 설계).

자기완결형 해답 코드입니다. 외부 xlsx 파일에 의존하지 않고,
문제에서 제시한 데이터 생성 코드(seed=101)를 그대로 포함합니다.

수행 과제
  1) 가상 데이터 생성 (2x2 교차 설계, 12명 / 6명씩 2개 순서 그룹)
  2) 'Subject','Period','Sequence','Treatment','Time' 데이터프레임 구성 및 점검
  3) statsmodels 혼합 효과 모형(mixedlm): 고정효과 Treatment+Period, 랜덤효과 Subject
     - 이월(carryover) 효과 검정도 보조 모형으로 추가
  4) 유의효과(alpha=0.05) 식별
  5) 시각화: 순서 그룹별 시계열, 처리/시기 효과, 잔차 진단
  6) 종합 결론 및 최적 처리(UI) 도출

라이브러리: matplotlib만 사용(seaborn 미사용). 한글 폰트 Malgun Gothic.
그림은 같은 폴더에 PNG로 저장합니다.
"""

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

plt.rc("font", family="Malgun Gothic")
plt.rc("axes", unicode_minus=False)

ALPHA = 0.05
OUT_DIR = Path(__file__).resolve().parent


# ============================================================
# [1단계] 가상 데이터 생성 (문제 제공 코드 동일: seed=101)
# ============================================================
def generate_data():
    np.random.seed(101)  # 결과 재현성을 위한 시드
    n_subjects = 12
    subjects_ui = np.repeat(np.arange(1, n_subjects + 1), 2)
    periods_ui = np.tile([1, 2], n_subjects)

    treatments_ui = []
    sequences_ui = []
    # 그룹 1 (A -> B), 피험자 1~6
    for _ in range(n_subjects // 2):
        treatments_ui.extend(["A", "B"])
        sequences_ui.extend(["A->B", "A->B"])
    # 그룹 2 (B -> A), 피험자 7~12
    for _ in range(n_subjects // 2):
        treatments_ui.extend(["B", "A"])
        sequences_ui.extend(["B->A", "B->A"])

    df = pd.DataFrame({
        "Subject": subjects_ui,
        "Period": periods_ui,
        "Sequence": sequences_ui,
        "Treatment": treatments_ui,
    })

    base_time = 120  # 기본 과업 완료 시간 (초)
    treatment_effects_ui = {"A": 0, "B": -15}   # UI B가 A보다 15초 빠름
    period_effects_ui = {1: 0, 2: -10}          # 2차에 학습 효과로 10초 단축
    subject_random_effects_ui = np.repeat(
        np.random.normal(0, 10, n_subjects), 2)  # 개인별 숙련도 차이
    noise_ui = np.random.normal(0, 5, n_subjects * 2)  # 순수 오차

    df["Time"] = (base_time
                  + df["Treatment"].map(treatment_effects_ui)
                  + df["Period"].map(period_effects_ui)
                  + subject_random_effects_ui + noise_ui)
    df["Time"] = df["Time"].round(1)
    return df


# ============================================================
# [2단계] 데이터 구조 점검
# ============================================================
def inspect_data(df):
    print("=" * 64)
    print("[Step 0] 데이터 구조 점검")
    print("=" * 64)
    print(df.head(8).to_string(index=False))
    print(f"\n총 관측치: {len(df)}행, 피험자 수: {df['Subject'].nunique()}명")
    print(f"순서 그룹: {sorted(df['Sequence'].unique())}")
    print(f"처리(UI) 수준: {sorted(df['Treatment'].unique())}, "
          f"기간: {sorted(df['Period'].unique())}")
    print("\n[처리별 평균 시간]")
    print(df.groupby("Treatment")["Time"].mean().round(2).to_string())
    print("\n[Sequence x Period 평균 시간]")
    print(df.groupby(["Sequence", "Period"])["Time"].mean().round(2).to_string())


# ============================================================
# [3단계] 혼합 효과 모형 적합 및 분석
# ============================================================
def fit_models(df):
    print("\n" + "=" * 64)
    print("[Step 1] 혼합 효과 모형 (고정: Treatment+Period / 랜덤: Subject)")
    print("=" * 64)
    # 주 모형: 처리 + 시기 고정효과, 피험자 랜덤효과
    model = smf.mixedlm("Time ~ Treatment + Period",
                        data=df, groups=df["Subject"])
    result = model.fit()
    print(result.summary())

    # 보조 모형: 이월(carryover) 효과 점검
    # 2x2 교차에서 이월효과는 Sequence(순서 그룹) 간 차이로 나타남.
    # Subject가 Sequence에 완전히 내포되므로, 순서 그룹 평균 차이를
    # 피험자 평균(개체당 두 기간 합) 수준에서 t검정으로 점검한다.
    print("\n" + "=" * 64)
    print("[Step 1-b] 이월(Carryover) 효과 점검 - 순서 그룹 간 피험자 총합 비교")
    print("=" * 64)
    subj_tot = df.groupby(["Sequence", "Subject"])["Time"].sum().reset_index()
    g1 = subj_tot.loc[subj_tot["Sequence"] == "A->B", "Time"]
    g2 = subj_tot.loc[subj_tot["Sequence"] == "B->A", "Time"]
    from scipy import stats
    t_stat, p_carry = stats.ttest_ind(g1, g2, equal_var=True)
    print(f"  A->B 그룹 피험자 총합 평균: {g1.mean():.2f}")
    print(f"  B->A 그룹 피험자 총합 평균: {g2.mean():.2f}")
    print(f"  t = {t_stat:.3f}, p = {p_carry:.4f}")
    if p_carry < ALPHA:
        print("  -> 순서 그룹 간 차이 유의: 이월(잔류) 효과 가능성 있음.")
    else:
        print("  -> 순서 그룹 간 차이 유의하지 않음: 이월 효과 근거 약함.")

    return result, p_carry


def summarize_effects(result, p_carry):
    print("\n" + "=" * 64)
    print("[Step 2] 핵심 효과 요약 및 유의성 판정 (alpha=0.05)")
    print("=" * 64)
    effects = {}
    for label, key in [("처리 효과 Treatment[T.B]", "Treatment[T.B]"),
                       ("시기 효과 Period", "Period")]:
        if key in result.params.index:
            coef = result.params[key]
            pval = result.pvalues[key]
            sig = "유의함" if pval < ALPHA else "유의하지 않음"
            direction = "단축" if coef < 0 else "증가"
            print(f"  {label}: 계수={coef:+.2f}초, p={pval:.4f} -> {sig} "
                  f"(시간 {abs(coef):.2f}초 {direction})")
            effects[key] = (coef, pval, pval < ALPHA)

    carry_sig = "유의함" if p_carry < ALPHA else "유의하지 않음"
    print(f"  이월 효과(Carryover): p={p_carry:.4f} -> {carry_sig}")

    print("\n  [유의효과(0.05) 식별]")
    sig_list = [name for name, (_, _, s) in effects.items() if s]
    if p_carry < ALPHA:
        sig_list.append("Carryover")
    print(f"  유의한 효과: {sig_list if sig_list else '없음'}")
    return effects


# ============================================================
# [4단계] 시각화
# ============================================================
def plot_sequence_lines(df):
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = {"A->B": "tab:blue", "B->A": "tab:red"}
    for seq, g in df.groupby("Sequence"):
        m = g.groupby("Period")["Time"].mean()
        ax.plot(m.index, m.values, marker="o", linewidth=2,
                color=colors.get(seq), label=seq)
        for x, y in zip(m.index, m.values):
            ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points",
                        xytext=(0, 8), ha="center", fontsize=9)
    ax.set_xticks([1, 2])
    ax.set_xlabel("Period (기간)")
    ax.set_ylabel("평균 과업 완료 시간 (초)")
    ax.set_title("순서 그룹별 시계열 - 2x2 UI 교차 설계")
    ax.legend(title="Sequence")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    path = OUT_DIR / "code_19_05_solution_sequence_lines.png"
    plt.savefig(path, dpi=120)
    plt.close(fig)
    print(f"\n[그림 저장] {path.name}")


def plot_main_effects(df):
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    # 처리(UI) 효과 박스플롯
    treat_levels = sorted(df["Treatment"].unique())
    data_t = [df.loc[df["Treatment"] == t, "Time"] for t in treat_levels]
    axes[0].boxplot(data_t, labels=[f"UI {t}" for t in treat_levels])
    means_t = [d.mean() for d in data_t]
    axes[0].plot(range(1, len(treat_levels) + 1), means_t,
                 "D-", color="tab:green", label="평균")
    axes[0].set_title("처리(UI) 효과")
    axes[0].set_ylabel("과업 완료 시간 (초)")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 시기(Period) 효과 박스플롯
    per_levels = sorted(df["Period"].unique())
    data_p = [df.loc[df["Period"] == p, "Time"] for p in per_levels]
    axes[1].boxplot(data_p, labels=[f"{p}차" for p in per_levels])
    means_p = [d.mean() for d in data_p]
    axes[1].plot(range(1, len(per_levels) + 1), means_p,
                 "D-", color="tab:orange", label="평균")
    axes[1].set_title("시기(Period) 효과")
    axes[1].set_ylabel("과업 완료 시간 (초)")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    path = OUT_DIR / "code_19_05_solution_main_effects.png"
    plt.savefig(path, dpi=120)
    plt.close(fig)
    print(f"[그림 저장] {path.name}")


def plot_residual_diagnostics(df, result):
    resid = result.resid
    fitted = result.fittedvalues

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    # 잔차 vs 적합치
    axes[0].scatter(fitted, resid, color="tab:blue", alpha=0.7)
    axes[0].axhline(0, color="red", linestyle="--", linewidth=1)
    axes[0].set_xlabel("적합치 (Fitted)")
    axes[0].set_ylabel("잔차 (Residual)")
    axes[0].set_title("잔차 vs 적합치")
    axes[0].grid(True, alpha=0.3)

    # Q-Q plot (정규성)
    from scipy import stats
    stats.probplot(resid, dist="norm", plot=axes[1])
    axes[1].set_title("잔차 Q-Q Plot (정규성)")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    path = OUT_DIR / "code_19_05_solution_residuals.png"
    plt.savefig(path, dpi=120)
    plt.close(fig)
    print(f"[그림 저장] {path.name}")


# ============================================================
# [5단계] 종합 결론 및 최적 처리 도출
# ============================================================
def conclude(df, effects, p_carry):
    print("\n" + "=" * 64)
    print("[Step 3] 종합 결론 및 최적 처리(UI) 제안")
    print("=" * 64)

    treat_means = df.groupby("Treatment")["Time"].mean()
    best_ui = treat_means.idxmin()  # 시간이 짧을수록 좋음
    print(f"  처리별 평균 시간: "
          + ", ".join(f"UI {k}={v:.2f}초" for k, v in treat_means.items()))
    print(f"  관측상 최단 시간 UI: {best_ui}")

    t_sig = effects.get("Treatment[T.B]", (0, 1, False))[2]
    p_sig = effects.get("Period", (0, 1, False))[2]

    print("\n  [해석]")
    if t_sig:
        coef = effects["Treatment[T.B]"][0]
        if coef < 0:
            print("  - 처리 효과 유의: UI B가 UI A보다 통계적으로 유의하게 빠름.")
        else:
            print("  - 처리 효과 유의: UI B가 UI A보다 통계적으로 유의하게 느림.")
    else:
        print("  - 처리 효과는 유의수준 0.05에서 유의하지 않음.")
    if p_sig:
        print("  - 시기 효과 유의: 2차 기간에서 학습 효과(시간 단축)가 관찰됨.")
    else:
        print("  - 시기 효과는 유의하지 않음.")
    if p_carry < ALPHA:
        print("  - 이월 효과 가능성 있음: 결과 해석 시 주의 필요(워시아웃 기간 점검).")
    else:
        print("  - 이월 효과 근거 약함: 교차 설계 가정이 대체로 충족됨.")

    print("\n  [최종 제안]")
    if t_sig and effects["Treatment[T.B]"][0] < 0:
        print(f"  => UI B 채택 권장. 시기/개인차를 통제한 뒤에도 "
              f"UI B가 과업 완료를 유의하게 단축함.")
    elif t_sig and effects["Treatment[T.B]"][0] > 0:
        print("  => UI A 채택 권장. UI B는 오히려 시간이 더 걸림.")
    else:
        print(f"  => 통계적으로 명확한 차이는 없으나 평균상 UI {best_ui}가 우수. "
              "추가 표본 확보를 권장.")


def main():
    df = generate_data()
    inspect_data(df)
    result, p_carry = fit_models(df)
    effects = summarize_effects(result, p_carry)

    plot_sequence_lines(df)
    plot_main_effects(df)
    plot_residual_diagnostics(df, result)

    conclude(df, effects, p_carry)
    print("\n[완료] 모든 분석과 그림 저장이 끝났습니다.")


if __name__ == "__main__":
    main()

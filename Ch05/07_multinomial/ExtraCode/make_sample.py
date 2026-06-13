import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
# 5.7 다항 — 객관식 5지선다 설문조사 500명 응답
# 카테고리 (A,B,C,D,E) 실제 분포가 다를 때 응답 분포 시뮬레이션
import pandas as pd
import numpy as np

np.random.seed(101)
N = 500
choices = ["A", "B", "C", "D", "E"]
true_p = np.array([0.10, 0.20, 0.35, 0.25, 0.10])  # 합=1

answers = np.random.choice(choices, size=N, p=true_p)

df = pd.DataFrame({
    "respondent_id": np.arange(1, N+1),
    "answer": answers,
})

# 빈도 시트도 함께
counts = df["answer"].value_counts().reindex(choices).fillna(0).astype(int)
freq = pd.DataFrame({"choice": choices, "observed": counts.values})

with pd.ExcelWriter("sample_data.xlsx", engine="openpyxl") as w:
    df.to_excel(w, sheet_name="responses", index=False)
    freq.to_excel(w, sheet_name="frequency", index=False)

print(f"Saved. N={N}, observed = {dict(zip(choices, counts.values))}")

# Chapter 17.2 Excel 활용 버전
# sample_data.xlsx의 UnitID 컬럼을 읽어 시드 고정 무작위 배정을 수행하고
# 결과 배정표를 동일한 Excel 파일에 새 시트로 추가합니다.
# 무작위화 절차의 재현성(seed)과 문서화(시트 저장)를 함께 보여 줍니다.

from pathlib import Path
import random
import pandas as pd

xlsx = Path(__file__).with_name("sample_data.xlsx")
df = pd.read_excel(xlsx, sheet_name=0)

print("=" * 60)
print("[Step 0] 실험 단위 풀")
print("=" * 60)
print(df.head())
print(f"총 실험 단위: {len(df)}")

# 시드 고정 → 재현 가능한 무작위 배정
SEED = 2026
rng = random.Random(SEED)
units = df["UnitID"].tolist()
rng.shuffle(units)

groups = {"A": units[:10], "B": units[10:20], "C": units[20:30]}
assign_df = pd.DataFrame(
    [(u, g) for g, ids in groups.items() for u in ids],
    columns=["UnitID", "Treatment"]
).sort_values("UnitID").reset_index(drop=True)

print("\n[Step 1] 무작위 배정 결과 (시드={})".format(SEED))
for g, ids in groups.items():
    print(f"  처리 {g}: {sorted(ids)}")

# 분석 흐름에 활용할 수 있도록 결과 시트를 저장
with pd.ExcelWriter(xlsx, engine="openpyxl",
                    mode="a", if_sheet_exists="replace") as w:
    assign_df.to_excel(w, sheet_name="assignment", index=False)

print("\n[해석 메시지] 시드와 배정표를 함께 보관하면 나중에 동일한 ")
print("              무작위화 결과를 재현할 수 있어 실험 감사(audit)에 유리합니다.")

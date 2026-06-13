# code_20_08_01.py
# Chapter 20.08 코드 1: 4요인 2수준 설계 매트릭스 (page 329247)

from pyDOE3 import ff2n
import pandas as pd

design = ff2n(4)
df_design = pd.DataFrame(
    design,
    columns=["Temperature", "Pressure", "CoolingTime", "InjectionSpeed"]
)

print(df_design)

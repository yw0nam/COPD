# %%
import pandas as pd
import numpy as np
import datatable 

# %%
sm_df_1 = datatable.fread('/mnt/hdd/spow12/work/COPD/data/03_SCREENDATA_SM_01.csv').to_pandas()
sm_df_2 = datatable.fread('/mnt/hdd/spow12/work/COPD/data/03_SCREENDATA_SM_02.csv').to_pandas()
df = pd.concat([sm_df_1, sm_df_2])
df = df.reset_index(drop=True)
# %%
print(len(df))
# %%
df = df[df['RSLT_GRP'] != '']
df = df.dropna(subset=['RSLT_GRP'])
# %%
print(len(df))
# %%
temp = pd.DataFrame(df['CDW_ID'].value_counts() >= 2)
valid_list = temp[temp.CDW_ID].index
df = df.query("CDW_ID in @valid_list")
print(len(df))
# %%
df.sort_values(['CDW_ID','SM_DATE_N'], ascending=[True, True])
# %%

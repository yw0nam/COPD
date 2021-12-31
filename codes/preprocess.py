# %%
import pandas as pd
import numpy as np
import datatable 
from tqdm import tqdm
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
df = df.sort_values(['CDW_ID','SM_DATE_N'], ascending=[True, True])
df = df.reset_index(drop=True)
# %%
prev_id = df['CDW_ID'].iloc[0]
prev_date = df['SM_DATE_N'].iloc[0]
row_to_remove = []
for i in tqdm(range(1, len(df))):
    if prev_id != df['CDW_ID'].iloc[i]:
        pass
    elif prev_date == df['SM_DATE_N'].iloc[i]:
        row_to_remove.append(i)
    prev_id = df['CDW_ID'].iloc[i]
    prev_date = df['SM_DATE_N'].iloc[i]
# %%
df = df.drop(index=row_to_remove)
df = df.reset_index(drop=True)
# %%
print(len(df))
# %%
temp = pd.DataFrame(df['CDW_ID'].value_counts() >= 2)
valid_list = temp[temp.CDW_ID].index
df = df.query("CDW_ID in @valid_list")
print(len(df))
df = df.reset_index(drop=True)

# %%
res = []
for id in tqdm(valid_list):
    temp = df.query('CDW_ID == @id')
    date = '|'.join(temp['SM_DATE_N'].to_list())
    result = '|'.join(temp['RSLT_GRP'].to_list())
    res.append({'CDW_ID':id, 
                'SM_DATE_N': date,
                'RSLT_GRP': result})
# %%
data = pd.DataFrame(res)
# %%
data.to_csv('/mnt/hdd/spow12/work/COPD/data/data.in_oneline.csv', index=False)
# %%

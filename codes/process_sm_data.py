# %%
import pandas as pd
import numpy as np
import datatable 
from tqdm import tqdm
# %%
sm_df_1 = datatable.fread('/mnt/hdd/spow12/work/COPD/data/03_SCREENDATA_SM_01.csv').to_pandas()
sm_df_2 = datatable.fread('/mnt/hdd/spow12/work/COPD/data/03_SCREENDATA_SM_02.csv').to_pandas()
sm_df = pd.concat([sm_df_1, sm_df_2])
sm_df = sm_df.reset_index(drop=True)
df = sm_df[['CDW_ID', 'SM_DATE_N', 'GEND_CD', 'AGE', 'RSLT_GRP', 'SEVERITY']]
df['SEVERITY'] = df[df['SEVERITY'] != ""]['SEVERITY'].map(lambda x: x[2:])
df['SM'] = 'Y'
# %%
ex_df = pd.read_csv('/mnt/hdd/spow12/work/COPD/data/03_SCREENDATA_ex.csv')
ex_df['SM_DATE_N'] = ex_df['FVC_ENFR_DT'].map(lambda x: x[:7])
df = pd.concat([df, ex_df[['CDW_ID', 'SM_DATE_N', 'GEND_CD', 'AGE', 'RSLT_GRP', 'SEVERITY']]])
df = df.reset_index(drop=True)
# %%
print(len(df['CDW_ID'].drop_duplicates()))
# %%
df = df[df['RSLT_GRP'] != '']
df = df.dropna(subset=['RSLT_GRP'])
print(len(df['CDW_ID'].drop_duplicates()))
# %%
temp = pd.DataFrame(df['CDW_ID'].value_counts() >= 2)
valid_list = temp[temp.CDW_ID].index
df = df.query("CDW_ID in @valid_list")
print(len(df['CDW_ID'].drop_duplicates()))
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
print(len(df['CDW_ID'].drop_duplicates()))
# %%
temp = pd.DataFrame(df['CDW_ID'].value_counts() >= 2)
valid_list = temp[temp.CDW_ID].index
df = df.query("CDW_ID in @valid_list")
df = df.reset_index(drop=True)
# %%
print(len(df['CDW_ID'].drop_duplicates()))

# %%
res = []
for id in tqdm(valid_list):
    temp = df.query('CDW_ID == @id')
    date = '|'.join(temp['SM_DATE_N'].to_list())
    result = '|'.join(temp['RSLT_GRP'].to_list())
    res.append({'CDW_ID':id, 
                'SM_DATE_N': date,
                'RSLT_GRP': result})

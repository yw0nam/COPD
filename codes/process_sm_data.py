# %%
import pandas as pd
import numpy as np
import datatable 
from tqdm import tqdm
pd.set_option('display.max_columns', None)
# %%
sm_df_1 = datatable.fread('/mnt/hdd/spow12/work/COPD/data/03_SCREENDATA_SM_01.csv').to_pandas()
sm_df_2 = datatable.fread('/mnt/hdd/spow12/work/COPD/data/03_SCREENDATA_SM_02.csv').to_pandas()
sm_df = pd.concat([sm_df_1, sm_df_2])
sm_df = sm_df.reset_index(drop=True)
df = sm_df[['CDW_ID', 'SM_DATE_N', 'GEND_CD', 'AGE', 'RSLT_GRP', 'SEVERITY', 'PRED_SM0401', 'PRED_SM0402']]
df['SEVERITY'] = df[df['SEVERITY'] != ""]['SEVERITY'].map(lambda x: x[2:])
df['SM'] = 'Y'
df = df.rename(columns= {'PRED_SM0401': "FVC", 'PRED_SM0402': "FEV1"})
# %%
ex_df = pd.read_csv('/mnt/hdd/spow12/work/COPD/data/03_SCREENDATA_ex.csv')
ex_df['SM_DATE_N'] = ex_df['FVC_ENFR_DT'].map(lambda x: x[:7])
ex_df = ex_df.rename(columns={"FEV1_PRE": "FEV1", "FVC_PRE": "FVC"})
# %%
df = pd.concat([df, ex_df[['CDW_ID', 'SM_DATE_N', 'GEND_CD', 'AGE', 'RSLT_GRP', 'SEVERITY', "FEV1", "FVC", 'FVC_ENFR_DT']]])
df = df.reset_index(drop=True)
# %%
excel = pd.read_excel('../data/03_SCREENDATA_SM_결과비교.xlsx', sheet_name='Sheet1')
excel['SEVERITY_ORG'] = excel['SEVERITY_ORG'].dropna().map(lambda x: x[2:])
excel = excel[['CDW_ID', 'SM_DATE_N', 'RSLT_GRP_ORG', 'SEVERITY_ORG']]
# %%
df = pd.merge(df, excel, how='left', left_on=['CDW_ID', 'SM_DATE_N'], 
         right_on=['CDW_ID', 'SM_DATE_N'])
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
df['SM'] = df['SM'].fillna('N')
# %%
fvl_1 = pd.read_excel('./../data/03_SCREENDATA_SM_orgrslt_fvldata01.xlsx')
fvl_2 = pd.read_excel('./../data/03_SCREENDATA_SM_orgrslt_fvldata02.xlsx')
# %%
temp = pd.concat([fvl_1, fvl_2], ignore_index=True)
# %%
df = pd.merge(df, temp[['CDW_ID', 'SM_DATE_N', 'FVL_YN']], how='left', 
         left_on=['CDW_ID', 'SM_DATE_N'], right_on=['CDW_ID', 'SM_DATE_N'])
# %%
df['FVL_YN'] = df['FVL_YN'].fillna('N')
# %%
res = []
for id in tqdm(valid_list):
    temp = df.query('CDW_ID == @id')
    date = '|'.join(temp['SM_DATE_N'].to_list())
    result = '|'.join(temp['RSLT_GRP'].to_list())
    darwin_result = '|'.join(temp['RSLT_GRP_ORG'].fillna(temp['RSLT_GRP']).to_list())
    is_sm = '|'.join(temp['SM'].to_list())
    FVL = '|'.join(temp['FVL_YN'].to_list())
    res.append({'CDW_ID':id, 
                'SM_DATE_N': date,
                'RSLT_GRP': result,
                'RSLT_GRP_ORG': darwin_result,
                'GEND_CD' : temp['GEND_CD'].iloc[0],
                'AGE': temp['AGE'].iloc[0],
                'FVL_YN' : FVL,
                'sm': is_sm})
    
# %%
pd.DataFrame(res).to_csv('./../data/sm_ex_one_line.csv', index=False)
# %%    
df.to_csv('./../data/data.csv', index=False)

# %%

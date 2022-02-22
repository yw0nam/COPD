# %%
import pandas as pd
from tqdm import tqdm
# %%
abnormal = pd.read_csv('./../data/abnormal.csv')
normal = pd.read_csv('./../data/normal_only_first.csv')
csv = pd.read_csv('./../data/data.csv')
# %%
normal_sm = pd.merge(normal, csv[['CDW_ID', 'SM_DATE_N', 'SM', 'FVC_ENFR_DT', 'FVL_YN']], how='left',
         left_on=['CDW_ID', 'SM_DATE_N'], right_on=['CDW_ID', 'SM_DATE_N'])
# %%
normal_sm = normal_sm.drop_duplicates("CDW_ID")
# %%
abnormal_sm = pd.merge(abnormal, csv[['CDW_ID', 'SM_DATE_N', 'SM', 'FVC_ENFR_DT', 'FVL_YN']], how='left',
         left_on=['CDW_ID', 'SM_DATE_N'], right_on=['CDW_ID', 'SM_DATE_N'])

# %%
prev_id = abnormal_sm['CDW_ID'].iloc[0]
prev_date = abnormal_sm['SM_DATE_N'].iloc[0]
row_to_remove = []
for i in tqdm(range(1, len(abnormal_sm))):
    if prev_id != abnormal_sm['CDW_ID'].iloc[i]:
        pass
    elif prev_date == abnormal_sm['SM_DATE_N'].iloc[i]:
        row_to_remove.append(i)
    prev_id = abnormal_sm['CDW_ID'].iloc[i]
    prev_date = abnormal_sm['SM_DATE_N'].iloc[i]
# %%
df = abnormal_sm.drop(index=row_to_remove)
df = df.reset_index(drop=True)
# %%
df
# %%
grouped_csv = df.groupby("CDW_ID")
is_first_sm = grouped_csv.agg({"SM": lambda x: x.iloc[0] == 'Y'})
# %%
valid_id = list(is_first_sm.loc[is_first_sm['SM']].index)

# %%
df = df.query("CDW_ID in @valid_id")
normal_sm = normal_sm.query("SM == 'Y'")
# %%
df.to_csv('./../data/abnormal.with_sm_fvl.csv', index=False)
normal_sm.to_csv('./../data/normal.with_sm_fvl.csv', index=False)

# %%

# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
from utils import *
# %%
csv = pd.read_csv('./../data/data.csv')
csv['FEV1per_FVC'] = (csv['FEV1'] / csv['FVC']).map(lambda x: round(x, 3) * 100)
grouped_csv = csv.groupby('CDW_ID')
# %%
t = grouped_csv.agg({"RSLT_GRP": lambda x: x.iloc[0] == "1.Normal"})
temp = t.loc[t.values].index
# %%
first_normal_csv = csv.query("CDW_ID in @temp")
# %%
grouped_csv = first_normal_csv.groupby('CDW_ID')
# %%
is_all_normal = grouped_csv.agg({"RSLT_GRP": lambda x: (x == "1.Normal").all()})
all_normal_id = is_all_normal.loc[is_all_normal.values].index
event_id = is_all_normal.loc[~is_all_normal.values].index
# %%
abnormal_csv = first_normal_csv.query("CDW_ID in @event_id")
normal_csv = first_normal_csv.query("CDW_ID in @all_normal_id")
# %%
normal_group = normal_csv.groupby("CDW_ID").agg({"SM_DATE_N": lambda x: x.iloc[0]})
# %%
normal_group['CDW_ID'] = normal_group.index
# %%
sm_date_counts = grouped_csv.agg({'SM_DATE_N':'count'}).sort_values(by="SM_DATE_N", 
                                                   ascending=False).iloc[:10]
# %%
temp = sm_date_counts.index
csv.query("CDW_ID in @temp").to_excel('../data/exporting_data/sort_by_many_exam.xlsx', index=False)
# %%
first_normal_csv['exam_year_over_2012'] = first_normal_csv['SM_DATE_N'].map(lambda x: "Y" if x[:4] >= "2012" else "N")
draw_pieplot(first_normal_csv['exam_year_over_2012'], 
             save_path='../figure/exam_year_over_2012.png',
             plot_title="Exam year over 2012")
# %%
fvc_gap = grouped_csv.agg({"FVC" : lambda x: x.max() - x.min()})
# %%
temp = fvc_gap.sort_values(by='FVC', ascending=False).iloc[:10].index
csv.query("CDW_ID in @temp").to_excel('../data/exporting_data/sort_by_fvc_gap.xlsx', index=False)
# %%
first_normal_csv.query("RSLT_GRP == '2.Restrictive'")['FVC'].hist()
# %%
first_normal_csv.query("RSLT_GRP == '2.Restrictive'")['SEVERITY'].hist()
# %%
def count_obstructive(x):
    return len(x[x == "3.Obstructive"])
count_obs_df = grouped_csv.agg({"RSLT_GRP": lambda x: count_obstructive(x)})
# %%
temp = count_obs_df.sort_values(by="RSLT_GRP", ascending=False).iloc[:10].index
csv.query("CDW_ID in @temp").to_excel('../data/exporting_data/sort_by_obstructive.xlsx', index=False)
# %%

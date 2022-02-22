# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
from utils import *
# %%
csv = pd.read_csv('./../data/sm_ex_one_line.csv')
# %%
csv['first_result'] = csv['RSLT_GRP'].map(lambda x: x.split('|')[0])
csv['last_result'] = csv['RSLT_GRP'].map(lambda x: x.split('|')[-1])
# %%
draw_pieplot(csv['first_result'], save_path='./../figure/First_result_distribution.png',
             plot_title="First Result Distribution")
# %%
csv_first_normal = csv.query("first_result == '1.Normal'")
# %%
def map_fn(grp):
    group_ls = grp.split('|')
    for idx, group in enumerate(group_ls):
        if group != '1.Normal':
            return idx, group
        else:
            continue
    return idx, group
# %%
temp = csv_first_normal['RSLT_GRP'].map(lambda x: map_fn(x))
csv_first_normal['event_grp'] = temp.map(lambda x: x[1])
csv_first_normal['event_grp_idx'] = temp.map(lambda x: x[0])
# %%
draw_pieplot(csv_first_normal['event_grp'], save_path='../figure/event_distribution.png', 
             plot_title='event Result Distribution')
# %%
temp = csv_first_normal['RSLT_GRP_ORG'].map(lambda x: map_fn(x))
csv_first_normal['event_grp_ORG'] = temp.map(lambda x: x[1])
csv_first_normal['event_grp_idx_ORG'] = temp.map(lambda x: x[0])
# %%
draw_pieplot(csv_first_normal['event_grp_ORG'], save_path='../figure/event_distribution_with_darwin.png', 
             plot_title='event Result with darwin Distribution')
# %%
pd.crosstab(csv_first_normal['event_grp_ORG'], csv_first_normal['event_grp'])
# %%
def apply_fn(sm_date, idx):
    date_ls = sm_date.split('|')
    return date_ls[0], date_ls[idx]

temp = csv_first_normal.apply(lambda x: apply_fn(x['SM_DATE_N'], x['event_grp_idx']), axis=1)
csv_first_normal['event_grp_first_date'] = temp.map(lambda x: x[0])
csv_first_normal['event_grp_event_date'] = temp.map(lambda x: x[1])
csv_first_normal['event_fu_length']  = (pd.to_datetime(csv_first_normal['event_grp_event_date']) - pd.to_datetime(csv_first_normal['event_grp_first_date'])).map(lambda x: x.days // 30)
# %%
plot_hist_with_group(csv_first_normal, 'event_grp', 'event_fu_length', '../figure/group_hist.png')
# %%
temp = csv_first_normal.apply(lambda x: apply_fn(x['SM_DATE_N'], x['event_grp_idx_ORG']), axis=1)
csv_first_normal['event_grp_ORG_first_date'] = temp.map(lambda x: x[0])
csv_first_normal['event_grp_ORG_event_date'] = temp.map(lambda x: x[1])
csv_first_normal['event_fu_length_ORG']  = (pd.to_datetime(csv_first_normal['event_grp_ORG_event_date']) - pd.to_datetime(csv_first_normal['event_grp_ORG_first_date'])).map(lambda x: x.days // 30)
# %%
plot_hist_with_group(csv_first_normal, 'event_grp_ORG', 'event_fu_length_ORG', '../figure/group_hist_ORG.png')
# %%
csv_first_normal.groupby(['GEND_CD', 'event_grp']).size()
# %%
csv_first_normal.groupby(['GEND_CD', 'event_grp_ORG']).size()
# %%
plt.figure(figsize=(12, 8))
sns.histplot(data=csv_first_normal, x='AGE', hue='event_grp', multiple='stack',
             hue_order=['4.Combined', '3.Obstructive', "2.Restrictive", '1.Normal'])
plt.savefig('./../figure/Age_distribution.png')
# %%
def map_fn(age):
    if age < 40:
        return "Under 40"
    elif age >= 40 and age < 55:
        return "Over 40, Under 55"
    else:
        return "Over 55"
csv_first_normal['AGE_bin'] = csv_first_normal['AGE'].map(lambda x: map_fn(x))
# %%
t = csv_first_normal.groupby(['AGE_bin', 'event_grp'])
# %%
pd.DataFrame(t.size(), columns=['Count'])
# %%
# data_40_55 = [32075, 8334, 2717, 154]
# data_55 = [8965, 3293, 1590, 132]
# data_40 = [10846, 1375, 286, 21]
# [i / sum(data_55) for i in data_55]
# %%
csv_first_normal['event_date_fvl'] = csv_first_normal.apply(lambda x: x['FVL_YN'].split('|')[x['event_grp_idx']], axis=1)
csv_first_normal['first_date_fvl'] = csv_first_normal.apply(lambda x: x['FVL_YN'].split('|')[0], axis=1)
# %%
csv_first_normal['event_date_fvl'].value_counts()
# %%
draw_pieplot(csv_first_normal['event_date_fvl'], 
             './../figure/event_date_fvl.png', "Event date FVL")
# %%
draw_pieplot(csv_first_normal['first_date_fvl'], 
             './../figure/first_date_fvl.png', "First date FVL")
# %%
csv_first_normal['first_date_fvl'].value_counts()
# %%
csv_first_normal.groupby(['GEND_CD', 'event_grp']).size()

# %%
csv_first_normal['event_grp'] = pd.Categorical(csv_first_normal['event_grp'], ['1.Normal', '2.Restrictive', '3.Obstructive', '4.Combined'])
csv_first_normal['first_result'] = pd.Categorical(csv_first_normal['event_grp'], ['1.Normal', '2.Restrictive', '3.Obstructive', '4.Combined'])
# %%
fig = plt.figure(figsize=(12, 8))
sns.set_style('dark')
area1 = fig.add_subplot(1, 2, 1)
area1.set_title('Female')
sns.histplot(data=csv_first_normal.query("GEND_CD == 'F'"), x='event_grp', ax=area1)
area2 = fig.add_subplot(1, 2, 2)
area2.set_title('Male')
sns.histplot(data=csv_first_normal.query("GEND_CD == 'M'"), x='event_grp', ax=area2)
plt.savefig('./../figure/event_grp_gend.png')


# %%

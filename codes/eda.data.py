# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

def draw_pieplot(df_series, save_path, plot_title):
    temp = df_series.value_counts()
    fig1, ax1 = plt.subplots(figsize=(8,12))
    cmap = plt.get_cmap("Set2")
    colors = cmap(np.array([1, 2, 3, 4]))
    explode = (0.05, 0.05, 0.05, 0.05)
    ax1.pie(temp.values, labels=temp.index.map(lambda x: x[0]), autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'white'},
        shadow=False,
        # textprops={'fontsize': 7},
        pctdistance=0.85,
        counterclock=False,
        # explode=explode,
        colors=colors
    )
    plt.text(0, 0, 'Number of patient =%d'%len(df_series), horizontalalignment='center',
        verticalalignment='center',bbox=dict(facecolor='white', alpha=0.5))
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax1.axis('equal')
    plt.legend(temp.index)
    plt.title(plot_title, fontsize=16, pad=10)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

def plot_hist_with_group(df, event_col,length_col, save_path, xlim=(0, 260)):
    fig = plt.figure(figsize=(20, 5))
    sns.set_style('dark')
    area1 = fig.add_subplot(1, 4, 1)
    area1.set_title('Event Group == Normal  follow up lengths')
    area1.set(xlim=xlim)
    area2 = fig.add_subplot(1, 4, 2)
    area2.set_title('Event Group == Restrictive follow up lengths')
    area2.set(xlim=xlim)
    area3 = fig.add_subplot(1, 4, 3)
    area3.set(xlim=xlim)
    area3.set_title('Event Group == Obstructive follow up lengths')
    area4 = fig.add_subplot(1, 4, 4)
    area4.set(xlim=xlim)
    area4.set_title('Event Group == Combined follow up lengths')
    sns.histplot(csv_first_normal.query("%s == '1.Normal'"%(event_col))[length_col], ax=area1)
    sns.histplot(csv_first_normal.query("%s == '2.Restrictive'"%(event_col))[length_col], ax=area2)
    sns.histplot(csv_first_normal.query("%s == '3.Obstructive'"%(event_col))[length_col], ax=area3)
    sns.histplot(csv_first_normal.query("%s == '4.Combined'"%(event_col))[length_col], ax=area4)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
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
csv_first_normal
# %%
def apply_fn(sm_date, idx):
    date_ls = sm_date.split('|')
    return date_ls[0], date_ls[idx]

temp = csv_first_normal.apply(lambda x: apply_fn(x['SM_DATE_N'], x['event_grp_idx']), axis=1)
csv_first_normal['event_grp_first_date'] = temp.map(lambda x: x[0])
csv_first_normal['event_grp_event_date'] = temp.map(lambda x: x[1])
# %%
csv_first_normal['event_fu_length']  = (pd.to_datetime(csv_first_normal['event_grp_event_date']) - pd.to_datetime(csv_first_normal['event_grp_first_date'])).map(lambda x: x.days // 30)
# %%
fig = plt.figure(figsize=(20, 5))
xlim = (0, 260)
sns.set_style('dark')
area1 = fig.add_subplot(1, 4, 1)
area1.set_title('Event Group == Normal  follow up lengths')
area1.set(xlim=xlim)
area2 = fig.add_subplot(1, 4, 2)
area2.set_title('Event Group == Restrictive follow up lengths')
area2.set(xlim=xlim)
area3 = fig.add_subplot(1, 4, 3)
area3.set(xlim=xlim)
area3.set_title('Event Group == Obstructive follow up lengths')
area4 = fig.add_subplot(1, 4, 4)
area4.set(xlim=xlim)
area4.set_title('Event Group == Combined follow up lengths')
sns.histplot(csv_first_normal.query("event_grp == '1.Normal'")['event_fu_length'], ax=area1)
sns.histplot(csv_first_normal.query("event_grp == '2.Restrictive'")['event_fu_length'], ax=area2)
sns.histplot(csv_first_normal.query("event_grp == '3.Obstructive'")['event_fu_length'], ax=area3)
sns.histplot(csv_first_normal.query("event_grp == '4.Combined'")['event_fu_length'], ax=area4)
# %%
temp = csv_first_normal.apply(lambda x: apply_fn(x['SM_DATE_N'], x['event_grp_idx_ORG']), axis=1)
csv_first_normal['event_grp_ORG_first_date'] = temp.map(lambda x: x[0])
csv_first_normal['event_grp_ORG_event_date'] = temp.map(lambda x: x[1])
csv_first_normal['event_fu_length_ORG']  = (pd.to_datetime(csv_first_normal['event_grp_ORG_event_date']) - pd.to_datetime(csv_first_normal['event_grp_ORG_first_date'])).map(lambda x: x.days // 30)
# %%
fig = plt.figure(figsize=(20, 5))
xlim = (0, 260)
sns.set_style('dark')
area1 = fig.add_subplot(1, 4, 1)
area1.set_title('Event Group == Normal  follow up lengths')
area1.set(xlim=xlim)
area2 = fig.add_subplot(1, 4, 2)
area2.set_title('Event Group == Restrictive follow up lengths')
area2.set(xlim=xlim)
area3 = fig.add_subplot(1, 4, 3)
area3.set(xlim=xlim)
area3.set_title('Event Group == Obstructive follow up lengths')
area4 = fig.add_subplot(1, 4, 4)
area4.set(xlim=xlim)
area4.set_title('Event Group == Combined follow up lengths')
sns.histplot(csv_first_normal.query("event_grp_ORG == '1.Normal'")['event_fu_length'], ax=area1)
sns.histplot(csv_first_normal.query("event_grp_ORG == '2.Restrictive'")['event_fu_length'], ax=area2)
sns.histplot(csv_first_normal.query("event_grp_ORG == '3.Obstructive'")['event_fu_length'], ax=area3)
sns.histplot(csv_first_normal.query("event_grp_ORG == '4.Combined'")['event_fu_length'], ax=area4)
# %%
csv_first_normal.groupby(['GEND_CD', 'event_grp']).size()
# %%
csv_first_normal.groupby(['GEND_CD', 'event_grp_ORG']).size()
# %%
sns.histplot(data=csv_first_normal, x='AGE', hue='event_grp', multiple='stack')

# %%

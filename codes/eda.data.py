# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


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
csv_first_normal.query('event_grp != event_grp_ORG')
# %%

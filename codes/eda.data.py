# %%
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
# %%
csv = pd.read_csv('./../data/sm_ex_one_line.csv')
# %%
csv['first_result'] = csv['RSLT_GRP'].map(lambda x: x.split('|')[0])
csv['last_result'] = csv['RSLT_GRP'].map(lambda x: x.split('|')[-1])
# %%
csv['first_result'].value_counts()
# %%
csv['last_result'].value_counts()
# %%
temp = csv['first_result'].value_counts()
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
plt.text(0, 0, 'Number of patient =%d'%len(csv), horizontalalignment='center',
        verticalalignment='center',bbox=dict(facecolor='white', alpha=0.5))
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
ax1.axis('equal')
plt.legend(temp.index)
plt.title('First Result Distribution', fontsize=16, pad=10)
plt.tight_layout()
plt.show()
# %%
csv_first_normal = csv.query("first_result == '1.Normal'")
# %%
temp = csv_first_normal['last_result'].value_counts()
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
plt.text(0, 0, 'Number of patient =%d'%len(csv_first_normal), horizontalalignment='center',
        verticalalignment='center',bbox=dict(facecolor='white', alpha=0.5))
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
ax1.axis('equal')
plt.legend(temp.index)
plt.title('Final Result Distribution', fontsize=16, pad=10)
plt.tight_layout()
plt.show()
# %%
csv_first_normal['first_result'].value_counts()
# %%
csv_first_normal['last_result'].value_counts()
# %%

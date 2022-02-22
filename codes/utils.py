import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def draw_pieplot(df_series, save_path=None, plot_title=None):
    temp = df_series.value_counts()
    fig1, ax1 = plt.subplots(figsize=(8,12))
    cmap = plt.get_cmap("Set2")
    # colors = cmap(np.array([1, 2, 3, 4]))
    explode = (0.05, 0.05, 0.05, 0.05)
    ax1.pie(temp.values, labels=temp.index.map(lambda x: x[0]), autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'white'},
        shadow=False,
        # textprops={'fontsize': 7},
        pctdistance=0.85,
        counterclock=False,
        # explode=explode,
        # colors=colors
    )
    plt.text(0, 0, 'Number of sample =%d'%len(df_series), horizontalalignment='center',
        verticalalignment='center',bbox=dict(facecolor='white', alpha=0.5))
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax1.axis('equal')
    plt.legend(temp.index)
    plt.title(plot_title, fontsize=16, pad=10)
    plt.tight_layout()
    if save_path:
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
    sns.histplot(df.query("%s == '1.Normal'"%(event_col))[length_col], ax=area1)
    sns.histplot(df.query("%s == '2.Restrictive'"%(event_col))[length_col], ax=area2)
    sns.histplot(df.query("%s == '3.Obstructive'"%(event_col))[length_col], ax=area3)
    sns.histplot(df.query("%s == '4.Combined'"%(event_col))[length_col], ax=area4)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
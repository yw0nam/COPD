# %%
import pandas as pd
import numpy as np
import datatable 
from tqdm import tqdm

# %%
df = pd.read_excel('/mnt/hdd/spow12/work/COPD/data/03_SCREENDATA_외래.xlsx')
# %%
pd.read_csv('')
# %%
# 책임님이주신것은 올림으로 처리되어있음, 반올림으로 대체
df['FEV1FVC_PRE'] = round((df['FEV1_PRE'] / df['FVC_PRE'])  * 100, 0).astype(int)
# %%
def cal_COPD(FEV1_over_FVC, FVC, FEV1):
    """
    Calculate COPD group using COPD definition.

    Args:
        FEV1_over_FVC (int): calculate by following formula ((FEV1 / FVC) * 100, 0) 
        FVC (int): FVC percentage 
        FEV1 (int):  FEV1 percentage
    """
    if FEV1_over_FVC >= 70:
        if FVC >= 80:
            return "1.Normal", None
        elif FVC >= 60 and FVC < 80:
            return "2.Restrictive", 'Mild'
        elif FVC >= 50 and FVC < 60:
            return "2.Restrictive", 'Moderate'
        elif FVC < 50:
            return "2.Restrictive", 'Severe'
    elif FEV1_over_FVC < 70:
        if FVC >= 80:
            if FEV1 >= 80:
                return "3.Obstructive", 'Mild'
            elif FEV1 >= 50 and FEV1 < 80:
                return "3.Obstructive", 'Moderate'
            elif FEV1 >= 30 and FEV1 < 50:
                return "3.Obstructive", 'Severe'
            elif FEV1 < 30:
                return "3.Obstructive", 'Very Severe'
        elif FVC < 80:
            return "4.Combined", None

result= df.apply(lambda x: cal_COPD(x['FEV1FVC_PRE'], x['FVC_PRED'], x['FEV1_PRED']), axis=1)
df['RSLT_GRP'] = result.map(lambda x: x[0])
df['SEVERITY'] = result.map(lambda x: x[1])
# %%
df.to_csv('/mnt/hdd/spow12/work/COPD/data/03_SCREENDATA_ex.csv', index=False)
# %%

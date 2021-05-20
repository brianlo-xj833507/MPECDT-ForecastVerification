"""
Script to read raw data and split it in one dataset per projection
"""

import glob
import pandas as pd
datapath = '../data/raw/'
file = glob.glob(datapath + '*.txt')
df = pd.read_table(file[0])
dfs_list = list(df.groupby('HOUR_FCST'))
for proj, df in dfs_list:
    df.to_csv(f'../data/by_projection/Projection_{proj}h.txt', index=False)

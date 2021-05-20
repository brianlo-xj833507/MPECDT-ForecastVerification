"""
Script to read and merge raw data files.
"""
import glob
import pandas as pd
datapath = '../data/raw/Project 2_data {proj}h.txt'
ds_list = []
projections = [24, 48, 72, 96, 120]
for proj in projections:
    df = pd.read_table(datapath.format(proj=proj))
    df['Projection'] = proj
    df = df.set_index(['Date', 'Projection'])
    ds_list.append(df)
df = pd.concat(ds_list, axis=0)

print(df)
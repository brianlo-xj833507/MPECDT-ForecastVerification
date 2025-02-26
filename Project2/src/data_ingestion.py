"""
Script to read and merge raw data files.
"""
import glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def read_data():
    df_all = pd.DataFrame()
    projections = [24, 48, 72, 96, 120]
    for proj in projections:
        datapath = f'../data/raw/Project 2_data {proj}h.txt'
        df = pd.read_table(datapath)
        df['Projection'] = proj
        df['Date'] = df['Date'].astype(str).str[0:8]
        df['Date'] = pd.to_datetime(df['Date'], format="%Y%m%d")
        df.mask(df == -99, inplace=True)
        df_all = pd.concat([df_all, df], axis=0)

    # Calculate "Ensemble" Mean
    df_all['Ens'] = df_all[['GSM0p50', 'GFS', 'IFS']].mean(axis=1)

    # Station Information
    station_info = pd.DataFrame(np.array(
        [[48327, "Chiang Mai", 18.783, 98.983],
         [48820, "Ha Noi", 21.017, 105.800],
         [48894, "Ho Chi Minh City", 10.650, 106.717],
         [48455, "Bangkok", 13.733, 100.567],
         [48940, "Vientiane", 17.950, 102.567],
         [48947, "Savannakhet", 13.550, 104.650]]),
        columns=['StationID', 'Name', 'Lat', 'Lon'])
    new_dtypes = {"StationID": int, "Name": 'string', "Lat": np.float32, "Lon": np.float32}
    station_info = station_info.astype(new_dtypes)

    df_all = pd.merge(df_all, station_info, left_on='StationID', right_on='StationID')
    df_all = df_all.set_index(["Date"])
    return df_all


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    df = read_data()
    print(df)
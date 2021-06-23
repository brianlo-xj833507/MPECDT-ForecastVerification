"""Calculates verification metrics with confidence intervals"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
import xskillscore as xs

from data_ingestion import read_data

def resample_dataset(filtered_df):
    return filtered_df.sample(frac=1, replace=True)

def convert_resampled_df_to_xarray(resampled_df):
    return resampled_df.to_xarray()

def bootstrap_calc_metrics(filtered_df, bootstrap_num_times=1000, fcst_name=None):
    multi_category_edges = np.array([0, 1.0, 30.0, 1000.0])
    filtered_xr = convert_resampled_df_to_xarray(filtered_df)
    multicategory_contingency = xs.Contingency(
        filtered_xr['Observation'], filtered_xr[fcst_name], multi_category_edges, multi_category_edges, dim='Date')
    print(multicategory_contingency.accuracy())
    print(multicategory_contingency.heidke_score())
    print(multicategory_contingency.peirce_score())
    print(multicategory_contingency.gerrity_score())

    for _ in range(bootstrap_num_times):
        resampled_df = resample_dataset(filtered_df)
        resampled_xr = convert_resampled_df_to_xarray(resampled_df)
        multicategory_contingency = xs.Contingency(
            resampled_xr['Observation'], resampled_xr[fcst_name], multi_category_edges, multi_category_edges, dim='Date')



def plot_roc(filtered_df, fcst_name=None):
    filtered_xr = convert_resampled_df_to_xarray(filtered_df)
    roc = xs.roc(filtered_xr['Observation'], filtered_xr[fcst_name], bin_edges=np.array([0,1.0,5.0,10.0,20.0,30.0,1000]), return_results='all_as_metric_dim')

    plt.figure(figsize=(4, 4))
    plt.plot([0, 1], [0, 1], 'k:')
    roc.to_dataset(dim='metric').plot.scatter(y='true positive rate', x='false positive rate')
    print(roc.sel(metric='area under curve').values[0])
    plt.show()

if __name__ == '__main__':
    pd.set_option('display.max_columns', None)

    df_all = read_data()

    station_names = ["Chiang Mai", "Ha Noi", "Ho Chi Minh City", "Bangkok", "Vientiane", "Savannakhet"]
    lead_times = [24, 48, 72, 96, 120]

    df = df_all.loc[(df_all['Name'] == "Chiang Mai") & (df_all['Projection'] == 24)]
    resampled = resample_dataset(df)
    resampled_xr = convert_resampled_df_to_xarray(resampled)
    # print(df)
    # print(resampled_xr)

    bootstrap_calc_metrics(df, fcst_name='GSM0p50')

    plot_roc(df, fcst_name='GSM0p50')
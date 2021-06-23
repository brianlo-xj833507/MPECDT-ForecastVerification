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

def get_multi_cat_metrics(multicat_cont_obj):
    acc = multicat_cont_obj.accuracy().values
    hss = multicat_cont_obj.heidke_score().values
    pss = multicat_cont_obj.peirce_score().values
    gss = multicat_cont_obj.gerrity_score().values

    score_list_np = np.array([[acc, hss, pss, gss]])
    score_list = pd.DataFrame(score_list_np, columns=['ACC', 'HSS', 'PSS', 'GSS'])
    return score_list


def bootstrap_calc_metrics(filtered_df, bootstrap_num_times=1000, fcst_name=None):
    multi_category_edges = np.array([0, 1.0, 30.0, 1000.0])
    # filtered_xr = convert_resampled_df_to_xarray(filtered_df)
    # multicategory_contingency = xs.Contingency(
    #     filtered_xr['Observation'], filtered_xr[fcst_name], multi_category_edges, multi_category_edges, dim='Date')
    # print(multicategory_contingency.accuracy())
    # print(multicategory_contingency.heidke_score())
    # print(multicategory_contingency.peirce_score())
    # print(multicategory_contingency.gerrity_score())

    master_score_lists = pd.DataFrame()
    for _ in range(bootstrap_num_times):
        resampled_df = resample_dataset(filtered_df)
        resampled_xr = convert_resampled_df_to_xarray(resampled_df)
        multicategory_contingency = xs.Contingency(
            resampled_xr['Observation'], resampled_xr[fcst_name], multi_category_edges, multi_category_edges, dim='Date')
        this_resample_score_list = get_multi_cat_metrics(multicategory_contingency)
        master_score_lists = pd.concat([master_score_lists, this_resample_score_list], axis=0)

    master_score_lists.reset_index(drop=True, inplace=True)
    return master_score_lists

def difference_in_bootstrapped_metrics(filtered_df, fcst_name1, fcst_name2):
    fcst1_metrics = bootstrap_calc_metrics(filtered_df, fcst_name=fcst_name1)
    fcst2_metrics = bootstrap_calc_metrics(filtered_df, fcst_name=fcst_name2)
    delta_metrics = fcst2_metrics - fcst1_metrics
    p95_median = delta_metrics.quantile(q=0.500, axis=0, interpolation='midpoint')
    p95_median.name = "50.0%-ile"
    p95_lower = delta_metrics.quantile(q=0.025, axis=0, interpolation='midpoint')
    p95_lower.name = "2.5%-ile"
    p95_upper = delta_metrics.quantile(q=0.975, axis=0, interpolation='midpoint')
    p95_upper.name = "97.5%-ile"

    delta_metrics_ci = pd.concat([p95_median, p95_lower, p95_upper], axis=1)

    return delta_metrics_ci


###########################

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

    df = df_all.loc[(df_all['Projection'] == 24)]
    # resampled = resample_dataset(df)
    # resampled_xr = convert_resampled_df_to_xarray(resampled)
    # print(df)
    # print(resampled_xr)

    # all_scores_GSM0p50 = bootstrap_calc_metrics(df, fcst_name='GSM0p50')
    # print(all_scores_GSM0p50)

    station_names = ["Chiang Mai", "Ha Noi", "Ho Chi Minh City", "Bangkok", "Vientiane", "Savannakhet"]
    lead_times = [24, 48, 72, 96, 120]

    for lead_time in lead_times:
        df = df_all.loc[(df_all['Projection'] == lead_time)]
        IFS_GSM0p50_ci = difference_in_bootstrapped_metrics(df, 'GSM0p50', 'IFS')
        IFS_GSM0p50_ci.name = f'IFS_minus_GSM0p50_allstations_{lead_time}h'
        IFS_GSM0p50_ci.to_csv(f'../output/{IFS_GSM0p50_ci.name}.csv')
        GFS_GSM0p50_ci = difference_in_bootstrapped_metrics(df, 'GSM0p50', 'GFS')
        GFS_GSM0p50_ci.name = f'GFS_minus_GSM0p50_allstations_{lead_time}h'
        GFS_GSM0p50_ci.to_csv(f'../output/{GFS_GSM0p50_ci.name}.csv')
        GFS_IFS_ci = difference_in_bootstrapped_metrics(df, 'IFS', 'GFS')
        GFS_IFS_ci.name = f'GFS_minus_IFS_allstations_{lead_time}h'
        GFS_IFS_ci.to_csv(f'../output/{GFS_IFS_ci.name}.csv')


    for station_name in station_names:
        for lead_time in lead_times:
            df = df_all.loc[(df_all['Name'] == station_name) & (df_all['Projection'] == lead_time)]
            IFS_GSM0p50_ci = difference_in_bootstrapped_metrics(df, 'GSM0p50', 'IFS')
            IFS_GSM0p50_ci.name = f'IFS_minus_GSM0p50_{station_name}_{lead_time}h'
            IFS_GSM0p50_ci.to_csv(f'../output/{IFS_GSM0p50_ci.name}.csv')
            GFS_GSM0p50_ci = difference_in_bootstrapped_metrics(df, 'GSM0p50', 'GFS')
            GFS_GSM0p50_ci.name = f'GFS_minus_GSM0p50_{station_name}_{lead_time}h'
            GFS_GSM0p50_ci.to_csv(f'../output/{GFS_GSM0p50_ci.name}.csv')
            GFS_IFS_ci = difference_in_bootstrapped_metrics(df, 'IFS', 'GFS')
            GFS_IFS_ci.name = f'GFS_minus_IFS_{station_name}_{lead_time}h'
            GFS_IFS_ci.to_csv(f'../output/{GFS_IFS_ci.name}.csv')

    # plot_roc(df, fcst_name='GFS')
import pandas as pd
import glob
from copy import deepcopy
import numpy as np


def open_and_concat(filepaths):
    """
    Helper function
    """
    concat_list = []
    for filepath in filepaths:
        df = pd.read_table(filepath)
        if df.shape[1] == 1:
            df = pd.read_csv(filepath)
        concat_list.append(df)
    return pd.concat(concat_list, axis=0)

def read_data(raw_datapath):
    """
    Reads raw files and return pandas dataframes
    Parameters
    ----------
    raw_datapath: path for raw files

    Returns
    -------
    Pandas Dataframes
    """
    UKMetfiles = glob.glob(raw_datapath + 'UKMet*.txt')
    allfiles = glob.glob(raw_datapath + '*.txt')
    ECMWFfiles = list(set(allfiles).difference(set(UKMetfiles)))
    ECMWFfiles.sort()
    UKMetfiles.sort()
    ECMWF_df = open_and_concat(ECMWFfiles)
    UKMet_df = open_and_concat(UKMetfiles)
    # ---- Storing only two files with all forecast dates ---- #
    ECMWF_df.to_csv('../data/processed/ECMWF_ALL_FCdates.csv', index=False)
    UKMet_df.to_csv('../data/processed/UKMet_ALL_FCdates.csv', index=False)
    return ECMWF_df, UKMet_df


if __name__ == '__main__':
    datapath = '../data/raw/'
    df = read_data(datapath)
    ECMWF_df, UKMet_df = read_data(datapath)

    steps = np.arange(24, 24*7, 24)
    for step in steps:
        UKMet_df_step = UKMet_df.loc[UKMet_df['step'] == step]
        ECMWF_df_step = UKMet_df.loc[UKMet_df['step'] == step]
        merged_df = ECMWF_df_step.merge(UKMet_df_step, how='inner',
                                        left_on=['FCdate', 'lat', 'lon', 'STAT_ID', 'step', 'VT', 'OBS'],
                                        right_on=['FCdate', 'lat', 'lon', 'STAT_ID', 'step', 'VT', 'OBS'],
                                        suffixes=('_ECMWF', '_UKMet'))
        merged_df.to_csv(f'../data/processed/merged_step_{step}hrs.txt', index=False)

    ECMWF_df.merge(UKMet_df, how='outer').columns
    pd.read_csv(UKMetfiles[0])
    pd.merge
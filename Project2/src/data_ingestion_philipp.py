"""
Script to read and merge raw data files.
"""
import pandas as pd


def get_data_as_pandas_df(projections=None, bins=None):
    """ Reads in the data into a pandas dataframe and bins the continuous rainfall data.

    :param projections: list of hours we project into the future
    :type projections: list
    :param bins: list of bin boarders we use to bin the continuous rainfall data
    :type bins: list
    :return: data as a pandas dataframe
    :rtype: pandas dataframe
    """
    if bins is None:
        bins = [0.0, 1, 30, 1000]
    if projections is None:
        projections = [24, 48, 72, 96, 120]

    # Labels of the bins
    labels = range(len(bins) - 1)

    datapath = '../data/raw/Project 2_data {proj}h.txt'
    ds_list = []
    for proj in projections:
        df = pd.read_table(datapath.format(proj=proj))
        df['Projection'] = proj
        df = df.set_index(['Date'])
        ds_list.append(df)
    df = pd.concat(ds_list, axis=0)

    # Make an additional entry with categorical data
    for entry in ['Observation', 'GSM0p50', 'GFS', 'IFS']:
        df[entry + '_bin'] = pd.cut(df[entry], bins=bins, labels=labels,
                                    include_lowest=True)
    return df


def get_xarray_data(projection, stationdid):
    """ Given the projection and StationID, cast the pandas datafram into an xarray dataframe.

    :param projection: The hours we project into the future
    :type projection: str
    :param stationdid: The ID of the raingage station, possible values: [48327 48455 48820 48894 48940 48947]
    :type stationdid: str
    :return: The data as an xarray dataframe
    :rtype: xarray dataframe
    """

    df = get_data_as_pandas_df()
    df = df.query('(Projection == {0}) &  (StationID == {1})'.format(projection, stationdid))
    df = df.to_xarray()
    return df


if __name__ == "__main__":
    df = get_xarray_data('24', '48327')
    df = get_data_as_pandas_df()

    print(df.index)

import numpy as np
import xarray as xr
import xskillscore as xs
from data_ingestion_philipp import get_xarray_data, get_data_as_pandas_df
import matplotlib.pyplot as plt

np.random.seed(seed=42)


def resample_dataset(df):
    return df.sample(frac=1, replace=True)


def bootstrap(func):
    """Decorator to bootstrap over the data and create a contingency table which is then fed into the function
    'number of straps' times. """

    def wrapper(stationid, leadtime, model_name, number_of_straps=1000, category_edges = None):

        return_list = []

        if category_edges is None:
            category_edges = np.array([0.0, 1, 30, 1000])

        # Get the data
        df = get_data_as_pandas_df()
        df = df.query('(Projection == {0}) &  (StationID == {1})'.format(leadtime, stationid))
        df = df[['Observation', model_name]]

        for i in range(number_of_straps):
            # Copy the data, resample and turn into xarray
            df_resampled = df.copy()
            df_resampled = resample_dataset(df_resampled)
            df_resampled = df_resampled.to_xarray()

            # setup contingency table
            obs = df_resampled['Observation']
            forc = df_resampled[model_name]
            multicategory_contingency = xs.Contingency(obs, forc, category_edges, category_edges, dim=['Date'])

            # Write the results of the function into a list for returning
            return_list.append(func(multicategory_contingency))

        return return_list

    return wrapper


def single_contingency(func):
    """Decorator that sets up a contingency table to feed into the function."""
    def wrapper(stationid, leadtime, model_name):
        contingency = setup_contingency_table(stationid, leadtime, model_name, category_edges=None)
        return func(contingency)

    return wrapper


def setup_contingency_table(station_id, lead_time, model_name, category_edges=None):
    """Given the location, lead time and model, sets up the contingency table."""
    if category_edges is None:
        category_edges = [0.0, 1, 30, 1000]
    category_edges = np.array(category_edges)
    df = get_xarray_data(lead_time, station_id)

    obs = df['Observation']
    forc = df[model_name]

    multicategory_contingency = xs.Contingency(obs, forc, category_edges, category_edges, dim=['Date'])

    return multicategory_contingency


@single_contingency
def gerrity_score(multicategory_contingency):
    return multicategory_contingency.gerrity_score()

@single_contingency
def accuracy(multicategory_contingency):
    return multicategory_contingency.accuracy()

@bootstrap
def accuracy_error(multicategory_contingency):
    return multicategory_contingency.accuracy().values


if __name__ == "__main__":
    print(accuracy('48455', '48', 'GFS'))
    print(gerrity_score('48455', '48', 'GFS'))

    list = accuracy_error('48455', '48', 'GFS')
    print(list)

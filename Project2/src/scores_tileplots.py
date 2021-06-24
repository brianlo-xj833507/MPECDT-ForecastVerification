import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def make_file_path(basepath, models, station, leadtime):
    filepath = basepath + models + '_' + station + '_' + leadtime + 'h.csv'
    return filepath


def read_in_file(filepath):
    df = pd.read_csv(filepath)

    return df


def get_scores_with_significance_mask(df):
    """Reads in the score array and calculates significance array (based on 95% bootstrap interval), which has binary
    entries, 0 for non significant, 1 for significant."""
    scores = df['50.0%-ile'].values
    lower_bound = df['2.5%-ile'].values
    upper_bound = df['97.5%-ile'].values
    # If both upper and lower bound have the same sign (positive or negative), value is significant and mask entry
    # becomes a 1, 0 otherwise
    mask = (np.sign(lower_bound * upper_bound) + 1) / 2

    return scores, mask


def cast_1_d_to_2_d(input):
    """Makes a 2D array out of input

    :params
        input, 1D array, [0 1 ... n]
    returns
        output, 2D array, [[0...n/2-1][n/2...n]]
    """
    nt = len(input) // 2
    output = np.zeros((nt, nt))
    output[0, :] = input[:nt]
    output[1, :] = input[nt:]

    return output


def single_raw_plot(values, ax=None, vmin=-1, vmax=1):
    """Makes a colorplot of the input value without axis ticks.

    :params
        values, 2D array, values between vmin and vmax

    returns
        im, matplotlib image
    """
    if ax is None:
        fig, ax = plt.subplots(1, 1)

    im = ax.imshow(values, vmin=vmin, vmax=vmax, cmap='RdBu_r')
    ax.set_xticks([])
    ax.set_yticks([])

    return im


def single_plot(filepath, ax=None, vmin=-1, vmax=1):
    """From a given filepath, reads in the data, calculates the score array and the statistically significance array
    and plots the values that are significant.

    :params,
        filepath, str, path to file

    """
    if ax is None:
        fig, ax = plt.subplots(1, 1)

    # We have to do try and except here, since some of the raw data was missing, so we do not have the scores for all
    # stations at all lead times
    try:
        df = read_in_file(filepath)
        # get scores array and significance array of these scores, significance is binary
        scores, significance = get_scores_with_significance_mask(df)
    except:
        # If we do not have the data, put scores to zero
        scores = np.zeros(4)
        significance = np.zeros(4)

    # mask the scores with the significance, which is a binary array
    plotting = scores * significance
    plotting_2d = cast_1_d_to_2_d(plotting)
    im = single_raw_plot(plotting_2d, ax=ax, vmin=vmin, vmax=vmax)
    return im


def multiplot(basepath, models, vmin=-1, vmax=1):
    """Make many single plots for every station and lead time in one multiplot.

    :params,
        basepath, str, path to folder with data
        models, str, name of models we are comparing, e.g.'GFS_minus_GSM0p50'
    """

    # list of stations
    stations = ['Ha Noi', 'Ho Chi Minh City', 'Chiang Mai', 'Bangkok', 'Savannakhet', 'Vientiane', 'allstations']
    # list of lead times
    lead_times = ['24', '48', '72', '96', '120']

    fig, ax = plt.subplots(7, 5, figsize=(10, 10))

    for i, station in enumerate(stations):
        for j, leadtime in enumerate(lead_times):

            axis = ax[i, j]
            # make path to file
            filepath = make_file_path(basepath, models, station, leadtime)
            # plot image of scores for this file
            im = single_plot(filepath, ax=axis, vmin=vmin, vmax=vmax)

            # set leadtimes and station names at outer edge of image
            if i == 0:
                axis.set_title(leadtime)
            if j == 0:
                axis.set_ylabel(station, rotation=45, loc="top")

    fig.colorbar(im, ax=ax.ravel().tolist(), orientation="horizontal", shrink=0.7)


def explanatory_plot():
    """Makes a plot that explains which metric is shown where in the single_plot"""
    fig, ax = plt.subplots(1, 1)
    im = single_plot(np.zeros((2, 2)), ax=ax)
    ax.grid()
    ax.text(-0.1, 0, 'ACC', fontsize=20)
    ax.text(0.9, 0, 'HSS', fontsize=20)
    ax.text(-0.1, 1, 'PSS', fontsize=20)
    ax.text(0.9, 1, 'GBS', fontsize=20)
    x = np.linspace(-0.5, 1.5, 10)
    ax.plot(x, x * 0 + 0.5, color='black')
    ax.plot(x * 0 + 0.5, x, color='black')


if __name__ == "__main__":
    basepath = '../../../output_multicat_metricdiffs_1_20/'

    # list of how we compared the models with each other
    model_list = ['GFS_minus_GSM0p50', 'GFS_minus_IFS', 'IFS_minus_GSM0p50']

    # For each model comparison, make one multiplot
    for models in model_list:
        multiplot(basepath, models, vmin=-0.5, vmax=0.5)
        plt.savefig('../Plots/score_plot_{}.pdf'.format(models), bbox_inches='tight')

    # Make a plot that explains how to read the entries in the above plots
    explanatory_plot()
    plt.savefig('../Plots/score_plot_explanatory.pdf', bbox_inches='tight')

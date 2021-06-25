import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data_ingestion_philipp import get_data_as_pandas_df
import tensorflow as tf


def confusion_matrix_plot(y_pred, y_true, title='Confusion Matrix', xlabel='Predicted Label', ylabel='True Label',
                          ax=None):
    """Takes the predictor and true values of a classifier and calculates and plots the confusion matrix of those.
    :parameter
        y_pred, array, length nt, containing the predicted labels
        y_true, array, length nt, containing the true values
    """

    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(6, 5))

    con_mat = tf.math.confusion_matrix(labels=y_true, predictions=y_pred).numpy()
    con_mat_norm = np.around(con_mat.astype('float') / con_mat.sum(axis=1)[:, np.newaxis], decimals=2)
    raw_confusion_matrix_plot(con_mat_norm, ax=ax, title=title, xlabel=xlabel, ylabel=ylabel)


def raw_confusion_matrix_plot(data, ax, title='Confusion Matrix', xlabel='Predicted Label', ylabel='True Label'):
    """Takes data and plots it in the style of a confusion matrix.
    :parameter
        data, 2D array (nx,nx)
    """

    sns.heatmap(data, annot=True, cmap=plt.cm.Blues, ax=ax, vmin=0, vmax=1)
    plt.tight_layout()

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


if __name__ == "__main__":

    # Makes two plots for the confusion matrix by compounding over 24 & 48 hour predictions and 72 & 96 & 120
    projections = [[24, 48], [72, 96, 120], [24, 48, 72, 96, 120]]

    for proj in projections:
        df = get_data_as_pandas_df(projections=proj)
        y_true = df['Observation_bin']
        fig, ax = plt.subplots(1, 3, figsize=(18, 5))

        for i, model in enumerate(['GSM0p50', 'GFS', 'IFS']):
            axis = ax[i]
            y_pred = df[model + '_bin']
            confusion_matrix_plot(y_true=y_true, y_pred=y_pred, ax=axis, title=model, xlabel='Forecast',
                                  ylabel='Observation')

        #plt.show()
        plt.savefig('../Plots/confusion_matrix_{}h.png'.format(proj), bbox_inches='tight')

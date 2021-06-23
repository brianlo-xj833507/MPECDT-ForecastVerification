import matplotlib.pyplot as plt
import pandas as pd

from data_ingestion import read_data

def data_threshold_count(df):

    threshold_bounds = [0.0, 1.0, 5.0, 10.0, 20.0, 30.0, 50.0, 1000.0]
    master_count = pd.DataFrame()
    for idx, threshold in enumerate(threshold_bounds[:-1]):
        this_threshold_count = pd.DataFrame(df[(threshold_bounds[idx] <= df) & (df < threshold_bounds[idx+1])].count(),
                                            columns=[f'{threshold_bounds[idx]} <= x < {threshold_bounds[idx+1]}'])
        master_count = pd.concat([master_count, this_threshold_count], axis=1)

    return master_count
    # df[(0.0 <= df) & (df < 1.0)].count()
    # df[(1.0 <= df) & (df < 5.0)].count()
    # df[(5.0 <= df) & (df < 10.0)].count()
    # df[(10.0 <= df) & (df < 20.0)].count()
    # df[(20.0 <= df) & (df < 30.0)].count()
    # df[(30.0 <= df) & (df < 50.0)].count()
    # df[(50.0 <= df) & (df < 1000.0)].count()


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)

    df_all = read_data()

    # Count all
    df = df_all[['Observation', 'GSM0p50', 'GFS', 'IFS']]

    all_counts = data_threshold_count(df)
    print("All counts")
    print("************")
    print(all_counts)

    ax = all_counts.plot(kind='bar', rot=45)
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.000, p.get_height() * 1.010), rotation=90, fontsize=6)
    plt.legend(prop={'size': 6})
    plt.tight_layout()
    # plt.show()
    plt.savefig("../plots/02_counts_all.pdf")
    plt.clf()

    # Count each station
    station_names = ["Chiang Mai", "Ha Noi", "Ho Chi Minh City", "Bangkok", "Vientiane", "Savannakhet"]
    for station_name in station_names:
        df = df_all.loc[df_all['Name'] == station_name][['Observation', 'GSM0p50', 'GFS', 'IFS']]
        all_counts = data_threshold_count(df)
        print(station_name)
        print("************")
        print(all_counts)
        ax = all_counts.plot(kind='bar', rot=45)
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.000, p.get_height() * 1.010), rotation=90, fontsize=6)
        plt.legend(prop={'size': 6})
        plt.tight_layout()
        plt.savefig(f"../plots/02_counts_{station_name}.pdf")
        plt.clf()
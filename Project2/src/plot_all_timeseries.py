import matplotlib.pyplot as plt

from data_ingestion import read_data

if __name__ == '__main__':

    df = read_data()

    station_names = ["Chiang Mai", "Ha Noi", "Ho Chi Minh City", "Bangkok", "Vientiane", "Savannakhet"]
    lead_times = [24, 48, 72, 96, 120]

    for station_name in station_names:
        for lead_time in lead_times:
            leadtime_subset = df.loc[df.Projection==lead_time]
            leadtime_subset.loc[(leadtime_subset['Name'] == station_name)]['Observation'].plot(color='black', linewidth=0.8)
            leadtime_subset.loc[(leadtime_subset['Name'] == station_name)]['GSM0p50'].plot(linewidth=0.5)
            leadtime_subset.loc[(leadtime_subset['Name'] == station_name)]['IFS'].plot(linewidth=0.5)
            leadtime_subset.loc[(leadtime_subset['Name'] == station_name)]['GFS'].plot(linewidth=0.5)
            plt.legend()
            plt.title(f'{station_name} | Leadtime: {lead_time}h', loc='left')
            plt.savefig(f'../plots/{station_name}_{lead_time}.pdf')
            plt.clf()
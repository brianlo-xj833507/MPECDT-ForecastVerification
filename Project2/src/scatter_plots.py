from data_ingestion_philipp import get_xarray_data
import matplotlib.pyplot as plt

if __name__ == "__main__":
    projections = [24, 48, 72, 96, 120]
    stationids = [48327, 48455, 48820, 48894, 48940, 48947]

    fig, ax = plt.subplots(5, 6, figsize=(50, 50))
    for i, proj in enumerate(projections):
        for j, id in enumerate(stationids):
            axis = ax[i, j]
            df = get_xarray_data(str(proj), str(id))
            df.plot.scatter('Observation', 'GSM0p50', ax = axis)
            df.plot.scatter('Observation', 'GFS', ax = axis)
            df.plot.scatter('Observation', 'IFS', ax = axis)
    plt.show()
    # plt.savefig('scatter_stid-48820_h_24.pdf', bbox_inches = 'tight')

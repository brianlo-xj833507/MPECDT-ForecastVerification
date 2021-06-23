"""Plots all station locations on a map"""

import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy

import numpy as np
import pandas as pd
import cartopy
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt


def main():
    # Station Information
    station_info = pd.DataFrame(np.array(
        [[48327, "Chiang Mai", 18.783, 98.983],
         [48820, "Ha Noi", 21.017, 105.800],
         [48894, "Ho Chi Minh City", 10.650, 106.717],
         [48455, "Bangkok", 13.733, 100.567],
         [48940, "Vientiane", 17.950, 102.567],
         [48947, "Savannakhet", 13.550, 104.650]]),
        columns=['StationID', 'Name', 'Lat', 'Lon'])

    new_dtypes = {"StationID": int, "Name": 'string', "Lat": np.float32, "Lon": np.float32}
    station_info = station_info.astype(new_dtypes)
    station_info = station_info.set_index(['StationID'])

    # Create a Stamen Terrain instance.
    stamen_terrain = cimgt.StamenTerrain('terrain-background')

    # Create a GeoAxes in the tile's projection.
    ax = plt.axes(projection=stamen_terrain.crs)

    # Limit the extent of the map to a small longitude/latitude range.
    ax.set_extent([97.0, 112.0, 8.0, 23.0])

    # Add the Stamen data at zoom level 8.
    ax.add_image(stamen_terrain, 10)

    # Coastline and country borders
    ax.coastlines('10m', linewidth=0.75)
    ax.add_feature(cartopy.feature.BORDERS, color='grey', linewidth=0.5)

    # Add a marker for the Eyjafjallajökull volcano.
    for idx, station_data in station_info.iterrows():
        plt.plot(station_data['Lon'], station_data['Lat'], marker='o', color='red', markersize=4,
                 alpha=0.8, transform=ccrs.Geodetic())

    # Use the cartopy interface to create a matplotlib transform object
    # for the Geodetic coordinate system. We will use this along with
    # matplotlib's offset_copy function to define a coordinate system which
    # translates the text by 25 pixels to the left.
    geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
    text_transform = offset_copy(geodetic_transform, units='dots', x=0, y=-10)

    # Add text 25 pixels to the left of the volcano.
    for idx, station_data in station_info.iterrows():
        plt.text(station_data['Lon'], station_data['Lat'], station_data['Name'],
                 verticalalignment='top', horizontalalignment='left', fontsize=8,
                 transform=text_transform,
                 bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
    plt.savefig('../plots/00_station_map.pdf')


if __name__ == '__main__':
    main()
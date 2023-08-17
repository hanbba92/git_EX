import numpy as np

from matplotlib.ticker import MaxNLocator
from itertools import product
from netCDF4 import Dataset as dataset
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import io
import numpy as np
import os
output_folder='D:/apihub/gradient_png'
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
def plot(input_file_path,low,high,hour):
    fig = plt.figure(figsize=(20, 10))
    plt.suptitle('Gradient Descent Method', fontsize=20)
    nc = dataset(input_file_path)
    lat = nc['INPUTDATA'].variables['latitude'][:]
    lon = nc['INPUTDATA'].variables['longitude'][:]

    t2 = nc['INPUTDATA'].variables['PRMSL'][:]
    t2=t2
    ax = fig.add_subplot(111)
    ax.set_title("path")
    m = Basemap(projection='cyl', llcrnrlon=100, llcrnrlat=15, urcrnrlon=165, urcrnrlat=55, resolution='i')
    # x, y = m(*np.meshgrid(lon,lat))
    #print(t2[0, :, :])
    cs = m.contourf(lat, lon,t2[hour,:,:])
    cs = m.contour(lon, lat, t2[hour, :, :], latlon=True, colors='black', )
    cs2 = m.contourf(lon, lat, t2[hour, :, :], latlon=True, cmap=get_cmap("jet"), alpha=0.8)
    plt.clabel(cs, colors='black', inline=True, fontsize=12, fmt='%1.0f')
    m.drawcoastlines()
    m.drawmapboundary()
    m.drawcountries(linewidth=1, linestyle='solid', color='k')
    m.drawmeridians(range(33, 48, 2), color='k', linewidth=1.0, dashes=[4, 4], labels=[0, 0, 0, 1])
    m.drawparallels(range(3, 15, 2), color='k', linewidth=1.0, dashes=[4, 4], labels=[1, 0, 0, 0])
    plt.ylabel("Latitude", fontsize=15, labelpad=35)
    plt.xlabel("Longitude", fontsize=15, labelpad=20)
    cbar = m.colorbar(cs2, location='right', pad="3%")
    cbar.set_label('unit : mb', fontsize=13)
    plt.title('                   Air Pressure Reduced to Sea Level            ' +input_file_path[-13:-3]+'h%3.3d'%(hour*3), fontsize=13)

    # tmp_lat,tmp_lon=[],[]
    # for iy,ix in xs:
    #
    #     tmp_lat.append(lat[iy,ix])
    #     tmp_lon.append(lon[iy,ix])
    low_lat,low_lon=[],[]
    for iy,ix in low:
        low_lat.append(lat[iy, ix])
        low_lon.append(lon[iy,ix])
    high_lat, high_lon = [], []
    for iy, ix in high:
        high_lat.append(lat[iy, ix])
        high_lon.append(lon[iy, ix])

    # m.plot(tmp_lon, tmp_lat, linestyle='--', marker='o', color='red')
    # m.plot(tmp_lon[0], tmp_lat[0], 'ro', color='blue')
    # m.plot(tmp_lon[-1], tmp_lat[-1], marker='o', color='black')

    m.plot(low_lon, low_lat, 'ro', color='blue', label='LOW')
    m.plot(high_lon, high_lat, 'ro', color='red', label='HIGH')

    ax.legend(loc=1)

    # m.plot(tmp_lon, tmp_lat, linestyle='--', marker='o', color='red')
    # m.plot(tmp_lon[0], tmp_lat[0], 'ro', color='blue')
    # m.plot(tmp_lon[-1], tmp_lat[-1], marker='o', color='black')


    # ax = fig.add_subplot(122)
    #
    # ax.plot(ys, linestyle='--', marker='o', color='orange')
    # ax.plot(len(ys)-1, ys[-1], 'ro')
    # ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # ax.set(
    #     title='Objective Function Value During Optimization Process',
    #     xlabel='Iterations',
    #     ylabel='Objective Function Value'
    # )
    #ax.legend(['Gradient Descent Search Algorithm'])
    #
    plt.tight_layout()
    plt.savefig('{}.png'.format(output_folder + '/' + input_file_path[-13:-3]+'h%3.3d'%(hour*3)), format='png')
    #plt.show()
    nc.close()
    #plt.close('all')
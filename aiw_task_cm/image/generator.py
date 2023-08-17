from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.colors as mcl
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
import matplotlib
import numpy as np
import pkg_resources
import copy
import os
from shapefile import Reader
import time


def readshapefile(shapefile, default_encoding='utf-8'):
    shf = Reader(shapefile, encoding=default_encoding)
    coordslatlon = []

    for shprec in shf.shapeRecords():
        verts = np.array(shprec.shape.points)
        parts = shprec.shape.parts.tolist()
        for indx1, indx2 in zip(parts, parts[1:] + [len(verts)]):
            coordslatlon.append((verts[indx1:indx2].transpose((1, 0))))

    return coordslatlon


def drawshapefile(coordslatlons, ax, map_, linewidth=0.5, color='k'):
    coords = []
    coords_raw = np.column_stack(map_(*np.hstack(coordslatlons)))
    idx = 0
    for i in coordslatlons:
        coords_len = len(i[0])
        coords.append(coords_raw[idx:idx + coords_len])
        idx += coords_len

    lines = LineCollection(coords, antialiaseds=(1,))
    lines.set_color(color)
    lines.set_linewidth(linewidth)
    lines.set_label('_nolabel_')
    ax.add_collection(lines)
    map_.set_axes_limits(ax=ax)


shapefile_path = pkg_resources.resource_filename(__name__, "../metadata/sig_wgs84")
shpcoords = readshapefile(shapefile_path, default_encoding="euc-kr")


def generate(data, lat, lon, title=None, minv=None, maxv=None, unit=None, urcrnrlat=None, urcrnrlon=None,
             llcrnrlat=None, llcrnrlon=None, colorIndex=None, colorType=1, save=None, map_=None):
    # set font
    font = {'size': 15}
    matplotlib.rc('font', **font)

    # set masked array
    if type(data) != np.ma.masked_array:
        data = np.ma.masked_array(data)

    # set plot type
    if len(data.shape) == 1:
        draw_scatter = True
        draw_map = False
    elif len(data.shape) == 2:
        draw_scatter = False
        draw_map = True
    else:
        raise Exception(f"data shape must be 1d or 2d array but {data.shape}")

    # set title
    is_title = False
    if title is not None and type(title) == str:
        is_title = True

    # set unit
    is_unit = False
    if unit is not None and type(unit) == str:
        is_unit = True

    # set data range
    if minv is None:
        minv = np.nanmin(data)
    if maxv is None:
        maxv = np.nanmax(data)

    # set region
    if None in [urcrnrlat, urcrnrlon, llcrnrlat, llcrnrlon]:
        urcrnrlat = np.nanmax(lat)
        urcrnrlon = np.nanmax(lon)
        llcrnrlon = np.nanmin(lon)
        llcrnrlat = np.nanmin(lat)

    # check geophysical data
    checklat = (lat > 180) | (lat < -180)
    checklon = (lon > 360) | (lon < -360)
    if len(lat[checklat]) > 0:
        lat[checklat] = max(np.nanmin(lat[~checklat]) - 1, -90)
    if len(lon[checklon]) > 0:
        lon[checklon] = max(np.nanmin(lon[~checklon]) - 1, -360)

    if not data.shape == lat.shape == lon.shape:
        raise Exception(f"data, lat, lon shape must be same but data: {data.shape}, lat: {lat.shape}, lon:{lon.shape}")

    # set colorIndex
    if colorIndex is None or len(colorIndex) == 0:
        colorIndex = [[ 68.08602 ,   1.24287 ,  84.000825],
                      [ 72.18336 ,  33.378225, 114.556455],
                      [ 66.84519 ,  61.78293 , 132.813435],
                      [ 56.114535,  87.543285, 140.100315],
                      [ 45.242865, 111.569385, 142.179075],
                      [ 36.552465, 133.307115, 141.855225],
                      [ 30.47556 , 154.90332 , 137.75559 ],
                      [ 42.427665, 176.16828 , 126.60801 ],
                      [ 81.551295, 196.58307 , 104.84376 ],
                      [134.07288 , 212.540205,  73.472385],
                      [194.405115, 223.48812 ,  34.95132 ],
                      [253.27824 , 231.070035,  36.70368 ]]
    elif len(colorIndex) == 1:
        colorIndex = [colorIndex[0], colorIndex[0]]

    # set cmap
    cmap = None
    if colorIndex is not None and len(colorIndex) > 0:
        colors = [[r/255, g/255, b/255] for [r, g, b] in colorIndex]
        cmap = mcl.LinearSegmentedColormap.from_list('my_cmap', colors, gamma=1)

    # set colorbar and legend
    is_colorbar = False
    is_legend = False
    if colorType == 'colorbar' or colorType == 1:
        is_colorbar = True
        is_legend = False
        colormapping = cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=minv, vmax=maxv), cmap=cmap)
    elif colorType == 'legend' or colorType == 2:
        is_colorbar = False
        is_legend = True
        patches = [mpatches.Patch(color=colors[0], label=minv)]
        if len(colors) > 1:
            getcolorv = lambda minv, maxv, colors, i: minv + (maxv - minv) / (len(colors) - 1) * (i + 1)
            fixcolorv = lambda v: v if abs(v - round(v)) > 1e-7 else round(v)
            patches += [mpatches.Patch(color=color, label=fixcolorv(getcolorv(minv, maxv, colors, i))) for i, color in enumerate(colors[1:-1])]
            patches += [mpatches.Patch(color=colors[-1], label=maxv)]

    is_save = False
    if save is not None:
        is_save = True
        if len(os.path.dirname(save)) != 0 and not os.path.isdir(os.path.dirname(save)):
            raise Exception(f"save path is not exist: {save}")

    # draw map
    if map_ is not None:
        map = copy.copy(map_)
    else:
        map = Basemap(projection='merc', resolution='h', urcrnrlat=urcrnrlat, urcrnrlon=urcrnrlon, llcrnrlat=llcrnrlat,
                      llcrnrlon=llcrnrlon)

    # draw data
    fig = plt.figure(figsize=(10, 11), clear=True)
    ax = plt.gca()
    drawshapefile(shpcoords, ax, map)
    map.drawcoastlines()

    if draw_scatter:
        plt.scatter(*map(lon, lat), c=data, cmap=cmap, vmin=minv, vmax=maxv)
    if draw_map:
        map.pcolormesh(*map(lon, lat), data, cmap=cmap, vmin=minv, vmax=maxv)

    # draw title
    if is_title:
        plt.title(title, fontsize=20)

    # draw colorbar and legend
    if is_colorbar:
        if is_unit:
            plt.colorbar(colormapping, label=unit, ax=plt.gca(), fraction=0.055, pad=0.04)
        else:
            plt.colorbar(colormapping, ax=plt.gca(), fraction=0.055, pad=0.04)
    elif is_legend:
        plt.legend(handles=patches)

    if is_save:
        plt.savefig(save, pad_inches=0.1, bbox_inches='tight')


if __name__=="__main__":
    np.random.seed(1)
    lats = np.linspace(39, 30, 300)
    lons = np.linspace(125, 130, 300)
    map_ = Basemap(projection='merc', resolution='h', urcrnrlat=39, urcrnrlon=130, llcrnrlon=125, llcrnrlat=30)

    data = np.random.randint(3, size=300)
    lat = lats[np.random.randint(300, size=300)]
    lon = lons[np.random.randint(300, size=300)]

    now = time.time()
    generate(data, lat, lon, save="1.png", map_=map_, colorIndex=[[255, 0, 0], [0, 255, 0], [0, 0, 255]], colorType=1, minv=0, maxv=2)
    print(time.time() - now); now = time.time()
    generate(data, lat, lon, save="2.png", map_=map_, colorIndex=[[255, 0, 0], [0, 255, 0], [0, 0, 255]], colorType=2, minv=0, maxv=2)
    print(time.time() - now); now = time.time()

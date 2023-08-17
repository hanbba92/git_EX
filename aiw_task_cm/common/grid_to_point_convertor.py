import numpy as np
import pkg_resources
from aiw_task_cm.file.file_manager_factory import FileManagerFactory


def grid_to_points(latitude, longitude):
    """
    격자 자료를 지점 자료로 변경
    :param latitude: latitude 2d array
    :param longitude: longitude 2d array
    :param vgrd: vvv-wind grid values
    :param ugrd: uuu-wind grid values
    :return: codes, latitude, longitude, points, vvv-wind values, uuu-wind values
    """
    latlon_config_path = pkg_resources.resource_filename(__name__, '../metadata/codes_latlon.csv')
    fm = FileManagerFactory().get_instance('csv')
    points_config = fm.read(latlon_config_path)
    pixels = []
    codes = []
    points = []

    for aws_code in points_config:
        pixel = convert_latlon_to_pixel(latitude, longitude, float(aws_code['위도']), float(aws_code['경도']))
        pixels.append(pixel)
        points.append(int(float(aws_code['지점'])))
        codes.append(aws_code['지점명'])

    return codes, pixels, points


def convert_latlon_to_pixel(lats, lons, lat, lon):
    """
    convert lat lon to pixel
    :param lats: latitude 2d list
    :param lons: longitude 2d list
    :param lat: latitude
    :param lon: longitude
    :return: pixel
    """
    array = np.sqrt((lats - lat) ** 2 + (lons - lon) ** 2)
    min = np.min(array)
    pixel_by = np.where(array == min)
    pixel = [pixel_by[0][0], pixel_by[1][0]]
    return pixel

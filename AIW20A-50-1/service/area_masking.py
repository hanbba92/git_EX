import numpy as np


def get_location_result_list(latitude, longitude ,location_data):
    '''
    위치 정보에 맞게 해당 영역을 masking하는 함수
    :param latitude: 위도값 배열
    :param longitude: 경도값 배열
    :param location_data: 위치 정보
    :return:
    '''
    # 경도 계산
    longitude_max_base = np.array(location_data['lon']).max()
    longitude_min_base = np.array(location_data['lon']).min()
    longitude_result = np.logical_and(longitude <= longitude_max_base, longitude >= longitude_min_base)

    # 위도 계산
    latitude_max_base = np.array(location_data['lat']).max()
    latitude_min_base = np.array(location_data['lat']).min()
    latitude_result = np.logical_and(latitude <= latitude_max_base, latitude >= latitude_min_base)

    location_result = np.logical_and(longitude_result, latitude_result)

    return location_result

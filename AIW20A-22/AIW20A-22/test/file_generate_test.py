import unittest

import numpy as np
from netCDF4 import Dataset

from aiw_task_cm.file.file_manager_factory import FileManagerFactory

class FileGenerateTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fm = FileManagerFactory().get_instance('netcdf')

    def read(self, input_file):
        data = {
            'tmp_925': self.read_task_values(input_file, 'FLOWDATA/22/values'),
            'cin': self.read_task_values(input_file, 'FLOWDATA/22/values'),
            'southwest': self.read_task_values(input_file, 'FLOWDATA/22/values'),
            'latitude': self.read_task_values(input_file, 'INPUTDATA/latitude'),
            'longitude': self.read_task_values(input_file, 'INPUTDATA/longitude')
        }
        return data

    def read_task_values(self, input_file, data_path):
        path = data_path
        task2_values, meta = self.fm.read(input_file, data_path=path)
        return task2_values

    def test_file_generate(self):
        titles = ['tmp_925', 'cin', 'southwest']  # 사용할 데이터 목록

        ds = Dataset('/Users/user/Desktop/netcdf/aiw_task22_input_20220207.nc', 'w', format="NETCDF4")  # 새 nc파일 생성

        data1 = self.read('/Users/user/Desktop/netcdf/aiw_task22_tmp_input_20220207.nc')
        data2 = self.read('/Users/user/Desktop/netcdf/aiw_task22_cin_input_20220207.nc')
        data3 = self.read('/Users/user/Desktop/netcdf/aiw_task22_southwest_input_20220207.nc')

        lats = np.array(data1['latitude'])
        lons = np.array(data1['longitude'])

        # 차원 생성
        ds.createDimension('latitude', np.array(data1['tmp_925'])[:, :].shape[0])
        ds.createDimension('longitude', np.array(data1['tmp_925'])[:, :].shape[1])

        # 데이터 저장할 변수 공간 생성
        ds.createVariable('INPUTDATA/latitude', 'f8', 'latitude')
        ds.createVariable('INPUTDATA/longitude', 'f8', 'longitude')

        # 변수에 데이터 저장
        ds['INPUTDATA/latitude'][:] = lats
        ds['INPUTDATA/longitude'][:] = lons

        values = np.array(data1['tmp_925'])[:, :] #[1100:1500, 700:1100]
        ds.createVariable('INPUTDATA/' + 'tmp_925' + '/h000', float, ('latitude', 'longitude'))  # 변수공간 생성
        ds['INPUTDATA/' + 'tmp_925' + '/h000'][:, :] = values

        values = np.array(data2['cin'])[:, :]
        ds.createVariable('INPUTDATA/' + 'cin' + '/h000', float, ('latitude', 'longitude'))
        ds['INPUTDATA/' + 'cin' + '/h000'][:, :] = values

        values = np.array(data3['southwest'])[:, :]
        ds.createVariable('INPUTDATA/' + 'southwest' + '/h000', float, ('latitude', 'longitude'))
        ds['INPUTDATA/' + 'southwest' + '/h000'][:, :] = values

        ds.close()
import unittest

import numpy as np
from netCDF4 import Dataset

from aiw_task_cm.file.file_manager_factory import FileManagerFactory

class FileGenerateTest(unittest.TestCase):

    def __init__(self):
        self.fm = FileManagerFactory().get_instance('netcdf')

    def read(self, input_file):
        data = {
            'u_wind': self.read_task_values(input_file, '/UGRD_850mb'),
            'v_wind': self.read_task_values(input_file, '/VGRD_850mb'),
            'latitude': self.read_task_values(input_file, '/latitude'),
            'longitude': self.read_task_values(input_file, '/longitude')
        }
        return data

    def read_task_values(self, input_file, data_path):
        path = data_path
        task2_values, meta = self.fm.read(input_file, data_path=path)
        return task2_values

    def test_file_generate(self):
        titles = ['u_wind', 'v_wind'] #사용할 데이터 목록

        ds = Dataset('aiw_task18_input_20220207.nc', 'w', format="NETCDF4") #새 nc파일 생성

        data = self.read('/Users/user/Desktop/gdaps/g128_v070_ergl_pres_h000.2022020700.nc') #등압면 데이터
        lats = np.array(data['latitude'])[1100:1500]
        lons = np.array(data['longitude'])[700:1100] #사용할 범위

        # 차원 생성
        ds.createDimension('latitude', np.array(data[titles[0]])[0][1100:1500, 700:1100].shape[0])
        ds.createDimension('longitude', np.array(data[titles[0]])[0][1100:1500, 700:1100].shape[1])

        # 데이터 저장할 변수 공간 생성
        ds.createVariable('INPUTDATA/latitude', 'f8', 'latitude')
        ds.createVariable('INPUTDATA/longitude', 'f8', 'longitude')

        # 변수에 데이터 저장
        ds['INPUTDATA/latitude'][:] = lats
        ds['INPUTDATA/longitude'][:] = lons
        for title in titles:
            values = np.array(data[title])[0][1100:1500, 700:1100]

            ds.createVariable('INPUTDATA/'+title+'/h000', float,
                              ('latitude', 'longitude'))

            ds['INPUTDATA/'+title+'/h000'][:, :] = values
        ds.close()
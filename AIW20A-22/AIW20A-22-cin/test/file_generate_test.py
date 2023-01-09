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
            'tmp_600': self.read_task_values(input_file, '/TMP_600mb'),
            'tmp_700': self.read_task_values(input_file, '/TMP_700mb'),
            'tmp_850': self.read_task_values(input_file, '/TMP_850mb'),
            'tmp_925': self.read_task_values(input_file, '/TMP_925mb'),
            'tmp_950': self.read_task_values(input_file, '/TMP_950mb'),
            'tmp_1000': self.read_task_values(input_file, '/TMP_1000mb'),
            'rh_600': self.read_task_values(input_file, '/data'),
            'rh_700': self.read_task_values(input_file, '/data'),
            'rh_850': self.read_task_values(input_file, '/data'),
            'rh_925': self.read_task_values(input_file, '/data'),
            'rh_950': self.read_task_values(input_file, '/data'),
            'rh_1000': self.read_task_values(input_file, '/data'),
            'latitude': self.read_task_values(input_file, '/latitude'),
            'longitude': self.read_task_values(input_file, '/longitude')
        }
        return data

    def read_task_values(self, input_file, data_path):
        path = data_path
        task2_values, meta = self.fm.read(input_file, data_path=path)
        return task2_values

    def test_file_generate(self):
        tmp_titles = ['tmp_600', 'tmp_700', 'tmp_850', 'tmp_925', 'tmp_950', 'tmp_1000']
        rh_titles = ['rh_600', 'rh_700', 'rh_850', 'rh_925', 'rh_950', 'rh_1000']  # 사용할 데이터 목록

        ds = Dataset('/Users/user/Desktop/netcdf/aiw_task22_cin_input_20220207.nc', 'w', format="NETCDF4")  # 새 nc파일 생성

        data1 = self.read('/Users/user/Desktop/gdaps/g128_v070_ergl_pres_h000.2022020700.nc')  # 등압면 데이터 -> tmp 600 ~1000
        data600 = self.read('/Users/user/Desktop/GDAPS_UM_RH/g128_v070_ergl_pres_h000.2022020700.gb2__RH_600.nc')  #600hPa에서 rh
        data700 = self.read('/Users/user/Desktop/GDAPS_UM_RH/g128_v070_ergl_pres_h000.2022020700.gb2__RH_700.nc')
        data850 = self.read('/Users/user/Desktop/GDAPS_UM_RH/g128_v070_ergl_pres_h000.2022020700.gb2__RH_850.nc')
        data925 = self.read('/Users/user/Desktop/GDAPS_UM_RH/g128_v070_ergl_pres_h000.2022020700.gb2__RH_925.nc')
        data950 = self.read('/Users/user/Desktop/GDAPS_UM_RH/g128_v070_ergl_pres_h000.2022020700.gb2__RH_950.nc')
        data1000 = self.read('/Users/user/Desktop/GDAPS_UM_RH/g128_v070_ergl_pres_h000.2022020700.gb2__RH_1000.nc')

        lats = np.array(data1['latitude'])[1100:1500]
        lons = np.array(data1['longitude'])[700:1100]  # 사용할 범위 지정

        # 차원 생성
        ds.createDimension('latitude', np.array(data1[tmp_titles[0]])[0][1100:1500, 700:1100].shape[0])
        ds.createDimension('longitude', np.array(data1[tmp_titles[0]])[0][1100:1500, 700:1100].shape[1])

        # 데이터 저장할 변수 공간 생성
        ds.createVariable('INPUTDATA/latitude', 'f8', 'latitude')
        ds.createVariable('INPUTDATA/longitude', 'f8', 'longitude')

        # 변수에 데이터 저장
        ds['INPUTDATA/latitude'][:] = lats
        ds['INPUTDATA/longitude'][:] = lons

        for title in tmp_titles:
            values = np.array(data1[title])[0][1100:1500, 700:1100]

            ds.createVariable('INPUTDATA/'+title+'/h000', float,
                              ('latitude', 'longitude'))

            ds['INPUTDATA/'+title+'/h000'][:, :] = values

        values = np.array(data600['rh_600'])[1100:1500, 700:1100]
        ds.createVariable('INPUTDATA/' + 'rh_600' + '/h000', float, ('latitude', 'longitude'))
        ds['INPUTDATA/' + 'rh_600' + '/h000'][:, :] = values

        values = np.array(data700['rh_700'])[1100:1500, 700:1100]
        ds.createVariable('INPUTDATA/' + 'rh_700' + '/h000', float, ('latitude', 'longitude'))
        ds['INPUTDATA/' + 'rh_700' + '/h000'][:, :] = values

        values = np.array(data850['rh_850'])[1100:1500, 700:1100]
        ds.createVariable('INPUTDATA/' + 'rh_850' + '/h000', float, ('latitude', 'longitude'))
        ds['INPUTDATA/' + 'rh_850' + '/h000'][:, :] = values

        values = np.array(data925['rh_925'])[1100:1500, 700:1100]
        ds.createVariable('INPUTDATA/' + 'rh_925' + '/h000', float, ('latitude', 'longitude'))
        ds['INPUTDATA/' + 'rh_925' + '/h000'][:, :] = values

        values = np.array(data950['rh_950'])[1100:1500, 700:1100]
        ds.createVariable('INPUTDATA/' + 'rh_950' + '/h000', float, ('latitude', 'longitude'))
        ds['INPUTDATA/' + 'rh_950' + '/h000'][:, :] = values

        values = np.array(data1000['rh_1000'])[1100:1500, 700:1100]
        ds.createVariable('INPUTDATA/' + 'rh_1000' + '/h000', float, ('latitude', 'longitude'))
        ds['INPUTDATA/' + 'rh_1000' + '/h000'][:, :] = values

        ds.close()
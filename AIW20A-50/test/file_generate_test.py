import unittest
from aiw_task_cm.file.file_manager_factory import FileManagerFactory
import numpy as np
from netCDF4 import Dataset


class FileGenerateTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.fm = FileManagerFactory().get_instance('netcdf')

    def read_pres(self, input_file):
        data = {
            'latitude': self.read_task_values(input_file, '/latitude'),
            'longitude': self.read_task_values(input_file, '/longitude')
        }
        return data

    def read_task_values(self, input_file, data_path):
        path = data_path
        data, meta = self.fm.read(input_file, data_path=path)
        return data

    def test_file_generate(self):

        ds = Dataset('C:/Users/user/Desktop/netcdf/aiw_task_hr_43_input.nc', 'w', format="NETCDF4")
        times = ['h000', 'h003', 'h006', 'h009', 'h012', 'h015', 'h018', 'h021']
        result = self.read_pres('C:/Users/user/Desktop/netcdf/r120v070ereapresh003.2018091212.gb2.nc')


        lats = np.array(result['latitude'])
        lons = np.array(result['longitude'])

        # 차원생성
        ds.createDimension('latitude', lats.shape[0])
        ds.createDimension('longitude', lons.shape[1])
        ds.createDimension('times', len(times))

        # 데이터 저장할 변수 공간 생성
        ds.createVariable('INPUTDATA/latitude', 'f8', ('latitude', 'longitude'))
        ds.createVariable('INPUTDATA/longitude', 'f8', ('latitude', 'longitude'))
        ds.createVariable('INPUTDATA/times', 'str', 'times')

        # 변수에 데이터 저장
        ds['INPUTDATA/latitude'][:] = lats[:, :]
        ds['INPUTDATA/longitude'][:] = lons[:, :]
        ds['INPUTDATA/times'][:] = np.array(times)
        ds.close()


def main():
    file_gen = FileGenerateTest()
    file_gen.test_file_generate()


if __name__ == '__main__':
    main()
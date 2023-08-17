import unittest
from aiw_task_cm.file.file_manager_factory import FileManagerFactory
import numpy as np
from netCDF4 import Dataset
import datetime
import os
import subprocess


class FileGenerateTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.fm = FileManagerFactory().get_instance('netcdf')

    def read_data(self, input_file):
        data = {
            'TMP_100mb': self.read_task_values(input_file, '/TMP_100mb'),
            'RH_100mb': self.read_task_values(input_file, '/RH_100mb'),
            'TMP_150mb': self.read_task_values(input_file, '/TMP_150mb'),
            'RH_150mb': self.read_task_values(input_file, '/RH_150mb'),
            'TMP_200mb': self.read_task_values(input_file, '/TMP_200mb'),
            'RH_200mb': self.read_task_values(input_file, '/RH_200mb'),
            'TMP_250mb': self.read_task_values(input_file, '/TMP_250mb'),
            'RH_250mb': self.read_task_values(input_file, '/RH_250mb'),
            'TMP_300mb': self.read_task_values(input_file, '/TMP_300mb'),
            'RH_300mb': self.read_task_values(input_file, '/RH_300mb'),
            'TMP_350mb': self.read_task_values(input_file, '/TMP_350mb'),
            'RH_350mb': self.read_task_values(input_file, '/RH_350mb'),
            'TMP_400mb': self.read_task_values(input_file, '/TMP_400mb'),
            'RH_400mb': self.read_task_values(input_file, '/RH_400mb'),
            'TMP_450mb': self.read_task_values(input_file, '/TMP_450mb'),
            'RH_450mb': self.read_task_values(input_file, '/RH_450mb'),
            'TMP_500mb': self.read_task_values(input_file, '/TMP_500mb'),
            'RH_500mb': self.read_task_values(input_file, '/RH_500mb'),
            'TMP_600mb': self.read_task_values(input_file, '/TMP_600mb'),
            'RH_600mb': self.read_task_values(input_file, '/RH_600mb'),
            'TMP_700mb': self.read_task_values(input_file, '/TMP_700mb'),
            'RH_700mb': self.read_task_values(input_file, '/RH_700mb'),
            'TMP_950mb': self.read_task_values(input_file, '/TMP_950mb'),
            'RH_950mb': self.read_task_values(input_file, '/RH_950mb'),
            'TMP_1000mb': self.read_task_values(input_file, '/TMP_1000mb'),
            'RH_1000mb': self.read_task_values(input_file, '/RH_1000mb'),
            'DZDT_50mb': self.read_task_values(input_file, '/DZDT_50mb'),
            'DZDT_70mb': self.read_task_values(input_file, '/DZDT_70mb'),
            'DZDT_100mb': self.read_task_values(input_file, '/DZDT_100mb'),
            'DZDT_150mb': self.read_task_values(input_file, '/DZDT_150mb'),
            'DZDT_200mb': self.read_task_values(input_file, '/DZDT_200mb'),
            'DZDT_250mb': self.read_task_values(input_file, '/DZDT_250mb'),
            'DZDT_300mb': self.read_task_values(input_file, '/DZDT_300mb'),
            'DZDT_350mb': self.read_task_values(input_file, '/DZDT_350mb'),
            'DZDT_400mb': self.read_task_values(input_file, '/DZDT_400mb'),
            'DZDT_450mb': self.read_task_values(input_file, '/DZDT_450mb'),
            'DZDT_500mb': self.read_task_values(input_file, '/DZDT_500mb'),
            'DZDT_550mb': self.read_task_values(input_file, '/DZDT_550mb'),
            'DZDT_600mb': self.read_task_values(input_file, '/DZDT_600mb'),
            'DZDT_650mb': self.read_task_values(input_file, '/DZDT_650mb'),
            'DZDT_700mb': self.read_task_values(input_file, '/DZDT_700mb'),
            'DZDT_750mb': self.read_task_values(input_file, '/DZDT_750mb'),
            'DZDT_800mb': self.read_task_values(input_file, '/DZDT_800mb'),
            'DZDT_850mb': self.read_task_values(input_file, '/DZDT_850mb'),
            'DZDT_875mb': self.read_task_values(input_file, '/DZDT_875mb'),
            'DZDT_900mb': self.read_task_values(input_file, '/DZDT_900mb'),
            'DZDT_925mb': self.read_task_values(input_file, '/DZDT_925mb'),
            'DZDT_950mb': self.read_task_values(input_file, '/DZDT_950mb'),
            'DZDT_975mb': self.read_task_values(input_file, '/DZDT_975mb'),
            'DZDT_1000mb': self.read_task_values(input_file, '/DZDT_1000mb'),
            'UGRD_200mb': self.read_task_values(input_file, '/UGRD_200mb'),
            'VGRD_200mb': self.read_task_values(input_file, '/VGRD_200mb'),
            'UGRD_250mb': self.read_task_values(input_file, '/UGRD_250mb'),
            'VGRD_250mb': self.read_task_values(input_file, '/VGRD_250mb'),
            'UGRD_300mb': self.read_task_values(input_file, '/UGRD_300mb'),
            'VGRD_300mb': self.read_task_values(input_file, '/VGRD_300mb'),
            'UGRD_350mb': self.read_task_values(input_file, '/UGRD_350mb'),
            'VGRD_350mb': self.read_task_values(input_file, '/VGRD_350mb'),
            'UGRD_400mb': self.read_task_values(input_file, '/UGRD_400mb'),
            'VGRD_400mb': self.read_task_values(input_file, '/VGRD_400mb'),
            'UGRD_450mb': self.read_task_values(input_file, '/UGRD_450mb'),
            'VGRD_450mb': self.read_task_values(input_file, '/VGRD_450mb'),
            'UGRD_500mb': self.read_task_values(input_file, '/UGRD_500mb'),
            'VGRD_500mb': self.read_task_values(input_file, '/VGRD_500mb'),
            'UGRD_550mb': self.read_task_values(input_file, '/UGRD_550mb'),
            'VGRD_550mb': self.read_task_values(input_file, '/VGRD_550mb'),
            'UGRD_600mb': self.read_task_values(input_file, '/UGRD_600mb'),
            'VGRD_600mb': self.read_task_values(input_file, '/VGRD_600mb'),
            'UGRD_650mb': self.read_task_values(input_file, '/UGRD_650mb'),
            'VGRD_650mb': self.read_task_values(input_file, '/VGRD_650mb'),
            'UGRD_700mb': self.read_task_values(input_file, '/UGRD_700mb'),
            'VGRD_700mb': self.read_task_values(input_file, '/VGRD_700mb'),
            'UGRD_750mb': self.read_task_values(input_file, '/UGRD_750mb'),
            'VGRD_750mb': self.read_task_values(input_file, '/VGRD_750mb'),
            'UGRD_800mb': self.read_task_values(input_file, '/UGRD_800mb'),
            'VGRD_800mb': self.read_task_values(input_file, '/VGRD_800mb'),
            'UGRD_850mb': self.read_task_values(input_file, '/UGRD_850mb'),
            'VGRD_850mb': self.read_task_values(input_file, '/VGRD_850mb'),
            'UGRD_875mb': self.read_task_values(input_file, '/UGRD_875mb'),
            'VGRD_875mb': self.read_task_values(input_file, '/VGRD_875mb'),
            'UGRD_900mb': self.read_task_values(input_file, '/UGRD_900mb'),
            'VGRD_900mb': self.read_task_values(input_file, '/VGRD_900mb'),
            'UGRD_925mb': self.read_task_values(input_file, '/UGRD_925mb'),
            'VGRD_925mb': self.read_task_values(input_file, '/VGRD_925mb'),
            'UGRD_950mb': self.read_task_values(input_file, '/UGRD_950mb'),
            'VGRD_950mb': self.read_task_values(input_file, '/VGRD_950mb'),
            'UGRD_975mb': self.read_task_values(input_file, '/UGRD_975mb'),
            'VGRD_975mb': self.read_task_values(input_file, '/VGRD_975mb'),
            'UGRD_1000mb': self.read_task_values(input_file, '/UGRD_1000mb'),
            'VGRD_1000mb': self.read_task_values(input_file, '/VGRD_1000mb'),
            'RH_850mb': self.read_task_values(input_file, '/RH_850mb'),
            'TMP_850mb': self.read_task_values(input_file, '/TMP_850mb'),
            'RH_925mb': self.read_task_values(input_file, '/RH_925mb'),
            'TMP_925mb': self.read_task_values(input_file, '/TMP_925mb'),
            'latitude': self.read_task_values(input_file, '/latitude'),
            'longitude': self.read_task_values(input_file, '/longitude')
        }
        return data

    def read_task_values(self, input_file, data_path):
        path = data_path
        task2_values, meta = self.fm.read(input_file, data_path=path)
        return task2_values

    def get_date_times(self, current, times):
        result = []
        current_datetime = datetime.datetime.strptime(current, '%Y%m%d%H%M')
        for time in times:
            hour = int(time.replace('h', ''))
            o_date = current_datetime + datetime.timedelta(hours=hour)
            result.append(o_date.strftime('%Y%m%d%H'))
        return result

    def test_file_generate(self):
        input_data_prefix = 'kim_g120_ne36_'

        # Specify the folder containing the files
        input_folder_path = 'C:/Users/user/Desktop/KIM'
        output_folder_path = input_folder_path+'/output'
        os.makedirs(output_folder_path, exist_ok=True)

        # Iterate over the files in the folder
        for filename in os.listdir(input_folder_path):


            date = filename[24:34]
            data_type=filename[14:19]
            output_file = output_folder_path+'/'+date+'gb2.nc'
                
            ds = Dataset(output_file, 'w', format="NETCDF4")
            times = ['h000', 'h003', 'h006', 'h009','h012','h015','h018','h021','h024','h027','h030','h033','h036','h039','h042','h045','h048']



            result = self.read_data(input_folder_path+'/'+input_data_prefix+data_type+times[0]+'.'+date+'.gb2')
            titles = result.keys()

            for title in titles:
                result[title] = np.empty((len(times),result['longitude'].shape[0],result['longitude'].shape[1]))
            for index, time in enumerate([times[0]]):
                data = self.read_data(input_data_prefix+time+'.'+date+'.gb2.nc')
                for title in titles:
                    result[title][index] = data[title]
            times = self.get_date_times(date, times)
            lats = np.array(result['latitude'])[0]
            lons = np.array(result['longitude'])[0]

            #차원생성
            ds.createDimension('latitude', lats.shape[0])
            ds.createDimension('longitude', lats.shape[1])
            ds.createDimension('times', len(times))

            #데이터 저장할 변수 공간 생성
            ds.createVariable('INPUTDATA/latitude', 'f8', ('latitude', 'longitude'))
            ds.createVariable('INPUTDATA/longitude', 'f8', ('latitude', 'longitude'))
            ds.createVariable('INPUTDATA/times', 'str', 'times')

            #변수에 데이터 저장
            ds['INPUTDATA/latitude'][:] = lats
            ds['INPUTDATA/longitude'][:] = lons
            ds['INPUTDATA/times'][:] = np.array(times)
            for title in titles:
                if title == 'latitude' or title == 'longitude':
                    continue
                values = np.array(result[title])[:, :]
                ds.createVariable('INPUTDATA/'+title, 'f4',
                                  ('times', 'latitude', 'longitude'),fill_value=9.999e+20)
                ds['INPUTDATA/'+title][:, :] = np.array(values)[:]

            ds.close()
            print(f'{date} done')


def main():
    file_gen= FileGenerateTest()
    file_gen.test_file_generate()

if __name__ == '__main__':
    main()
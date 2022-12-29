# import unittest
#
# import numpy as np
# from netCDF4 import Dataset
#
# from aiw_task_cm.file.file_manager_factory import FileManagerFactory
#
# class FileGenerateTest(unittest.TestCase):
#
#     def setUp(self) -> None:
#         super().setUp()
#         self.fm = FileManagerFactory().get_instance('netcdf')
#
#     def read(self, input_file):
#         data = {
#             'tmp_500': self.read_task_values(input_file, '/TMP_700mb'),
#             'tmp_700': self.read_task_values(input_file, '/TMP_700mb'),
#             'tmp_850': self.read_task_values(input_file, '/TMP_850mb'),
#             'ugrd_850': self.read_task_values(input_file, '/UGRD_850mb'),
#             'vgrd_850': self.read_task_values(input_file, '/VGRD_850mb'),
#             'latitude': self.read_task_values(input_file, '/latitude'),
#             'longitude': self.read_task_values(input_file, '/longitude')
#         }
#         return data
#
#     def read_task_values(self, input_file, data_path):
#         path = data_path
#         task2_values, meta = self.fm.read(input_file, data_path=path)
#         return task2_values
#
#     def test_file_generate(self):
#         titles = ['tmp_500', 'tmp_700', 'tmp_850', 'ugrd_850', 'vgrd_850']
#
#         ds = Dataset('/home/hbh/dev/test.nc', 'w', format="NETCDF4")
#
#         data = self.read('/home/hbh/dev/g128_v070_ergl_pres_h000.2022020700.nc')
#         lats = np.array(data['latitude'])[1066:1600]
#         lons = np.array(data['longitude'])[750:1050]
#
#         ds.createDimension('latitude', np.array(data[titles[0]])[0][1066:1600, 750:1050].shape[0])
#         ds.createDimension('longitude', np.array(data[titles[0]])[0][1066:1600, 750:1050].shape[1])
#         ds.createVariable('INPUTDATA/latitude', 'f8', 'latitude')
#         ds.createVariable('INPUTDATA/longitude', 'f8', 'longitude')
#         ds['INPUTDATA/latitude'][:] = lats
#         ds['INPUTDATA/longitude'][:] = lons
#         for title in titles:
#             values = np.array(data[title])[0][1066:1600, 750:1050]
#
#             ds.createVariable('INPUTDATA/'+title+'/h000', float,
#                               ('latitude', 'longitude'))
#
#             ds['INPUTDATA/'+title+'/h000'][:, :] = values
#         ds.close()
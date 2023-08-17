from netCDF4 import Dataset
from aiw_task_cm.file.file_manager import FileManager
import numpy as np


class NetcdfFileManager(FileManager):

    def read(self, path, **kwargs):
        try:
            dim = kwargs.get('dim', None)
            data_path = kwargs.get('data_path', '')
            nc = Dataset(path, 'r', format="NETCDF4")
            nc.set_auto_mask(False)
            dataset = nc[data_path]

            data = np.asarray(dataset, order='C')
            mata = dataset.__dict__
            if dim != None:
                return data[dim], mata
            nc.close()
            return data, mata
        except IndexError as e:
            print(e)
        return np.asarray([]), None

    def write(self, data, path, **kwargs):
        try:
            task_number = kwargs.get('task_number', '')
            data_type = kwargs.get('data_type', '')
            value_type = 'f4'
            if 'value_type' in kwargs:
                value_type = kwargs.get('value_type')
            ds = Dataset(path, 'a', format="NETCDF4")

            if data_type == "flow":
                values = np.array(data[2])



                if values.ndim==1:
                    ds.createVariable('FLOWDATA/' + task_number, 'int', ('times'))
                    ds['FLOWDATA/' + task_number][:] = values
                else:
                    ds.createVariable('FLOWDATA/' + task_number, value_type, ('times', 'latitude', 'longitude'))
                    ds['FLOWDATA/' + task_number][:, :, :] = values
                ds.close()
            elif data_type == "result":
                for dt in data:

                    date = dt[2]
                    advisory = np.array(dt[0])
                    warning = np.array(dt[1])
                    ds.createDimension(date + '_advisory', len(advisory))
                    ds.createDimension(date + '_warning', len(advisory))

                    ds.createVariable('RESULT/' + date + '/advisory', 'int', (date + '_advisory'))
                    ds.createVariable('RESULT/' + date + '/advisory_total_precipitation', 'f8', (date + '_advisory'))
                    ds.createVariable('RESULT/' + date + '/warning', 'int', (date + '_warning'))
                    ds.createVariable('RESULT/' + date + '/warning_total_precipitation', 'f8', (date + '_warning'))
                    if len(advisory) != 0:
                        ds['RESULT/' + date + '/advisory'][:] = advisory
                        ds['RESULT/' + date + '/warning_total_precipitation'][:] = warning
                    # if len(warning) != 0:
                    #     ds['RESULT/' + date + '/warning'][:] = warning
                ds.close()
            pass
        except IndexError as e:
            ds.close()
            print(e)
        pass
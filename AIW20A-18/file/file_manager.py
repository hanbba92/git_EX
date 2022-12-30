from aiw_task_cm.file.file_manager_factory import FileManagerFactory

class FileManager(object):
    def __init__(self):
        self.fm = FileManagerFactory().get_instance('netcdf')

    def read(self, input_file, **kwargs):
        return FileReader(self.fm).read(input_file)

    def write(self, input_file, result, **kwargs):
        task_number = kwargs.get('task_number', '')
        self.fm.write(result, input_file, task_number=task_number, data_type='flow')
        pass


class FileReader(object):
    def __init__(self, fm):
        self.fm = fm

    def read(self, input_file):
        data = {
            'u_wind': self.read_task_values(input_file, 'INPUTDATA/u_wind/h000'),
            'v_wind': self.read_task_values(input_file, 'INPUTDATA/v_wind/h000'),
            'longitude': self.read_task_values(input_file, 'INPUTDATA/longitude'),
            'latitude': self.read_task_values(input_file, 'INPUTDATA/latitude')
        }
        return data

    def read_task_values(self, input_file, data_path):
        path = data_path
        task2_values, meta = self.fm.read(input_file, data_path=path)
        return task2_values
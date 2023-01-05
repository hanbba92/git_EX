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
            'tmp_600': self.read_task_values(input_file, 'INPUTDATA/tmp_600/h000'),
            'tmp_700': self.read_task_values(input_file, 'INPUTDATA/tmp_700/h000'),
            'tmp_850': self.read_task_values(input_file, 'INPUTDATA/tmp_850/h000'),
            'tmp_925': self.read_task_values(input_file, 'INPUTDATA/tmp_925/h000'),
            'tmp_950': self.read_task_values(input_file, 'INPUTDATA/tmp_950/h000'),
            'tmp_1000': self.read_task_values(input_file, 'INPUTDATA/tmp_1000/h000'),
            'rh_600': self.read_task_values(input_file, 'INPUTDATA/rh_600/h000'),
            'rh_700': self.read_task_values(input_file, 'INPUTDATA/rh_700/h000'),
            'rh_850': self.read_task_values(input_file, 'INPUTDATA/rh_850/h000'),
            'rh_925':self.read_task_values(input_file, 'INPUTDATA/rh_925/h000'),
            'rh_950':self.read_task_values(input_file, 'INPUTDATA/rh_950/h000'),
            'rh_1000': self.read_task_values(input_file, 'INPUTDATA/rh_1000/h000'),
            'longitude': self.read_task_values(input_file, 'INPUTDATA/longitude'),
            'latitude': self.read_task_values(input_file, 'INPUTDATA/latitude')
        }
        return data

    def read_task_values(self, input_file, data_path):
        path = data_path
        task2_values, meta = self.fm.read(input_file, data_path=path)
        return task2_values
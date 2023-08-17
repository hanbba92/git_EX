from aiw_task_cm.file.aws_file_mananger import AwsFileManager
from aiw_task_cm.file.netcdf_file_manager import NetcdfFileManager
from aiw_task_cm.file.yaml_file_manager import YamlFileManager

class FileManagerFactory(object):
    """
    File Manager Factory
    """
    def __init__(self):
        """
        constructor
        """
        self.instance = {
            'aws': AwsFileManager(),
            'netcdf': NetcdfFileManager(),
            'yaml': YamlFileManager()
        }

    def get_instance(self, type):
        """
        get file manager instance
        :param type: file type
        :return: instance
        """
        return self.instance[type]
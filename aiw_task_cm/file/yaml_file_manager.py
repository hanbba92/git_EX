import yaml
from aiw_task_cm.file.file_manager import FileManager



class YamlFileManager(FileManager):
    """
    yaml file manager
    """
    def read(self, path, **kwargs):
        """
        yaml file read
        :param path: file path
        :param kwargs:
        :return: yaml file value
        """
        stream = open(path, 'r', encoding='utf-8')
        data = yaml.load(stream, Loader=yaml.FullLoader)
        stream.close()
        return data


    def write(self, data, path, **kwargs):
        """
        write data as yaml
        :param data: data
        :param path: file path
        :param kwargs:
        :return: N/A
        """

        pass
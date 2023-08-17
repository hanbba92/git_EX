from abc import *


class FileManager(metaclass=ABCMeta):
    """
    File manager interface
    """
    @abstractmethod
    def read(self, path, **kwargs):
        """
        read file
        :param path: file path
        :param kwargs: file read option
        :return: N/A
        """
        pass

    @abstractmethod
    def write(self, data, path, **kwargs):
        """
        write data
        :param data:
        :param path:
        :param kwargs:
        :return:
        """
        pass

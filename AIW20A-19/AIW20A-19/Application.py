import sys

import numpy as np
import aiw_task_cm.common.initiator as common
from file.file_manager import FileManager
from test.file_generate_test import FileGenerateTest


# check conditions(temperature, CAPE, CIN)
class Application(object):

    def __init__(self, input_file1, input_file2, input_file3, output_tasks):
        self.input_file1 = input_file1
        self.input_file2 = input_file2
        self.input_file3 = input_file3
        self.output_tasks = output_tasks

    def run(self):
        """
        run task
        :return: N/A
        """

        common.logger.info("Checking Conditions...")

        task_file_manager = FileManager()
        file_gen = FileGenerateTest()

        data1 = task_file_manager.read(self.input_file1)
        data2 = task_file_manager.read(self.input_file2)
        data3 = task_file_manager.read(self.input_file3)

        tmp_925, cape, cin = data1['tmp_925'], data2['cape'], data3['cin']

        result = tmp_925 + cape + cin
        result = np.where(result == 3, 1, 0)

        ds = file_gen.test_file_generate()

        task_file_manager.write('/Users/user/Desktop/netcdf/aiw_task19_input_20220207.nc',
                                [data1['latitude'], data1['longitude'], result], task_number=self.output_tasks)
        print(result)
        common.logger.info("Creating Output Data..")


def main():
    input_file1 = sys.argv[1] #tmp 타스크의 출력 nc파일명
    input_file2 = sys.argv[2] #cape 타스크의 출력 nc파일명
    input_file3 = sys.argv[3] #cin 타스크의 출력 nc파일명
    output_task = sys.argv[4]

    common.init('aiw-task-hr-19')
    app = Application(input_file1, input_file2, input_file3, output_task)
    app.run()
    pass
    # python application.py /Users/user/Desktop/netcdf/aiw_task19_tmp_input_20220207.nc /Users/user/Desktop/netcdf/aiw_task19_cape_input_20220207.nc /Users/user/Desktop/netcdf/aiw_task19_cin_input_20220207.nc 19

if __name__ == '__main__':
    main()
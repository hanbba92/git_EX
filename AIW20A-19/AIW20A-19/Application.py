import sys

import numpy as np
import aiw_task_cm.common.initiator as common
from file.file_manager import FileManager
from test.file_generate_test import FileGenerateTest

#check conditions(temperature, CAPE)
class Application(object):

    def __init__(self, input_file1, input_file2, output_tasks):
        self.input_file1 = input_file1
        self.input_file2 = input_file2
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

        tmp_925, cape = data1['tmp_925'], data2['cape']

        result = tmp_925 + cape
        result = np.where(result == 2, 1, 0)

        ds = file_gen.test_file_generate()

        task_file_manager.write('/Users/user/Desktop/netcdf/aiw_task19_input_20220207.nc', [data1['latitude'], data1['longitude'], result], task_number=self.output_tasks)
        print(result)
        common.logger.info("Creating Output Data..")


def main():
    input_file1 = sys.argv[1]  #tmp task의 출력 nc파일
    input_file2 = sys.argv[2]  #CAPE task의 출력 nc파일
    output_task = sys.argv[3]
    
    common.init('aiw-task-hr-19')
    app = Application(input_file1, input_file2,  output_task)
    app.run()
    pass

if __name__ == '__main__':
    main()
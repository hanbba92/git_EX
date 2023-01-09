import sys

import numpy as np
import aiw_task_cm.common.initiator as common
from file.file_manager import FileManager
from test.file_generate_test import FileGenerateTest

#check conditions(temperature, CIN, SouthWest wind speed)
class Application(object):

    def __init__(self, input_file, output_tasks):
        self.input_file = input_file
        self.output_tasks = output_tasks

    def run(self):
        """
        run task
        :return: N/A
        """

        common.logger.info("Checking Conditions...")

        task_file_manager = FileManager()
        file_gen = FileGenerateTest()

        data = task_file_manager.read(self.input_file)

        tmp_925, cin, southwest = data['tmp_925'], data['cin'], data['southwest']

        result = tmp_925 + cin + southwest
        result = np.where(result == 3, 1, 0)


        task_file_manager.write(self.input_file, [data['latitude'], data['longitude'], result], task_number=self.output_tasks)
        print(result)
        common.logger.info("Creating Output Data..")


def main():
    input_file = sys.argv[1]
    output_task = sys.argv[2]
    #공통위치 판단만이 목적으로 base값은 불필요
    
    common.init('aiw-task-hr-22')
    app = Application(input_file, output_task)
    app.run()
    pass

if __name__ == '__main__':
    main()
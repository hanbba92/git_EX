import sys

import numpy as np
import aiw_task_cm.common.initiator as common
from file.file_manager import FileManager

# base1 <= tmp <= base2
class Application(object):

    def __init__(self, input_file, output_tasks, base1, base2):
        self.input_file = input_file
        self.output_tasks = output_tasks
        self.base1 = base1
        self.base2 = base2

    def run(self):
        """
        run task
        :return: N/A
        """

        common.logger.info("Calculating Temperature...")

        task_file_manager = FileManager()

        data = task_file_manager.read(self.input_file)

        tmp_925 = data['tmp_925']
        tmp_925 = tmp_925 - 273.15 #절대온도 -> 섭씨

        result = np.where(tmp_925 <= self.base2, tmp_925, 0) #기온 기준값 해당여부 판단
        result = np.where(self.base1 <= result, 1, 0)

        task_file_manager.write(self.input_file, [data['latitude'], data['longitude'], result], task_number=self.output_tasks)
        print(result)
        common.logger.info("Creating Output Data..")


def main():
    input_file = sys.argv[1]
    output_task = sys.argv[2]
    base1 = float(sys.argv[3])
    base2 = float(sys.argv[4])

    common.init('aiw-task-hr-22')
    app = Application(input_file, output_task, base1, base2)
    app.run()
    pass

if __name__ == '__main__':
    main()
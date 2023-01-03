import sys

import numpy as np
import aiw_task_cm.common.initiator as common
from file.file_manager import FileManager

#CAPE >= base
class Application(object):

    def __init__(self, input_file, output_tasks, base):
        self.input_file = input_file
        self.output_tasks = output_tasks
        self.base = float(base)

    def run(self):
        """
        run task
        :return: N/A
        """

        common.logger.info("Calculating CAPE...")

        task_file_manager = FileManager()

        data = task_file_manager.read(self.input_file)

        CAPE = data['cape']

        result = np.where(CAPE >= self.base, 1, 0)

        task_file_manager.write(self.input_file, [data['latitude'], data['longitude'], result], task_number=self.output_tasks)
        print(result)
        common.logger.info("Creating Output Data..")


def main():
    input_file = sys.argv[1]
    output_task = sys.argv[2]
    base = sys.argv[3]

    common.init('aiw-task-hr-19')
    app = Application(input_file, output_task, base)
    app.run()
    pass

if __name__ == '__main__':
    main()
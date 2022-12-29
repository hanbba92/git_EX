import sys

import aiw_task_cm.common.initiator as common
from file.file_manager import FileManager
from service.DewPointCalculator import DewPointCalculator
import numpy as np


class Application(object):

    def __init__(self, input_file, output_tasks, base):
        self.input_file = input_file
        self.output_tasks = output_tasks
        self.base = base

    def run(self):
        """
        run task
        :return: N/A
        """

        common.logger.info("Calculating Dew Point Temperature..")

        task_file_manager = FileManager()

        data = task_file_manager.read(self.input_file)
        dew_point_calc = DewPointCalculator()

        tmp_925, rh_925 = data['tmp_925'], data['rh_925']

        tmp_925 = tmp_925 - 273.15

        print(tmp_925)

        dew_point_list_925 = dew_point_calc.get_dew_point_result_list(tmp_925, rh_925)

        result = np.array(dew_point_list_925) >= self.base
        print(result)

        task_file_manager.write(self.input_file, [data['latitude'], data['longitude'], result], task_number=self.output_tasks)
        common.logger.info("Creating Output Data..")


def main():
    input_file = sys.argv[1]
    output_task = sys.argv[2]
    base = float(sys.argv[3])

    common.init('AIW20A-16')
    app = Application(input_file, output_task, base)
    app.run()
    pass


if __name__ == '__main__':
    main()


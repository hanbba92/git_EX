import sys

import aiw_task_cm.common.initiator as common
from file.file_manager import FileManager
from service.wind_direction_calculator import WindDirectionCalculator
import numpy as np


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

        common.logger.info("Calculating WindWind Direction..")

        task_file_manager = FileManager()

        data = task_file_manager.read(self.input_file)
        wind_direction_cal = WindDirectionCalculator()

        u_925, v_925 = data['u_925'], data['v_925']

        dew_point_list_925 = wind_direction_cal.get_wind_direction_result_list(u_925, v_925)
        dew_point_list_925 = np.array(dew_point_list_925)

        result = np.where(dew_point_list_925 <= self.base2, dew_point_list_925, 0)
        result = np.where(self.base1 <= result, 1, 0)

        print(result)

        task_file_manager.write(self.input_file, [data['latitude'], data['longitude'], result], task_number=self.output_tasks)
        common.logger.info("Creating Output Data..")


def main():
    input_file = sys.argv[1]
    output_task = sys.argv[2]
    base1 = float(sys.argv[3])
    base2 = float(sys.argv[4])

    common.init('aiw-task-hr-17')
    app = Application(input_file, output_task, base1, base2)
    app.run()
    pass


if __name__ == '__main__':
    main()


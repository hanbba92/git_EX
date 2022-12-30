import sys

import numpy as np
#from netCDF4 import Dataset
from test.file_generate_test import FileGenerateTest
import aiw_task_cm.common.initiator as common
from file.file_manager import FileManager
from service.SouthwestWindCaculator import SouthwestWindCalculator

#southewst_wind_speed
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

        common.logger.info("Calculating Souhtwest Wind Speed...")

        task_file_manager = FileManager()

        data = task_file_manager.read(self.input_file)
        sw_wspd_clac = SouthwestWindCalculator()

        u_wind, v_wind = data['u_wind'], data['v_wind'] #단위 = m/s이므로 1.94384를 곱해서 kts단위로 환산 필요
        u_wind = u_wind * 1.94384
        v_wind = v_wind * 1.94384

        result = sw_wspd_clac.get_sw_wind_speed_result(u_wind, v_wind) > float(self.base)

        task_file_manager.write(self.input_file, [data['latitude'], data['longitude'], result], task_number=self.output_tasks)
        print(result)
        common.logger.info("Creating Output Data..")


def main():
    input_file = sys.argv[1]
    output_task = sys.argv[2]
    base = sys.argv[3]

    common.init('aiw-task')
    app = Application(input_file, output_task, base)
    app.run()
    pass

if __name__ == '__main__':
    main()
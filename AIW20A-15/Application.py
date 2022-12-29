import sys

import numpy as np
#from netCDF4 import Dataset

import aiw_task_cm.common.initiator as common
from file.file_manager import FileManager
from service.WetBulbCalculator import WetBulbCalculator
#wet-bulb temperature

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

        common.logger.info("Calculating wet-bulb temperature...")

        task_file_manager = FileManager()

        data = task_file_manager.read(self.input_file)
        wet_bulb_calc = WetBulbCalculator()

        tmp_1D5maboveground, rh_1D5maboveground = data['tmp_1D5maboveground'], data['rh_1D5maboveground']

        tmp_1D5maboveground = tmp_1D5maboveground-273.15 #절대온도 -> 섭씨로 변환

        result = wet_bulb_calc.get_wet_bulb_temp_result(tmp_1D5maboveground, rh_1D5maboveground) > float(self.base) #형변환 과정 추가됨

        task_file_manager.write(self.input_file, [data['latitude'], data['longitude'], result], task_number=self.output_tasks)
        print(result)
        common.logger.info("Creating Output Data..")


def main():
    input_file = sys.argv[1]
    output_task = sys.argv[2]
    base = sys.argv[3]

    common.init('aiw-task') #타스크명 수정필요
    app = Application(input_file, output_task, base)
    app.run()
    pass

if __name__ == '__main__':
    main()
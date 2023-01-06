import sys

import numpy as np
import aiw_task_cm.common.initiator as common
from file.file_manager import FileManager
from service.SouthwestWindCalculator import SouthwestWindCalculator

#base1 <= SouthWest wind speed <= base2
class Application(object):

    def __init__(self, input_file, output_tasks, base1, base2):
        self.input_file = input_file
        self.output_tasks = output_tasks
        self.base1 = float(base1)
        self.base2 = float(base2)

    def run(self):
        """
        run task
        :return: N/A
        """

        common.logger.info("Calculating Southwest Wind Speed...")

        task_file_manager = FileManager()

        data = task_file_manager.read(self.input_file)
        sw_wspd_calc = SouthwestWindCalculator()

        u_wind, v_wind = data['u_wind'], data['v_wind']  # 단위 = m/s이므로 1.94384를 곱해서 kts단위로 환산 필요
        u_wind = u_wind * 1.94384
        v_wind = v_wind * 1.94384

        sw_speed = sw_wspd_calc.get_sw_wind_speed_result(u_wind, v_wind)
        result = np.where(sw_speed <= self.base2, sw_speed, 0)  # 속력 기준값 해당여부 판단
        result = np.where(self.base1 <= result, 1, 0)

        task_file_manager.write(self.input_file, [data['latitude'], data['longitude'], result], task_number=self.output_tasks)
        print(result)
        common.logger.info("Creating Output Data..")


def main():
    input_file = sys.argv[1]
    output_task = sys.argv[2]
    base1 = sys.argv[3]
    base2 = sys.argv[4]

    common.init('aiw-task-hr-22')
    app = Application(input_file, output_task, base1, base2)
    app.run()
    pass

if __name__ == '__main__':
    main()
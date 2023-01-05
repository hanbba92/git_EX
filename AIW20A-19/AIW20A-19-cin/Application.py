import sys

import aiw_task_cm.common.initiator as common
from file.file_manager import FileManager
from service.CIN_Calculator import CIN_Calculator

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

        common.logger.info("Calculating CIN...")

        task_file_manager = FileManager()

        data = task_file_manager.read(self.input_file)
        cin_calc = CIN_Calculator()

        tmp_600, tmp_700, tmp_850, tmp_925, tmp_950, tmp_1000 = data['tmp_600'], data['tmp_700'], data['tmp_850'], data['tmp_925'], data['tmp_950'], data['tmp_1000']
        rh_600, rh_700, rh_850, rh_925, rh_950, rh_1000 =  data['rh_600'], data['rh_700'], data['rh_850'], data['rh_925'], data['rh_950'], data['rh_1000']

        result = cin_calc.get_cin_result(tmp_600, tmp_700, tmp_850, tmp_925, tmp_950, tmp_1000, rh_600, rh_700, rh_850, rh_925, rh_950, rh_1000) >= -float(self.base)

        task_file_manager.write(self.input_file, [data['latitude'], data['longitude'], result], task_number=self.output_tasks)
        print(result)
        common.logger.info("Creating Output Data..")


def main():
    input_file = sys.argv[1]
    output_task = sys.argv[2]
    base = sys.argv[3]

    common.init('aiw-task-19')
    app = Application(input_file, output_task, base)
    app.run()
    pass

if __name__ == '__main__':
    main()
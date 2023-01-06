import sys

import aiw_task_cm.common.initiator as common
from file.file_manager import FileManager
from service.CIN_Calculator import CIN_Calculator

#cin calculate
class Application(object):

    def __init__(self, input_file, output_tasks):
        self.input_file = input_file
        self.output_tasks = output_tasks

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
        rh_600, rh_700, rh_850, rh_925, rh_950, rh_1000 = data['rh_600'], data['rh_700'], data['rh_850'], data['rh_925'], data['rh_950'], data['rh_1000']

        #cin은 -nnn ~ 0의 값을 가진다. 값이 0미만이라면 역전층이 존재하는 것으로 볼 수 있다.
        result = cin_calc.get_cin_result(tmp_600, tmp_700, tmp_850, tmp_925, tmp_950, tmp_1000, rh_600, rh_700, rh_850, rh_925, rh_950, rh_1000) < 0

        task_file_manager.write(self.input_file, [data['latitude'], data['longitude'], result], task_number=self.output_tasks)
        print(result)
        common.logger.info("Creating Output Data..")


def main():
    input_file = sys.argv[1]
    output_task = sys.argv[2]
    #역전층 존재 여부 판단만이 목적으로 base값이 불필요

    common.init('aiw-task-22')
    app = Application(input_file, output_task)
    app.run()
    pass

if __name__ == '__main__':
    main()
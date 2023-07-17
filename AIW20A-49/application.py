import sys
from file.file_manager import FileManager
import aiw_task_cm.common.initiator as common
import numpy as np

class Application(object):
    def __init__(self, workflow_id, input_file, wind_shear_task, multiplier, output_task):
        self.workflow_id = workflow_id
        self.input_file = input_file
        self.wind_shear_task = wind_shear_task
        self.multiplier = multiplier
        self.output_task = output_task

    def run(self):
        task_file_manager = FileManager()
        wind_shear_inp = task_file_manager.read(self.input_file, self.wind_shear_task)
        multiplier_inp = task_file_manager.read(self.input_file, self.multiplier)
        # 각 바람성분을 하나로 합침.
        wind_shear = wind_shear_inp['value'][0]
        multiplier = multiplier_inp['value'][0]
        score = np.sum(wind_shear ** 2 * multiplier)
        result = np.full_like(wind_shear_inp['latitude'], score)

        task_file_manager.write(self.input_file, [wind_shear_inp['latitude'], wind_shear_inp['longitude'], result],
                                task_number=self.output_task)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    wind_shear_task = sys.argv[3]
    multiplier = sys.argv[4]
    output_task = sys.argv[5]

    common.init('aiw-task-hr-' + output_task, workflow_id)
    result = 0
    try:
        app = Application(workflow_id, input_file, wind_shear_task, multiplier, output_task)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

import sys
from file.file_manager import FileManager
import aiw_task_cm.common.initiator as common
import numpy as np
from service.conv2d import vector_conv_sameshape

class Application(object):
    def __init__(self, workflow_id, input_file, wind_shear_task, near_median_task, output_task):
        self.workflow_id = workflow_id
        self.input_file = input_file
        self.wind_shear_task = wind_shear_task
        self.near_median_task = near_median_task
        self.output_task = output_task

    def run(self):
        task_file_manager = FileManager()
        inp = task_file_manager.read(self.input_file, self.wind_shear_task, self.near_median_task)
        # 각 바람성분을 하나로 합침.
        wind_shear = inp['wind_shear'][0]
        near_median = inp['near_median'][0]
        score = np.sum(wind_shear ** 2 * near_median)
        result = np.full_like(inp['latitude'], score)

        task_file_manager.write(self.input_file, [inp['latitude'], inp['longitude'], result],
                                task_number=self.output_task)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    wind_shear_task = sys.argv[3]
    near_median_task = sys.argv[4]
    output_task = sys.argv[5]

    common.init('aiw-task-hr-' + output_task, workflow_id)
    result = 0
    try:
        app = Application(workflow_id, input_file, wind_shear_task, near_median_task, output_task)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

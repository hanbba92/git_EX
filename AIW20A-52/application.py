import sys
from file.file_manager import FileManager
import aiw_task_cm.common.initiator as common
import numpy as np
from service.conv2d import conv_sameshape
from scipy.ndimage import gaussian_filter

class Application(object):
    def __init__(self, workflow_id, input_file, input_task, output_task):
        self.workflow_id = workflow_id
        self.input_file = input_file
        self.input_task = input_task
        self.output_task = output_task

    def run(self):
        task_file_manager = FileManager()
        inp = task_file_manager.read(self.input_file, self.input_task)
        value = inp['value'][0]
        for i in range (value.shape[0]):
            for j in range (value.shape[1]):
                    if(value[i, j] > 10000): value[i, j]=value[i, j-1]
        value = gaussian_filter(value, sigma=1)
        median = (np.max(value) + np.min(value))/2
        print(median)

        result = np.absolute(value - median)
        result = np.max(result) - result
        result = result ** 2
        result = (result-np.mean(result))/np.std(result) +3





        task_file_manager.write(self.input_file, [inp['latitude'], inp['longitude'], result],
                                task_number=self.output_task)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    input_task = sys.argv[3]
    output_task = sys.argv[4]

    common.init('aiw-task-hr-' + output_task, workflow_id)
    result = 0
    try:
        app = Application(workflow_id, input_file, input_task, output_task)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

import sys
import numpy as np
from file.file_manager import FileManager
import aiw_task_cm.common.initiator as common
# from mpl_toolkits.basemap import Basemap
# import os
# import aiw_task_cm.image.generator as image
# import datetime
# from aiw_task_cm.common.grid_to_point_convertor import grid_to_points
# from aiw_task_cm.common.result_logger import result_logger


class Application(object):

    def __init__(self, input_file, task_number, input_task, op, base, workflow_id):
        self.input_file = input_file
        self.task_number = task_number
        self.input_task = input_task
        self.op = op
        self.base = base
        self.workflow_id = workflow_id

    def run(self):
        """
        run task
        :return: N/A
        """
        task_file_manager = FileManager()
        data = task_file_manager.read(self.input_file, self.input_task)
        result = []
        if self.op == '>=':
            result = data['value'] >= float(self.base)
        elif self.op == '>':
            result = data['value'] > float(self.base)
        elif self.op == '==':
            result = data['value'] == float(self.base)
        elif self.op == '<=':
            result = data['value'] <= float(self.base)
        elif self.op == '<':
            result = data['value'] < float(self.base)
        print(result.shape)
        print(result[:, 180, 267])

        task_file_manager.write(self.input_file, [data['latitude'], data['longitude'], result], task_number=self.task_number)

def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    task_number = sys.argv[3]
    input_task = sys.argv[4]
    op = sys.argv[5]
    base = sys.argv[6]

    common.init('aiw-task-hr-' + task_number, workflow_id)
    result = 0
    try:
        app = Application(input_file, task_number, input_task, op, base, workflow_id)
        app.run()
    except Exception as e:
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

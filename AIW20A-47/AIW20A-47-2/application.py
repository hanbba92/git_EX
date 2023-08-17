import sys
from file.file_manager import FileManager
import aiw_task_cm.common.initiator as common
import numpy as np


class Application(object):
    def __init__(self, workflow_id, input_file, input_task, output_task, lat_base):
        self.workflow_id = workflow_id
        self.input_file = input_file
        self.input_task = input_task
        self.output_task = output_task
        self.lat_base = lat_base

    def run(self):
        task_file_manager = FileManager()
        inp =  task_file_manager.read(self.input_file, self.input_task)
        val = inp['value']
        # 기준 위도보다 높은곳을 True로 마스킹함
        north_mask = np.full(inp['latitude'].shape, False)
        north_mask[inp['latitude'] >= self.lat_base] = True

        # 마스크 적용 및 최댓값 broadcast
        for timeslice in val:
            timeslice[north_mask] = 0
            timeslice[:] = np.max(timeslice)

        task_file_manager.write(self.input_file, [inp['latitude'], inp['longitude'], val],
                                task_number=self.output_task)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    input_task = sys.argv[3]
    output_task = sys.argv[4]
    lat_base = float(sys.argv[5])


    common.init('aiw-task-hr-' + output_task, workflow_id)
    result = 0
    try:
        app = Application(workflow_id, input_file, input_task, output_task, lat_base)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

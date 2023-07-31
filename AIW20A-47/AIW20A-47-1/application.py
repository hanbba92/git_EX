import sys
from file.file_manager import FileManager
import aiw_task_cm.common.initiator as common
import numpy as np


class Application(object):
    def __init__(self, workflow_id, input_file, input_task, output_task, wind_speed_base):
        self.workflow_id = workflow_id
        self.input_file = input_file
        self.input_task = input_task
        self.output_task = output_task
        self.wind_speed_base = wind_speed_base

    def run(self):
        task_file_manager = FileManager()
        inp = task_file_manager.read(self.input_file, self.input_task)
        # 풍속 데이터 불러오기
        air_speed = inp['value']
        # 각 경도마다 값이 가장 큰 위도 구하고 1로 표시하기
        max_idx = np.argmax(air_speed, axis=1)
        result = np.zeros_like(air_speed)
        for i in range(0, result.shape[0]):
            for j in np.arange(max_idx.shape[1]):
                result[i, max_idx[i, j], j] = air_speed[i, max_idx[i,j], j] > self.wind_speed_base

        task_file_manager.write(self.input_file, [inp['latitude'], inp['longitude'], result],
                                task_number=self.output_task, timed=True)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    input_task = sys.argv[3]
    output_task = sys.argv[4]
    wind_speed_base = float(sys.argv[5])

    common.init('aiw-task-hr-' + output_task, workflow_id)
    result = 0
    try:
        app = Application(workflow_id, input_file, input_task, output_task, wind_speed_base)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

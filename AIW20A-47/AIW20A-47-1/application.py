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
        self.axis_stddev_limit = 30

    def run(self):
        task_file_manager = FileManager()
        inp = task_file_manager.read(self.input_file, self.input_task)
        # 풍속 데이터 불러오기
        air_speed = inp['value']
        # 각 경도마다 값이 가장 큰 위도 구하고 1로 표시하기
        max_idx = np.argmax(air_speed, axis=1)
        result = np.zeros_like(air_speed)

        sliding_window_size = 25
        sliding_window = np.ones(sliding_window_size) / sliding_window_size
        small_std = np.full_like(max_idx, True)
        for i in range(0, max_idx.shape[0]):
            for j in range(0, max_idx.shape[1] - sliding_window_size + 1):
                std = np.std(max_idx[i, j:j + sliding_window_size])
                if (std > self.axis_stddev_limit): small_std[i, sliding_window_size // 2 + j] = False
            max_idx[i] = np.convolve(max_idx[i], sliding_window, mode='same')
            small_std[i, 0:sliding_window_size // 2] = small_std[i, sliding_window_size // 2]
            small_std[i, max_idx.shape[1] - (sliding_window_size + 1) // 2 + 1:] = small_std[i,max_idx.shape[1] - (sliding_window_size + 1) // 2]

        for i in range(0, result.shape[0]):
            for j in np.arange(max_idx.shape[1]):
                result[i, max_idx[i, j], j] = (air_speed[i, max_idx[i, j], j] > self.wind_speed_base)
        result = result * small_std

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

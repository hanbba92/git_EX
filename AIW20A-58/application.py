import sys
import aiw_task_cm.common.initiator as common
import numpy as np
from aiw_task_cm.file.file_manager_factory import FileManagerFactory


class Application(object):
    def __init__(self, workflow_id, input_file, upper_jet_speed, possible_rain_area, output_task):
        self.workflow_id = workflow_id
        self.input_file = input_file
        self.upper_jet_speed = upper_jet_speed
        self.possible_rain_area = possible_rain_area
        self.output_task = output_task

    def run(self):
        fm = FileManagerFactory().get_instance('netcdf')

        lat, _ = fm.read(self.input_file, data_path='INPUTDATA/latitude')
        lon, _ = fm.read(self.input_file, data_path='INPUTDATA/longitude')
        upper_jet_speed, _ = fm.read(self.input_file, data_path=self.upper_jet_speed)
        possible_rain_area, _ = fm.read(self.input_file, data_path=self.possible_rain_area)
        # 결측치 처리
        upper_jet_speed[np.isnan(upper_jet_speed)] = np.nanmedian(upper_jet_speed)

        for time in range(0, upper_jet_speed.shape[0]):
            # 상층 풍속이 가장 큰 위치를 찾고 그 위치의 서남쪽의 possible_rain_area만 보존함
            highest_upper_wind = np.unravel_index(np.argmax(upper_jet_speed[time]), shape=upper_jet_speed[time].shape)
            mask = np.zeros_like(upper_jet_speed[time])
            mask[0:highest_upper_wind[0], 0:highest_upper_wind[1]] = 1
            print(highest_upper_wind)
            possible_rain_area[time] = possible_rain_area[time] * mask

        fm.write([lat, lon, possible_rain_area], self.input_file, task_number=self.output_task,
                 data_type='flow', timed=True)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    upper_jet_speed = sys.argv[3]
    possible_rain_area = sys.argv[4]
    output_task = sys.argv[5]

    common.init('aiw-task-hr-' + output_task, workflow_id)
    result = 0
    try:
        app = Application(workflow_id, input_file, upper_jet_speed, possible_rain_area, output_task)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

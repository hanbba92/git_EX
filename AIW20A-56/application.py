import sys
import aiw_task_cm.common.initiator as common
import numpy as np
from aiw_task_cm.file.file_manager_factory import FileManagerFactory


class Application(object):
    def __init__(self, workflow_id, input_file, LLJ_axis, wind_speed, output_task):
        self.workflow_id = workflow_id
        self.input_file = input_file
        self.LLJ_axis = LLJ_axis
        self.wind_speed = wind_speed
        self.output_task = output_task

    def run(self):
        fm = FileManagerFactory().get_instance('netcdf')

        lat, _ = fm.read(self.input_file, data_path='INPUTDATA/latitude')
        lon, _ = fm.read(self.input_file, data_path='INPUTDATA/longitude')
        LLJ_axis, _ = fm.read(self.input_file, data_path=self.LLJ_axis)
        wind_speed, _ = fm.read(self.input_file, data_path=self.wind_speed)
        # 결측치는 중앙값으로 바꿈
        wind_speed[np.isnan(wind_speed)] = np.nanmedian(wind_speed)
        # 최소 풍속 조건 체크
        wind_condition = np.zeros_like(wind_speed, dtype=bool)
        wind_condition[wind_speed > 15] = True
        # 하층 제트 축의 위쪽을 True로 바꾸는 부분
        is_lat_has_axis = np.max(LLJ_axis, axis=1)
        upper_axis_condition = np.zeros_like(LLJ_axis, dtype=bool)
        for i, timeslice in enumerate(LLJ_axis):
            arg_of_axis = np.argmax(timeslice, axis=0)
            for j in range(0, timeslice.shape[1]):
                if (is_lat_has_axis[i, j]):
                    upper_axis_condition[i, arg_of_axis[j]:, j] = True
        result = upper_axis_condition & wind_condition

        fm.write([lat, lon, result], self.input_file, task_number=self.output_task,
                 data_type='flow', timed=True)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    LLJ_axis = sys.argv[3]
    wind_speed = sys.argv[4]
    output_task = sys.argv[5]

    common.init('aiw-task-hr-' + output_task, workflow_id)
    result = 0
    try:
        app = Application(workflow_id, input_file, LLJ_axis, wind_speed, output_task)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

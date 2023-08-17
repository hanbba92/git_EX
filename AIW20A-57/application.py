import sys
import aiw_task_cm.common.initiator as common
import numpy as np
from aiw_task_cm.file.file_manager_factory import FileManagerFactory


class Application(object):
    def __init__(self, workflow_id, input_file, A_or_B_area, wind_speed, output_task,upper_jet_base):
        self.workflow_id = workflow_id
        self.input_file = input_file
        self.A_or_B_area = A_or_B_area
        self.wind_speed = wind_speed
        self.output_task = output_task
        self.upper_jet_base = upper_jet_base

    def run(self):
        fm = FileManagerFactory().get_instance('netcdf')

        lat, _ = fm.read(self.input_file, data_path='INPUTDATA/latitude')
        lon, _ = fm.read(self.input_file, data_path='INPUTDATA/longitude')
        A_or_B_area, _ = fm.read(self.input_file, data_path=self.A_or_B_area)
        wind_speed, _ = fm.read(self.input_file, data_path=self.wind_speed)
        # 풍속 조건으로 상층제트 위치 파악
        wind_speed_mask = wind_speed > self.upper_jet_base
        result = wind_speed_mask * A_or_B_area

        fm.write([lat, lon, result], self.input_file, task_number=self.output_task,
                 data_type='flow', timed=True)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    A_or_B_area = sys.argv[3]
    wind_speed = sys.argv[4]
    output_task = sys.argv[5]
    upper_jet_base = float(sys.argv[6])

    common.init('aiw-task-hr-' + output_task, workflow_id)
    result = 0
    try:
        app = Application(workflow_id, input_file, A_or_B_area, wind_speed, output_task, upper_jet_base)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

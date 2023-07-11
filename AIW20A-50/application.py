import sys
from file.file_manager import FileManager
import aiw_task_cm.common.initiator as common
import numpy as np


class Application(object):
    def __init__(self, workflow_id, input_file, input_task_0, input_task_1):
        self.workflow_id = workflow_id
        self.input_file = input_file
        self.input_task_0 = input_task_0 # 베이스 등압면 레벨
        self.input_task_1 = input_task_1 # 비교 등압면 레벨
        self.output_task = input_task_0+'-'+input_task_1

    def run(self):
        task_file_manager = FileManager()
        inp = task_file_manager.read(self.input_file, self.input_task_0, self.input_task_1)
        # 풍속 데이터 불러오기

        VGRD_0 = inp['VGRD_0'] # Zonal wind Base Level
        UGRD_0 = inp['UGRD_0'] # Meridional wind
        DZDT_0 = inp['DZDT_0'] # Vertical wind
        VGRD_1 = inp['VGRD_1'] # Comparing Level
        UGRD_1 = inp['UGRD_1']
        DZDT_1 = inp['DZDT_1']


        #각 레벨 벡터의 차 X,Y,Z
        X = UGRD_0-UGRD_1
        Y = VGRD_0-VGRD_1
        Z = DZDT_0-DZDT_1

        #벡터 크기 구하기 (각 레벨 벡터 차의 제곱의 합과 그 제곱급 구하기)

        X = X**2
        Y = Y**2
        Z = Z**2
        wind_shear = X+Y+Z
        wind_shear = wind_shear**(1/2)

        task_file_manager.write(self.input_file, [inp['latitude'], inp['longitude'], wind_shear],
                                task_number=self.output_task)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    input_task_0 = sys.argv[3]
    input_task_1 = sys.argv[4]
    output_task = sys.argv[3]+'-'+sys.argv[4]

    common.init('aiw-task-hr-' + output_task, workflow_id)
    result = 0
    try:
        app = Application(workflow_id, input_file, input_task_0, input_task_1)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

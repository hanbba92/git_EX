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
        Shape_info = VGRD_0.shape # array structure

        #각 레벨 벡터 (x,y,z) 구현
        Base_Level= zip(UGRD_0.flatten(),VGRD_0.flatten(),DZDT_0.flatten()) # 1-Dimension으로 바꾸어 각 좌표의 바람 성분 3가지를 하나로 묶는다.
        Compare_Level= zip(UGRD_1.flatten(),VGRD_1.flatten(),DZDT_1.flatten())


        #벡터 차 구하기
        wind_shear_list = [] # 각 좌표의 wind shear 최종 리스트
        for (Base,Compare) in zip(Base_Level,Compare_Level):
            wind_shear=np.linalg.norm(np.array(np.array(Base)-np.array(Compare))) # Base와 Comparing level 차의 벡터 크기
            wind_shear_list.append(wind_shear)
        wind_shear_list=np.array(wind_shear_list)
        Wind_Shear=wind_shear_list.reshape(Shape_info) #원래 좌표에 따른 바람 성분 파일 구조로 변환
        task_file_manager.write(self.input_file, [inp['latitude'], inp['longitude'], Wind_Shear],
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

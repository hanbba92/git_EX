import sys
from file.file_manager import FileManager
import aiw_task_cm.common.initiator as common
import numpy as np
from scipy.ndimage import gaussian_filter



class Application(object):
    def __init__(self, workflow_id, input_file, ugrd_task, vgrd_task, base_degree, output_task):
        self.workflow_id = workflow_id
        self.input_file = input_file
        self.ugrd_task = ugrd_task
        self.vgrd_task = vgrd_task
        self.base_degree = base_degree
        self.output_task = output_task

    def run(self):
        task_file_manager = FileManager()
        ugrd_inp = task_file_manager.read(self.input_file, self.ugrd_task)
        vgrd_inp = task_file_manager.read(self.input_file, self.vgrd_task)
        lat = ugrd_inp['latitude']
        lon = ugrd_inp['longitude']
        ugrd = ugrd_inp['value'][0]
        # 이상치 제거
        ugrd[ugrd>10000] = 0
        vgrd = vgrd_inp['value'][0]
        vgrd[vgrd>10000] = 0
        wind = np.stack((ugrd, vgrd), axis=-1)
        # 단위벡터 생성
        rad = np.deg2rad(self.base_degree)
        base_vec = np.array([np.cos(rad), np.sin(rad)])
        # 단위벡터와 바람속도 내적
        result = np.apply_along_axis(lambda x: np.dot(x, base_vec), axis=2, arr=wind)
        print(np.shape(result))
        result[result <0] = 0
        # 스무딩
        result = gaussian_filter(result, 4.)

        task_file_manager.write(self.input_file, [lat, lon, result],
                                task_number=self.output_task)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    ugrd_task = 'INPUTDATA/'+ sys.argv[3]
    vgrd_task = 'INPUTDATA/'+ sys.argv[4]
    base_degree = float(sys.argv[5])
    output_task = sys.argv[6]

    common.init('aiw-task-hr-' + output_task, workflow_id)
    result = 0
    try:
        app = Application(workflow_id, input_file, ugrd_task, vgrd_task, base_degree, output_task)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

import sys
from file.file_manager import FileManager
import aiw_task_cm.common.initiator as common
import numpy as np
from service.conv2d import vector_conv_sameshape

class Application(object):
    def __init__(self, workflow_id, input_file, isobaric, output_task):
        self.workflow_id = workflow_id
        self.input_file = input_file
        self.DZDT = 'INPUTDATA/DZDT_'+isobaric
        self.UGRD = 'INPUTDATA/UGRD_'+isobaric
        self.VGRD = 'INPUTDATA/VGRD_'+isobaric
        self.output_task = output_task

    def run(self):
        task_file_manager = FileManager()
        inp = task_file_manager.read(self.input_file, self.DZDT, self.UGRD, self.VGRD)
        DZDT = inp['DZDT']
        UGRD = inp['UGRD']
        VGRD = inp['VGRD']
        wind = np.vstack((DZDT, UGRD, VGRD))
        for i in range (wind.shape[0]):
            for j in range (wind.shape[1]):
                for k in range (wind.shape[2]):
                    if(wind[i, j, k] > 1000): wind[i, j, k]=wind[i, j, k-1]

        print(wind.shape)
        laplacian_filter = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
        result = vector_conv_sameshape(wind, laplacian_filter)


        task_file_manager.write(self.input_file, [inp['latitude'], inp['longitude'], result],
                                task_number=self.output_task)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    isobaric = sys.argv[3]
    output_task = sys.argv[4]

    common.init('aiw-task-hr-' + output_task, workflow_id)
    result = 0
    try:
        app = Application(workflow_id, input_file, isobaric, output_task)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

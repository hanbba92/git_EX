import sys
import aiw_task_cm.common.initiator as common
import numpy as np
from aiw_task_cm.file.file_manager_factory import FileManagerFactory
from skimage.feature import peak_local_max
from scipy.ndimage import binary_dilation

class Application(object):
    def __init__(self, workflow_id, input_file, PRMSL, output_task):
        self.workflow_id = workflow_id
        self.input_file = input_file
        self.PRMSL = PRMSL
        self.output_task = output_task

    def run(self):
        fm = FileManagerFactory().get_instance('netcdf')

        latitude, _ = fm.read(self.input_file, data_path='INPUTDATA/latitude')
        longitude, _ = fm.read(self.input_file, data_path='INPUTDATA/longitude')
        prmsl, _ = fm.read(self.input_file, data_path = self.PRMSL)
        y = np.arange(0., prmsl.shape[1])
        x = np.arange(0., prmsl.shape[2])

        prmsl[np.isnan(prmsl)] = np.nanmedian(prmsl)
        filter_size = 40
        high_or_low_pres = np.zeros_like(prmsl)
        result = np.zeros_like(prmsl)

        for i in range(0,prmsl.shape[0]):
            prmsl_min = np.min(prmsl[i])
            prmsl_max = np.max(prmsl[i])
            high_pres_loc = peak_local_max(prmsl[i]-prmsl_min, min_distance=filter_size, threshold_rel= 0.5 )
            for loc in high_pres_loc:
                high_or_low_pres[i, loc[0], loc[1]] = 1
            low_pres_loc = peak_local_max(prmsl_max-prmsl[i], min_distance=filter_size, threshold_rel = 0.5)
            for loc in low_pres_loc:
                high_or_low_pres[i, loc[0], loc[1]] = -1
            result[i] = binary_dilation(high_or_low_pres[i] == 1, structure=np.ones((5,5))).astype(float) - \
                        binary_dilation(high_or_low_pres[i] == -1, structure=np.ones((5,5))).astype(float)


        fm.write([y, x, result], self.input_file, task_number=self.output_task,
                 data_type='flow', timed=True)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    PRMSL = sys.argv[3]
    output_task = sys.argv[4]

    common.init('aiw-task-hr-' + output_task, workflow_id)
    result = 0
    try:
        app = Application(workflow_id, input_file, PRMSL, output_task)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

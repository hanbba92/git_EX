import sys
import aiw_task_cm.common.initiator as common
from aiw_task_cm.file.file_manager_factory import FileManagerFactory
from file.file_manager import FileManager
from service.sw_calculator import calculate_speed

class Application(object):

    def __init__(self, input_file, task_number, input_task, workflow_id):
        self.input_file = input_file
        self.task_number = task_number
        self.input_task = input_task
        self.workflow_id = workflow_id
    def run(self):
        """
        run task
        :return: N/A
        """
        fm = FileManagerFactory().get_instance('netcdf')
        task_file_manager = FileManager()

        data = task_file_manager.read(self.input_file, self.input_task)

        urgd, vgrd = data['UUU'], data['VVV']
        winds = calculate_speed(urgd, vgrd)

        fm.write([data['latitude'], data['longitude'], winds], self.input_file, task_number=self.task_number,
                 data_type='flow', timed=True)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    task_number = sys.argv[3]
    input_task = sys.argv[4:]


    common.init('aiw-task-hr-' + task_number, workflow_id)
    result = 0
    try:
        app = Application(input_file, task_number, input_task, workflow_id)
        app.run()
    except Exception as e:
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()

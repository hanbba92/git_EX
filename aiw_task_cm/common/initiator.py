import logging
import os.path
import pkg_resources
from pathlib import Path
from aiw_task_cm.file.file_manager_factory import FileManagerFactory


def init(task, workflow_id):
    """
    Init.
    :return:
    """
    init_logger(task, workflow_id)


def init_logger(task, workflow_id):
    """
    Init Logger.
    :return:
    """
    from aiw_task_cm.common.logger import register_logger
    global logger
    log_file_path = "./%s.log" % task
    path = Path(log_file_path)
    if not os.path.isdir(path.parent):
        os.makedirs(path.parent)
    fm = FileManagerFactory().get_instance('yaml')
    config_path = pkg_resources.resource_filename(__name__, '../metadata/config.yaml')
    #config_path = "/home/aiw/config/logconfig.yaml"

    config = fm.read(config_path)

    logger = register_logger(logging.DEBUG, config, task, workflow_id, log_file_path)


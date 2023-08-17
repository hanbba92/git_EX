import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from fluent import handler
import socket

backup_count = 10    # possible exceeded log file counts.
formatter = None
ext_formatter = None
int_formatter = None

# 로그 관리자
def init_formatter():
    """
    로그 포멧을 정의한다
    :param tp_id: Tp_Id.
    :return:
    """
    global formatter, ext_formatter, int_formatter
    hostname = socket.gethostname()
    formatter = logging.Formatter('[%(asctime)s | AIW-HT-TASK | TP-{} | PRO | %(levelname)s |'
                                  '%(filename)s:%(lineno)s] > %(message)s'.format(hostname))
    ext_formatter = logging.Formatter('[%(asctime)s | AIW-HT-TASK | {} | EXT | %(levelname)s |'
                                      '%(filename)s:%(lineno)s] > %(message)s'.format(hostname))
    int_formatter = logging.Formatter('[%(asctime)s | AIW-HT-TASK | {} | INT | %(levelname)s | '
                                      '%(filename)s:%(lineno)s] > %(message)s'.format(hostname))


def register_logger(level, config, task, workflow_id, path=None):
    """
    로그를 저장한다
    :param level: 로그 수준
    :param task: Task 명
    :param config: 설정 정보
    :param path: 로깅 위치
    :return: 로거
    """
    logger = logging.getLogger(task)
    logger.setLevel(level)
    init_formatter()

    if not logger.handlers:
        # TODO remove stream handler in production level.
        # stream_handler = create_handler(level)
        file_handler = create_handler(level, path)
        fluent_handler = create_fluent_handler(config['common']['logger'], task, workflow_id)
        # logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        logger.addHandler(fluent_handler)
    return logger


def create_handler(level, path=None):
    """
    Create Handler.
    :param level: Level.
    :param path: Path.
    :return: File handler.
    """
    if path is None:
        stream_handler = StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        return stream_handler
    else:
        file_handler = TimedRotatingFileHandler(path, when='midnight', interval=1, backupCount=backup_count, encoding="UTF-8")
        file_handler.suffix = "_%Y%m%d"
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        return file_handler


def create_fluent_handler(config, task, workflow_id):
    custom_format = {
        'hostname': '%(hostname)s',
        'module': '%(module)s',
        'level': '%(levelname)s',
        'task': f'{task}',
        'workflow_id': f'{workflow_id}'
    }

    fluent_handler = handler.FluentHandler('task', host=config['host'], port=config['port'])
    fluent_handler.setFormatter(handler.FluentRecordFormatter(custom_format))
    return fluent_handler

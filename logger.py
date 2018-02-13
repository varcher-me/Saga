import logging
import logging.handlers
import traceback


def create_logger(log_file, error_file):
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
    handler_error = logging.handlers.RotatingFileHandler(error_file, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
    handler_error.setLevel(logging.ERROR)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler.setFormatter(formatter)  # 为handler添加formatter
    handler_error.setFormatter(formatter)
    logger = logging.getLogger('tst')  # 获取名为tst的logger
    logger.addHandler(handler)  # 为logger添加handler
    logger.addHandler(handler_error)
    logger.setLevel(logging.DEBUG)
    return logger

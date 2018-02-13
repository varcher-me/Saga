import logging
import logging.handlers
import traceback
import configparser

config = configparser.ConfigParser()
config.read('saga.conf')
LOG_FILE = config.get('log', 'LOG_FILE')
ERROR_FILE = config.get('log', 'ERROR_FILE')
print(ERROR_FILE)
LOG_FILE = 'd:/temp/process.log'
ERROR_FILE = 'd:/temp/error.log'
print(ERROR_FILE)
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
handler_error = logging.handlers.RotatingFileHandler(ERROR_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
handler_error.setLevel(logging.ERROR)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter
handler_error.setFormatter(formatter)
logger = logging.getLogger('tst')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.addHandler(handler_error)
logger.setLevel(logging.DEBUG)

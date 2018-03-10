import configparser
import os
import logger


class SagaConnector:
    params = {}
    logger = None

    def __init__(self):
        self.load_param()
        self.build_logger()

    def load_param(self):
        config = configparser.ConfigParser()
        if os.path.exists("saga.conf"):
            config_file = 'saga.conf'
        elif os.path.exists("saga.conf.sample"):
            config_file = "saga.conf.sample"
        else:
            print("FATAL ERROR: config file cannot find.")
            exit(200)
        config.read(config_file)
        self.set_param('redis_ip', config.get('redis', 'redis_ip'))
        self.set_param('redis_port', config.getint('redis', 'redis_port'))
        self.set_param('redis_db', config.getint('redis', 'redis_db'))
        self.set_param('redis_token', config.get('redis', 'redis_token', raw=True))

        self.set_param('mysql_ip', config.get('mysql', 'mysql_ip'))
        self.set_param('mysql_port', config.getint('mysql', 'mysql_port'))
        self.set_param('mysql_user', config.get('mysql', 'mysql_user'))
        self.set_param('mysql_pass', config.get('mysql', 'mysql_pass', raw=True))
        self.set_param('mysql_db', config.get('mysql', 'mysql_db'))

        self.set_param('log_file', config.get('log', 'log_file'))
        self.set_param('error_file', config.get('log', 'error_file'))
        self.set_param('log_level', config.get('log', 'log_level'))
        print("Class["+self.__class__.__name__+"]Configure file loaded.")

    def build_logger(self):
        self.logger = logger.create_logger(self.get_param('log_file'), self.get_param('error_file'), self.get_param('log_level'))
        print("Class["+self.__class__.__name__+"]logger loaded.")

    def get_logger(self):
        return self.logger

    def set_param(self, key, value):
        self.params[key] = value

    def get_param(self, key):
        try:
            return self.params[key]
        except Exception as e:
            return None
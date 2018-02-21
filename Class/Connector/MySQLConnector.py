from Class.SagaClass import SagaClass
import pymysql


class MySQLConnector(SagaClass):
    __conn = None

    def __init__(self):
        SagaClass.__init__(self)

    def conn(self):
        self.__conn = pymysql.connect(host=self.get_param('mysql_ip'),
                                      port=self.get_param('mysql_port'),
                                      user=self.get_param('mysql_user'),
                                      passwd=self.get_param('mysql_pass'),
                                      db=self.get_param('mysql_db'),
                                      charset='utf8')
        print("MySQL Connect successfully.")

    def ping(self):
        self.__conn.ping()
        print("MySQL Ping successful.")

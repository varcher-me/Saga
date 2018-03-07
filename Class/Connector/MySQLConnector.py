from Class.SagaClass import SagaClass
import pymysql
import uuid


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

    def search_file(self, file_name, file_ext, file_size, file_sha, file_md5):
        cache_status = True
        cursor = self.__conn.cursor()
        cursor.execute("SELECT filename_server FROM filelist WHERE filename_ext = %s "
                       "AND file_size = %s AND file_sha = %s AND file_md5 = %s",
                       (file_ext, file_size, file_sha, file_md5))
        filename_server = cursor.fetchone()
        cursor.close()
        if filename_server is None:
            while True:
                filename_server = uuid.uuid1().hex
                if not self.is_exist_filename_server(filename_server):
                    break
            cursor = self.__conn.cursor()
            cursor.execute("INSERT INTO filelist "
                           "(filename_server, filename_secure,filename_ext,file_size,file_sha,file_md5) "
                           "VALUES (%s, %s, %s, %s, %s, %s)",
                           (filename_server, file_name, file_ext, file_size, file_sha, file_md5))
            cursor.close()
            cache_status = False
        else:
            filename_server = filename_server[0]
        return filename_server, cache_status

    def commit(self):
        self.__conn.commit()

    def rollback(self):
        self.__conn.rollback()

    def is_exist_filename_server(self, filename_server):
        cursor = self.__conn.cursor()
        cursor.execute("SELECT filename_server FROM filelist WHERE filename_server = %s", filename_server)
        row = cursor.rowcount
        cursor.close()
        if row != 0:
            return True
        else:
            return False



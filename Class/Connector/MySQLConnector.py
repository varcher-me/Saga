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

    def search_file(self, file_name, file_ext, file_size, file_sha, file_md5):
        cache_status = True
        cursor = self.__conn.cursor()
        cursor.execute("SELECT file_seq_no FROM filelist WHERE filename_ext = %s "
                       "AND file_size = %s AND file_sha = %s AND file_md5 = %s",
                       (file_ext, file_size, file_sha, file_md5))
        file_seq_no = cursor.fetchone()
        cursor.close()
        if file_seq_no is None:
            cursor = self.__conn.cursor()
            cursor.execute("INSERT INTO filelist (filename_secure,filename_ext,file_size,file_sha,file_md5) "
                           "VALUES (%s, %s, %s, %s, %s)", (file_name, file_ext, file_size, file_sha, file_md5))
            file_seq_no = cursor.lastrowid
            cursor.close()
            cache_status = False
        else:
            file_seq_no = file_seq_no[0]
        return file_seq_no, cache_status

    def commit(self):
        self.__conn.commit()

    def rollback(self):
        self.__conn.rollback()

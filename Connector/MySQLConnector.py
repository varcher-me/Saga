import datetime
import pymysql
from Connector.SagaConnector import SagaConnector


class MySQLConnector(SagaConnector):
    __conn = None

    def __init__(self):
        SagaConnector.__init__(self)

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
            return None
        else:
            return filename_server[0]

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

    def get_uuid_fileist(self, in_uuid):
        self.__conn.begin()
        cursor = self.__conn.cursor()
        cursor.execute("SELECT seq_no, filename_secure FROM history "
                       "WHERE uuid = %s AND process_status = 1 LIMIT 500 FOR UPDATE", in_uuid)
        filelist = cursor.fetchall()
        cursor.close()
        return filelist

    def update_status(self, uuid, seq_no, status, phase, comment):
        cursor = self.__conn.cursor()
        cursor.execute("UPDATE history "
                       "SET time_process = %s, process_status = %s, process_phase = %s, process_comment = %s "
                       "WHERE uuid = %s AND seq_no = %s",
                       (datetime.datetime.now(), status, phase, comment, uuid, seq_no))
        cursor.close()

    def update_postlist_status(self, uuid, status):
        cursor = self.__conn.cursor()
        cursor.execute("UPDATE postlist SET process_status = %s WHERE uuid = %s", (status, uuid))
        cursor.close()

    def update_filename_server(self, uuid, seq_no, filename):
        cursor = self.__conn.cursor()
        cursor.execute("UPDATE history SET filename_server = %s WHERE uuid = %s AND seq_no = %s",
                       (filename, uuid, seq_no))
        cursor.close()

    def insert_filelist(self, filename_server, file_name, file_ext, file_size, file_sha, file_md5):
        cursor = self.__conn.cursor()
        cursor.execute("INSERT INTO filelist "
                       "(filename_server, filename_secure,filename_ext,file_size,file_sha,file_md5) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (filename_server, file_name, file_ext, file_size, file_sha, file_md5))
        cursor.close()

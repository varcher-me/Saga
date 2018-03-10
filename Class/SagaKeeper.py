from Class.SagaFile.SagaFile import SagaFile
from Class.Handler.GdHandler import GdHandler
from Class.Handler.WordHandler import WordHandler
from Class.Connector.MySQLConnector import MySQLConnector
from Class.Connector.RedisConnector import RedisConnector
from Class.Configure.Configure import Configure
from Class.Exception.SagaException import *
from Class.SagaClass import SagaClass
import time
import Constants.Constants as CT
import os


class SagaKeeper(SagaClass):
    __gdHandler = None
    __wordHandler = None
    __configure = None
    __lastHeartTime = 0
    __heartInterval = 0

    def __init__(self):
        SagaClass.__init__(self)
        self.__heartInterval = self.get_param('heart_interval')
        self.__gdHandler = GdHandler()
        self.__wordHandler = WordHandler()
        self.set_mysql( MySQLConnector())
        self.mysql().conn()
        self.set_redis(RedisConnector())
        self.redis().setup()
        self.__configure = Configure()
        return

    def heart_beat(self):
        curr_time = time.time()
        if curr_time - self.__lastHeartTime > self.__heartInterval:
            self.__lastHeartTime = curr_time
            self.redis().set('HeartBeat', curr_time, self.__heartInterval * 3)
            print("HeartBeat setup to %s (%d)" % (time.ctime(curr_time), curr_time))
            self.mysql().ping()

    def do(self):
        path_init = self.get_param("path_init")
        sleep_interval = self.get_param("sleep_interval")

        self.heart_beat()
        while True:
            (uuid_queue, uuid) = self.redis().blpop("INIT_QUEUE", self.__heartInterval)
            if "INIT_QUEUE" == uuid_queue:
                print("Get jobid = %s" % uuid)
                file_in_uuid = self.mysql().get_uuid_fileist(uuid)
                for file_record in file_in_uuid:
                    file_seq_no = file_record[0]
                    file_secure_name = file_record[1]
                    file = SagaFile(path_init, file_secure_name, uuid, file_seq_no)
                    try:
                        file.set_mysql(self.mysql())
                        file.set_redis(self.redis())
                        file_ext = file.get_file_ext()

                        if ".gd" == file_ext:
                            file.set_handler(self.__gdHandler)
                        if ".doc" == file_ext or ".docx" == file_ext:
                            file.set_handler(self.__wordHandler)
                        else:
                            except_string = "Unknown ext for file: %s" % (file.get_path_name())
                            raise FileExtUnknownException(except_string)

                        file.process()

                    except FileExtUnknownException as e:
                        file.update_process_status(CT.CONSTANT_PROCESS_STATUS_FAIL, "INIT", "Unknown ext")
                        self.mysql().commit()
                        self.get_logger().log(str(e))

                    except Exception as e:
                        except_string = "FATAL ERROR: something error, exception is >>>" + str(e) + "<<<."
                        print(except_string)
                        self.redis().lpush("INIT_QUEUE", uuid)  # resave the uuid as the first job
                        self.get_logger().fatal(except_string)
                        raise e
                self.mysql().commit()
            self.heart_beat()

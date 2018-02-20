from Class.SagaFile.SagaFile import SagaFile
from Class.Handler.GdHandler import GdHandler
from Class.Exception.SagaException import *
from Class.SagaClass import SagaClass
import redis
import time
import os
import shutil


class SagaKeeper(SagaClass):
    __gdHandler = GdHandler()
    __lastHeartTime = 0
    __heartInterval = 0

    def __init__(self):
        SagaClass.__init__(self)
        self.__heartInterval = self.get_param('heart_interval')
        return

    def set_heart_beat(self):
        curr_time = time.time()
        if curr_time - self.__lastHeartTime > self.__heartInterval:
            self.__lastHeartTime = curr_time
            self.redis_set('HeartBeat', curr_time, self.__heartInterval * 3)
            print("HeartBeat setup to %s (%d)" % (time.ctime(curr_time), curr_time))

    def do(self):
        path_init = self.get_param("path_init")
        sleep_interval = self.get_param("sleep_interval")

        self.set_heart_beat()
        while True:
            for i in os.walk(path_init):        # todo: 从redis队列中获取要处理的id，然后去MYSQL里取文件名
                for fileName in i[2]:
                    try:
                        file = SagaFile(path_init, fileName)
                        file_ext = file.get_file_ext()
                        if ".gd" == file_ext:
                            file.set_handler(self.__gdHandler)
                        else:
                            except_string = "Unknown ext for file: %s" % (file.get_path_name())
                            raise FileExtUnknownException(except_string)
                        file.process()
                    except Exception as e:
                        except_string = "FATAL ERROR: something error, exception is >>>" + str(e) + "<<<."
                        print(except_string)
                        self.get_logger().fatal(except_string)

            self.set_heart_beat()
            print("Process finished or no file, sleep %d seconds." % sleep_interval)
            time.sleep(sleep_interval)

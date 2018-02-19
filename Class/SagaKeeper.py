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

    def __init__(self):
        SagaClass.__init__(self)
        return

    def do(self):
        path_init = self.get_param("path_init")
        while True:
            for i in os.walk(path_init):
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
            print("Process finished or no file, sleep 10 seconds.")
            time.sleep(10)

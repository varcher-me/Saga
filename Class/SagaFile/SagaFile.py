import os
import time
import shutil
from Class.SagaClass import SagaClass
from Class.Exception.SagaException import *
import filetype


class SagaFile(SagaClass):
    __file_path = ''
    __file_name = ''
    __file_handler = None

    def __init__(self, file_path, file_name):
        SagaClass.__init__(self)
        self.__file_path = file_path
        self.__file_name = file_name
        self.__file_name_raw, self.__file_name_ext = os.path.splitext(self.__file_name)

    def get_path_name(self):
        return self.__file_path + self.__file_name

    def get_path(self):
        return self.__file_path

    def get_name(self):
        return self.__file_name

    def get_file_ext(self):
        raw_name, ext = os.path.splitext(self.__file_name)
        return ext

    def get_file_raw_name(self):
        raw_name, ext = os.path.splitext(self.__file_name)
        return raw_name

    def set_handler(self, handler):
        self.__file_handler = handler
        self.__file_handler.set_file_obj(self)
        return

    def output_file_move(self):
        path_printed = self.get_param('path_printed')  # PDF Creator创建的文件所在目录
        file_printed = self.get_param('file_printed')  # PDF Creator创建的文件名
        path_result = self.get_param('path_result')  # 打印后文件移动到的位置
        printed_pathname = os.path.join(path_printed, file_printed)  # PDF Creator创建后文件的完整路径+文件名
        moved_file = os.path.join(path_result, self.get_name() + '.pdf')  # 文件重命名后移动到目标位置后的完整路径+文件名

        # 移动文件
        try:
            self.move_file(printed_pathname, moved_file)
        except WaitFileTimeOutException as e:
            self.logger.fatal(str(e))
            raise e
        except Exception as e:
            exception_str = "FATAL ERROR: move file failed, exception is " + str(e) + ", process terminated."
            self.logger.fatal(exception_str)
            raise FileMoveFailedException(exception_str)
        return

    def initial_file_move(self):
        path_init = self.get_param("path_init")
        path_processed = self.get_param("path_processed")
        file_init = os.path.join(path_init, self.get_name())
        # 移动文件
        try:
            self.move_file(file_init, path_processed)
        except WaitFileTimeOutException as e:
            self.logger.fatal(str(e))
            raise e
        except Exception as e:
            exception_str = "FATAL ERROR: move file failed, exception is " + str(e) + ", process terminated."
            self.logger.fatal(exception_str)
            raise FileMoveFailedException(exception_str)
        return

    def process(self):
        # todo: 移入
        try:
            self.__file_handler.check_file_type()
            self.__file_handler.process()
            self.output_file_move()
            self.initial_file_move()
        except FileTypeErrorException as e:
            self.finalize(False, "FILE_TYPE_CHECK", str(e))
        except (FileOpenFailedException, FileOperaException) as e:
            self.finalize(False, "FILE_PROCESS", str(e))
        except (WaitFileTimeOutException, FileMoveFailedException) as e:
            self.finalize(False, "FILE_FINAL_MOVE", str(e))
        # todo：输出处理，统计
        return

    def finalize(self, is_success=True, status_string=None, status_comment=None):
        if is_success:
            pass
        else:
            print(status_string)
            print(status_comment)
        pass

    # 下面都是工具方法
    def move_file(self, origin_file, new_file):
        self.wait_for_file(origin_file)
        if os.path.isfile(new_file):
            os.remove(new_file)
        shutil.move(origin_file, new_file)
        print("File %s moved to %s ." % (origin_file, new_file))

    def wait_for_file(self, full_file):
        retry_seconds = self.get_param('retry_seconds')
        retry_interval = self.get_param('retry_interval')
        retry_time = retry_seconds / retry_interval
        while retry_time > 0:
            time.sleep(retry_interval)
            if os.path.isfile(full_file):
                try:
                    time.sleep(retry_interval)
                    fp = open(full_file, 'a')
                    fp.close()
                    return True
                except:
                    retry_time -= 1
            else:
                retry_time -= 1
        raise WaitFileTimeOutException("Wait for file " + full_file + " appear timed out.")

    def get_mime_type(self):
        try:
            kind = filetype.guess(self.get_path_name())
        except Exception:
            return None
        return kind

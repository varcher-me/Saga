import os
from Class.SagaClass import SagaClass


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

    def move_file(self, new_path):
        # todo: finish move function
        return;

    def set_handler(self, handler):
        self.__file_handler = handler
        return

    def process(self):
        self.__file_handler.process(self)
        return

from Class.SagaClass import *
import abc
import time
import win32gui
import win32api
import win32con
from Class.Exception.SagaException import *


class AbstractHandler(SagaClass, metaclass=abc.ABCMeta):
    __hwnd = None
    __file_obj = None
    __file_type_in_handler = None

    def __init__(self):
        SagaClass.__init__(self)
        return

    def set_hwnd(self, hwnd):
        self.__hwnd = hwnd
        return

    def get_hwnd(self):
        return self.__hwnd

    def set_file_obj(self, file_obj):
        self.__file_obj = file_obj
        return

    def get_file_obj(self):
        return self.__file_obj

    def set_file_type_in_handler(self, file_type_in_handler):
        self.__file_type_in_handler = file_type_in_handler
        return

    def process(self):
        try:
            self.open()
            self.pseudo_print()
            self.clean()
        except Exception as e:
            self.force_clean()
            raise e
        return

    @abc.abstractmethod
    def open(self):
        return

    @abc.abstractmethod
    def pseudo_print(self):
        return

    @abc.abstractmethod
    def clean(self):
        return

    def check_file_type(self):
        mime_type = self.__file_obj.get_mime_type()
        if mime_type != self.__file_type_in_handler:
            raise FileTypeErrorException("File Type Error for File: [%s], %s is needed, but %s is given"
                                         % (
                                             self.__file_obj.get_path_name(),
                                             self.__file_type_in_handler,
                                             mime_type
                                         ))
        return

    def get_window(self, hwnd_father, hwnd_child_after, window_class, window_context, no_wait=False):
        retry_interval = self.get_param('retry_interval')
        if no_wait:
            retry_time = 1
        else:
            retry_seconds = self.get_param('retry_seconds')
            retry_time = retry_seconds / retry_interval
        while retry_time > 0:
            time.sleep(retry_interval)
            hwnd = win32gui.FindWindowEx(hwnd_father, hwnd_child_after, window_class, window_context)
            if hwnd:
                return hwnd
            else:
                retry_time -= 1
        raise WaitWindowTimeOutException("Wait for window appear timed out.")

    def get_window_ex(self, hwnd_father, hwnd_child_after,
                      window_class1, window_context1,
                      window_class2, window_context2):
        retry_seconds = self.get_param('retry_seconds')
        retry_interval = self.get_param('retry_interval')
        retry_time = retry_seconds / retry_interval
        while retry_time > 0:
            time.sleep(retry_interval)
            hwnd1 = win32gui.FindWindowEx(hwnd_father, hwnd_child_after, window_class1, window_context1)
            hwnd2 = win32gui.FindWindowEx(hwnd_father, hwnd_child_after, window_class2, window_context2)
            if hwnd1 or hwnd2:
                return hwnd1, hwnd2
            else:
                retry_time -= 1
        raise WaitWindowTimeOutException("Wait for window appear timed out.")

    def wait_window_disappear(self, window_hwnd):
        retry_seconds = self.get_param('retry_seconds')
        retry_interval = self.get_param('retry_interval')
        retry_time = retry_seconds / retry_interval
        while retry_time > 0:
            time.sleep(0.2)
            result = win32gui.IsWindow(window_hwnd)
            if result:
                retry_time -= 1
            else:
                return True
        raise WaitWindowDisappearTimeOutException("Wait for window disappear timed out.")

    def force_clean(self):
        win32api.SendMessage(self.get_hwnd(), win32con.WM_CLOSE, 0, 0)
        return

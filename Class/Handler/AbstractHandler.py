from Class.SagaClass import SagaClass
import abc
import time
import win32gui


class AbstractHandler(SagaClass, metaclass=abc.ABCMeta):
    __hwnd = None

    def __init__(self):
        SagaClass.__init__(self)
        return

    def set_hwnd(self, hwnd):
        self.__hwnd = hwnd;
        return

    def get_hwnd(self):
        return self.__hwnd

    def process(self, file_obj):
        self.open(file_obj)
        self.pseudo_print(file_obj)
        self.clean(file_obj)
        return

    @abc.abstractmethod
    def open(self, file_obj):
        return

    @abc.abstractmethod
    def pseudo_print(self, file_obj):
        return

    @abc.abstractmethod
    def clean(self, file_obj):
        return

    def get_window(self, hwnd_father, hwnd_child_after, window_class, window_context):
        retry_seconds = self.get_param('retry_seconds')
        retry_interval = self.get_param('retry_interval')
        retry_time = retry_seconds / retry_interval
        hwnd = None
        while retry_time > 0:
            time.sleep(retry_interval)
            hwnd = win32gui.FindWindowEx(hwnd_father, hwnd_child_after, window_class, window_context)
            if hwnd:
                break
            else:
                retry_time -= 1
        if hwnd:
            return hwnd
        else:
            raise FileOperaException("Wait for window appear timed out.")

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
        raise FileOperaException("Wait for window disappear timed out.")
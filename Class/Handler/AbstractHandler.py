import abc
import time
import win32gui


class AbstractHandler(metaclass=abc.ABCMeta):
    __hwnd = None

    def __init__(self):
        return

    @abc.abstractmethod
    def open(self, file_obj):
        return

    @abc.abstractmethod
    def process(self, file_obj):
        return

    @abc.abstractmethod
    def clean(self, file_obj):
        return

    @staticmethod
    def get_window(hwnd_father, hwnd_child_after, window_class, window_context):
        retry_time = retry_seconds / retry_interval
        while retry_time > 0:
            time.sleep(0.2)
            hwnd = win32gui.FindWindowEx(hwnd_father, hwnd_child_after, window_class, window_context)
            if hwnd:
                break
            else:
                retry_time -= 1
        if hwnd:
            return hwnd
        else:
            raise FileOperaException("Wait for window appear timed out.")

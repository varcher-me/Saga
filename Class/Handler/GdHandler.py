import win32api
import win32gui
import win32con
from Class.Handler.AbstractHandler import AbstractHandler
from Class.Exception.SagaException import *


class GdHandler(AbstractHandler):
    def __init__(self):
        AbstractHandler.__init__(self)
        self.set_file_type_in_handler("gd")
        hwnd = self.get_window(None, None, None, 'SEP Reader', True)
        if hwnd:
            self.set_hwnd(hwnd)
        return

    def open(self):
        file_path_name = self.get_file_obj().get_path_name()
        file_path = self.get_file_obj().get_path()
        file_name = self.get_file_obj().get_name()
        print("Starting processing " + file_path_name)
        win32api.ShellExecute(0, 'open', file_path + file_name, '', '', 1)
        # hwnd = self.get_hwnd()
        # if hwnd:
        #     fail_hwnd = self.get_window(None, None, None, 'Reader', True)
        # else:
        hwnd, fail_hwnd = self.get_window_ex(None, None, None, 'SEP Reader - [' + file_name + ']', None,
                                             'Reader')
        if fail_hwnd:
            win32gui.SetForegroundWindow(fail_hwnd)
            win32api.keybd_event(13, 0, 0, 0)  # Enter
            win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
            try:
                self.wait_window_disappear(fail_hwnd)
            except WaitWindowTimeOutException as e:
                win32api.SendMessage(fail_hwnd, win32con.WM_CLOSE, 0, 0)
                # logger.error("File [" + raw_file + "] print-window-disappear timed out; WM_CLOSE signal sent.")
            raise FileOpenFailedException("File %s Open Failed." % (self.get_file_obj().get_path_name()))
        self.set_hwnd(hwnd)
        # if 0 == hwnd_main_sep:
        #     # logger.fatal("FATAL ERROR: SEP Reader Window not found! program terminated.")
        #     exit(100)
        return

    def pseudo_print(self):
        # 发送打印指令
        win32gui.SetForegroundWindow(self.get_hwnd())
        win32api.keybd_event(17, 0, 0, 0)  # Ctrl
        win32api.keybd_event(80, 0, 0, 0)  # P
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(80, 0, win32con.KEYEVENTF_KEYUP, 0)

        # 等待打印窗体、按回车并判断窗体消失
        hwnd_printer = self.get_window(None, None, None, 'SEP Reader')
        if hwnd_printer is None:
            raise FileOperaException("Wait for SEP Reader Print Window timed out.")
        win32gui.SetForegroundWindow(hwnd_printer)
        win32api.keybd_event(13, 0, 0, 0)  # Enter
        win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
        try:
            self.wait_window_disappear(hwnd_printer)
        except WaitWindowDisappearTimeOutException as e:
            # logger.error("File [" + raw_file + "] print-window-disappear timed out; WM_CLOSE signal sent.")
            win32api.SendMessage(hwnd_printer, win32con.WM_CLOSE, 0, 0)
        return

    def clean(self):
        # 窗口清理（SEP为关闭文件，保留程序窗口）
        win32gui.SetForegroundWindow(self.get_hwnd())
        win32api.keybd_event(17, 0, 0, 0)  # Ctrl
        win32api.keybd_event(87, 0, 0, 0)  # W
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(87, 0, win32con.KEYEVENTF_KEYUP, 0)
        # win32api.SendMessage(hwnd_main, win32con.WM_CLOSE, 0, 0)
        return

    def check_file_type(self):
        # GD文件无法获取MIME特征，直接跳过检查
        return
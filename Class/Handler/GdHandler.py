import win32api
import win32gui
import win32con
from Class.Handler.AbstractHandler import AbstractHandler


class GdHandler(AbstractHandler):
    def __init__(self):
        AbstractHandler.__init__(self)
        return

    def open(self, file_obj):
        file_path_name = file_obj.get_path_name()
        file_path = file_obj.get_path()
        file_name = file_obj.get_name()
        print("Starting processing " + file_path_name)
        win32api.ShellExecute(0, 'open', file_path + file_name, '', '', 1)
        hwnd = self.get_window(None, None, None, 'SEP Reader - [' + file_name + ']')
        self.set_hwnd(hwnd)
        # if 0 == hwnd_main_sep:
        #     # logger.fatal("FATAL ERROR: SEP Reader Window not found! program terminated.")
        #     exit(100)
        return

    def pseudo_print(self, file_obj):
        # 发送打印指令
        win32gui.SetForegroundWindow(self.get_hwnd())
        win32api.keybd_event(17, 0, 0, 0)  # Ctrl
        win32api.keybd_event(80, 0, 0, 0)  # P
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(80, 0, win32con.KEYEVENTF_KEYUP, 0)

        # 等待打印窗体、按回车并判断窗体消失
        hwnd_printer = self.get_window(None, None, None, 'SEP Reader')
        win32gui.SetForegroundWindow(hwnd_printer)
        win32api.keybd_event(13, 0, 0, 0)  # Enter
        win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
        if not self.wait_window_disappear(hwnd_printer):
            # logger.error("File [" + raw_file + "] print-window-disappear timed out; WM_CLOSE signal sent.")
            win32api.SendMessage(hwnd_printer, win32con.WM_CLOSE, 0, 0)
        return

    def clean(self, file_obj):
        # 窗口清理（SEP为关闭文件，保留程序窗口）
        win32gui.SetForegroundWindow(self.get_hwnd())
        win32api.keybd_event(17, 0, 0, 0)  # Ctrl
        win32api.keybd_event(87, 0, 0, 0)  # W
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(87, 0, win32con.KEYEVENTF_KEYUP, 0)
        # win32api.SendMessage(hwnd_main, win32con.WM_CLOSE, 0, 0)
        return

import win32api
from Class.Handler.AbstractHandler import AbstractHandler
from Global import g


class GdHandler(AbstractHandler):
    def __init__(self):
        super(GdHandler, self).__init__()
        return

    def open(self, file_obj):
        file_path_name = file_obj.get_path_name()
        file_path = file_obj.get_path()
        file_name = file_obj.get_name()
        print("Starting processing " + file_path_name)
        win32api.ShellExecute(0, 'open', file_path + file_name, '', '', 1)
        hwnd_main_sep = super(GdHandler, self).get_window(None, None, None, 'SEP Reader - [' + file_name + ']')
        if 0 == hwnd_main_sep:
            # logger.fatal("FATAL ERROR: SEP Reader Window not found! program terminated.")
            exit(100)
        return

    def process(self, file_obj):
        global a
        print(a)
        self.open(self, file_obj)
        return

    def clean(self, file_obj):
        return

from Class.Handler.AbstractHandler import AbstractHandler
from Class.Exception.SagaException import *
from win32com.client import constants, gencache, DispatchEx
import pywintypes


class PowerPointHandler(AbstractHandler):
    __w = None
    __ppt = None

    def __init__(self):
        AbstractHandler.__init__(self)
        self.set_file_type_in_handler("powerpoint")
        # makepy.py - i "Microsoft Excel 16.0 Object Library"
        # gencache.EnsureModule('{00020813-0000-0000-C000-000000000046}', 0, 1, 9)
        gencache.EnsureDispatch('PowerPoint.Application')

    def open(self, init_path_name):
        print("PowerPoint open for %s" % init_path_name)
        self.__w = DispatchEx("PowerPoint.Application")
        try:
            self.__ppt = self.__w.Presentations.Open(init_path_name,
                                                     ReadOnly=True,
                                                     WithWindow=False)
        except pywintypes.com_error as e:
            raise FileOpenFailedException("Open PowerPoint file failed.")

    def output(self, result_path_name):
        print("PowerPoint output for %s" % result_path_name)
        self.__ppt.ExportAsFixedFormat(result_path_name,
                                       FixedFormatType=2,
                                       PrintRange=None)

    def clean(self):
        print("clean")
        self.__w.Quit()

    def force_clean(self):
        self.clean()


from Class.Handler.AbstractHandler import AbstractHandler
from Class.Exception.SagaException import *
from win32com.client import constants, gencache, DispatchEx
import pywintypes


class ExcelHandler(AbstractHandler):
    __w = None
    __xls = None

    def __init__(self):
        AbstractHandler.__init__(self)
        self.set_file_type_in_handler("excel")
        # makepy.py - i "Microsoft Excel 16.0 Object Library"
        gencache.EnsureModule('{00020813-0000-0000-C000-000000000046}', 0, 1, 9)

    def open(self, init_path_name):
        print("Excel open for %s" % init_path_name)
        self.__w = DispatchEx("Excel.Application")
        try:
            self.__xls = self.__w.Workbooks.Open(init_path_name, ReadOnly=1)
        except pywintypes.com_error as e:
            raise FileOpenFailedException("Open excel file failed.")

    def output(self, result_path_name):
        print("Excel output for %s" % result_path_name)
        self.__xls.ExportAsFixedFormat(constants.xlTypePDF, result_path_name, Quality=constants.xlQualityStandard,
                                       OpenAfterPublish=False)

    def clean(self):
        print("clean")
        self.__w.Quit()

    def force_clean(self):
        self.clean()


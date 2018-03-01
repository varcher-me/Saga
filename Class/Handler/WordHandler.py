import sys, os
import win32api
import win32gui
import win32con
from Class.Handler.AbstractHandler import AbstractHandler
from Class.Exception.SagaException import *
from win32com.client import Dispatch, constants, gencache
import pywintypes


class WordHandler(AbstractHandler):
    __w = None
    __doc = None
    __output_file = None

    def __init__(self):
        AbstractHandler.__init__(self)
        self.set_file_type_in_handler("word")
        gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 7)
        path_printed = self.get_param('path_printed')  # PDF Creator创建的文件所在目录，这里是模拟
        file_printed = self.get_param('file_printed')  # PDF Creator创建的文件名，这里是模拟
        self.__output_file = os.path.join(path_printed, file_printed)

        return

    def open(self):
        self.__w = Dispatch("Word.Application")
        try:
            self.__doc = self.__w.Documents.Open(self.get_file_obj().get_path_name(), ReadOnly=1)
        except pywintypes.com_error as e:
            raise FileOpenFailedException("Open word file failed.")

    def pseudo_print(self):
        self.__doc.ExportAsFixedFormat(self.__output_file, constants.wdExportFormatPDF,
                                       Item=constants.wdExportDocumentContent,
                                       CreateBookmarks=constants.wdExportCreateHeadingBookmarks)

    def clean(self):
            self.__w.Quit(constants.wdDoNotSaveChanges)

    def force_clean(self):
            self.clean()


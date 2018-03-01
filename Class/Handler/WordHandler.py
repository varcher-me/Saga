import sys, os
import win32api
import win32gui
import win32con
from Class.Handler.AbstractHandler import AbstractHandler
from Class.Exception.SagaException import *
from win32com.client import Dispatch, constants, gencache


class WordHandler(AbstractHandler):
    __w = None
    __doc = None
    __output_file = None

    def __init__(self):
        AbstractHandler.__init__(self)
        self.set_file_type_in_handler("word")
        gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 7)
        self.__w = Dispatch("Word.Application")
        path_printed = self.get_param('path_printed')  # PDF Creator创建的文件所在目录，这里是模拟
        file_printed = self.get_param('file_printed')  # PDF Creator创建的文件名，这里是模拟
        self.__output_file = os.path.join(path_printed, file_printed)

        return

    def open(self):
        self.__doc = self.__w.Documents.Open(self.get_file_obj().get_path_name(), ReadOnly=1)

    def pseudo_print(self):
        self.__doc.ExportAsFixedFormat(self.__output_file, constants.wdExportFormatPDF,
                                       Item=constants.wdExportDocumentWithMarkup,
                                       CreateBookmarks=constants.wdExportCreateHeadingBookmarks)

    def clean(self):
            self.__w.Quit(constants.wdDoNotSaveChanges)

    def force_clean(self):
            self.clean()


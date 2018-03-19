from Class.Handler.AbstractHandler import AbstractHandler
from Class.Exception.SagaException import *
from win32com.client import constants, gencache, DispatchEx
import pywintypes


class WordHandler(AbstractHandler):
    __w = None
    __doc = None

    def __init__(self):
        AbstractHandler.__init__(self)
        self.set_file_type_in_handler("word")
        gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 7)

    def open(self, init_path_name):
        print("Word open for %s" % init_path_name)
        self.__w = DispatchEx("Word.Application")
        try:
            self.__doc = self.__w.Documents.Open(init_path_name, ReadOnly=1)
        except pywintypes.com_error as e:
            raise FileOpenFailedException("Open word file failed.")

    def output(self, result_path_name):
        print("Word output for %s" % result_path_name)
        self.__doc.ExportAsFixedFormat(result_path_name, constants.wdExportFormatPDF,
                                       Item=constants.wdExportDocumentContent,
                                       CreateBookmarks=constants.wdExportCreateHeadingBookmarks)

    def clean(self):
        print("clean")
        self.__w.Quit(constants.wdDoNotSaveChanges)

    def force_clean(self):
        self.clean()


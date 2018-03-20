import time
from Class.Exception.SagaException import *
from Class.SagaFile.SagaFile import SagaFile
import Constants.Constants as CT


class SagaQueue(SagaClass):
    uuid = None
    GDHandler = None
    WordHandler = None
    ExcelHandler = None
    PowerPointHandler = None

    def __init__(self, uuid):
        SagaClass.__init__(self)
        self.uuid = uuid

    def set_gdhandler(self, gdhandler):
        self.GDHandler = gdhandler

    def set_wordhandler(self, wordhandler):
        self.WordHandler = wordhandler

    def set_excelhandler(self, handler):
        self.ExcelHandler = handler

    def set_powerpointhandler(self, handler):
        self.PowerPointHandler = handler

    def process(self):
        uuid = self.uuid
        file_in_uuid = self.mysql().get_uuid_fileist(uuid)
        path_init = self.get_param("path_init")
        for file_record in file_in_uuid:
            file_seq_no = file_record[0]
            file_secure_name = file_record[1]
            file = SagaFile(path_init, file_secure_name, uuid, file_seq_no)
            try:
                file.set_mysql(self.mysql())
                file.set_redis(self.redis())
                file_ext = file.get_file_ext()
                if ".gd" == file_ext:
                    file.set_handler(self.GDHandler)
                elif ".doc" == file_ext or ".docx" == file_ext:
                    file.set_handler(self.WordHandler)
                elif ".xls" == file_ext or ".xlsx" == file_ext:
                    file.set_handler(self.ExcelHandler)
                elif ".ppt" == file_ext or ".pptx" == file_ext:
                    file.set_handler(self.PowerPointHandler)
                else:
                    except_string = "Unknown ext for file: %s" % (file.get_path_name())
                    raise FileExtUnknownException(except_string)

                file.process()

            except FileExtUnknownException as e:
                file.update_process_status(CT.CONSTANT_PROCESS_STATUS_FAIL, "INIT", "Unknown ext")
                self.mysql().commit()
                self.get_logger().warning(str(e))

        self.mysql().commit()

    def load(self):
        self.mysql().update_postlist_status(self.uuid, CT.CONSTANT_PROCESS_STATUS_LOADED)
        self.mysql().commit()

    def done(self):
        self.mysql().update_postlist_status(self.uuid, CT.CONSTANT_PROCESS_STATUS_SUCCESS)
        self.mysql().commit()

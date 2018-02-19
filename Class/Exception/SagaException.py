from Class.SagaClass import SagaClass


class SagaException(Exception, SagaClass):
    def __init__(self, arg):
        Exception.__init__(self, arg)
        SagaClass.__init__(self)


class FileOperaException(SagaException):
    pass


class FileTypeErrorException(SagaException):
    pass


class FileExtUnknownException(SagaException):
    pass


class FileOpenFailedException(SagaException):
    pass


class FileMoveFailedException(SagaException):
    pass


class WaitFileTimeOutException(SagaException):
    pass


class WaitWindowTimeOutException(SagaException):
    pass


class WaitWindowDisappearTimeOutException(SagaException):
    pass


from Class.SagaClass import SagaClass


class SagaException(Exception, SagaClass):
    def __init__(self, arg):
        Exception.__init__(self, arg)
        SagaClass.__init__(self)


class FileOperaException(SagaException):
    pass


class FileTypeErrorException(SagaException):
    pass


class FileOpenFailedException(SagaException):
    pass


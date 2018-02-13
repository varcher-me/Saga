import abc


class AbstractHandler(metaclass=abc.ABCMeta):
    __hwnd = None

    @abc.abstractmethod
    def open(self):
        return

    @abc.abstractmethod
    def process(self):
        return

    @abc.abstractmethod
    def clean(self):
        return

    def move(self):

from Class.SagaFile.SagaFile import SagaFile
from Class.Handler.GdHandler import GdHandler
from Class.SagaClass import SagaClass

file = SagaFile('D:/temp/init/', '关于开展2017年信息技术标准化工作检查的通知.gd')

handler = GdHandler()

file.set_handler(handler)
file.process()


from Class.SagaFile.SagaFile import SagaFile
from Class.Handler.GdHandler import GdHandler
import win32gui

file = SagaFile('D:/temp/init/', '关于开展2017年信息技术标准化工作检查的通知.gd')
file = SagaFile('D:/', '无标题.png.gd')

handler = GdHandler()

file.set_handler(handler)
file.process()
file.check_file_type()



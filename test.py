import Class.SagaFile.SagaFile as SagaFile
import Class.Handler.testHandler as TestHandler
import Class.Handler.GdHandler as GdHandler
from Global import g

file = SagaFile.SagaFile('d:/temp/', 'hello.txt')

handler = GdHandler.GdHandler

file.set_handler(handler)
file.process()


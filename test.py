import Class.SagaFile.SagaFile as SagaFile
import Class.Handler.GdHandler as GdHandler

file = SagaFile.SagaFile('d:/temp/', 'hello.txt')

handler = GdHandler.GdHandler

file.set_handler(handler)
file.process()


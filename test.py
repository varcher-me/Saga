from Class.SagaFile.SagaFile import SagaFile
from Class.Handler.GdHandler import GdHandler
from Class.Connector.RedisConnector import RedisConnector
from Class.Connector.MySQLConnector import MySQLConnector

redis = RedisConnector()
redis.setup()
mysql = MySQLConnector()
mysql.conn()

a = mysql.get_uuid_fileist("TEST")

print(type(a[0]))

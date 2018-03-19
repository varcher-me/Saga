import time
from Connector.RedisConnector import RedisConnector
from Class.Configure.Configure import Configure
from Class.Exception.SagaException import *
from Class.Handler.GdHandler import GdHandler
from Class.Handler.WordHandler import WordHandler
from Class.SagaClass import SagaClass
from Class.SagaQueue.SagaQueue import SagaQueue
from Connector.MySQLConnector import MySQLConnector


class SagaKeeper(SagaClass):
    __gdHandler = None
    __wordHandler = None
    __configure = None
    __lastHeartTime = 0
    __heartInterval = 0

    def __init__(self):
        SagaClass.__init__(self)
        self.__heartInterval = self.get_param('heart_interval')
        self.__gdHandler = GdHandler()
        self.__wordHandler = WordHandler()
        self.set_mysql(MySQLConnector())
        self.mysql().conn()
        self.set_redis(RedisConnector())
        self.redis().setup()
        self.__configure = Configure()
        return

    def heart_beat(self):
        curr_time = time.time()
        if curr_time - self.__lastHeartTime > self.__heartInterval:
            self.__lastHeartTime = curr_time
            self.redis().set('HeartBeat', curr_time, self.__heartInterval * 3)
            print("HeartBeat setup to %s (%d)" % (time.ctime(curr_time), curr_time))
            self.mysql().ping()

    def do(self):
        while True:
            self.heart_beat()   # todo 增加未完成列表继续处理
            (uuid_queue, uuid) = self.redis().blpop("INIT_QUEUE", self.__heartInterval)
            if "INIT_QUEUE" == uuid_queue:
                print("Get jobid = %s" % uuid)
                try:
                    saga_queue = SagaQueue(uuid)
                    saga_queue.set_mysql(self.mysql())
                    saga_queue.set_redis(self.redis())
                    saga_queue.set_gdhandler(self.__gdHandler)
                    saga_queue.set_wordhandler(self.__wordHandler)

                    saga_queue.load()
                    saga_queue.process()
                    saga_queue.done()

                except Exception as e:
                    except_string = "FATAL ERROR: something error, exception is >>>" + str(e) + "<<<."
                    print(except_string)
                    self.redis().lpush("INIT_QUEUE", uuid)  # resave the uuid as the first job
                    self.get_logger().fatal(except_string)
                    raise e

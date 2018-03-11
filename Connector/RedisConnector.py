import redis
from Connector.SagaConnector import SagaConnector


class RedisConnector(SagaConnector):
    __redisConnection = None

    def __init__(self):
        SagaConnector.__init__(self)

    def setup(self):      # todo redis链接后续建立connector
        redis_host = self.get_param('redis_ip')
        redis_port = self.get_param('redis_port')
        redis_db = self.get_param('redis_db')
        redis_token = self.get_param('redis_token')
        if redis_token == "":
            self.__redisConnection = redis.Redis(host=redis_host,
                                                 port=redis_port,
                                                 db=redis_db,
                                                 decode_responses=True)
        else:
            self.__redisConnection = redis.Redis(host=redis_host,
                                                 port=redis_port,
                                                 db=redis_db,
                                                 password=redis_token,
                                                 decode_responses=True)

    def set(self, key, value, ex=0):
        if self.__redisConnection is None:
            self.setup()
        if 0 == ex:
            self.__redisConnection.set(key, value)
        else:
            self.__redisConnection.set(key, value, ex)

    def get(self, key):
        return self.__redisConnection.get(key)

    def rpush(self, key, value):
        if self.__redisConnection is None:
            self.setup()
        self.__redisConnection.rpush(key, value)

    def lpush(self, key, value):
        if self.__redisConnection is None:
            self.setup()
        self.__redisConnection.lpush(key, value)

    def blpop(self, key, ex=0) -> tuple:
        if self.__redisConnection is None:
            self.setup()
        value = self.__redisConnection.blpop(key, ex)
        if value is None:
            return None, None
        else:
            return value

import redis
from Class.SagaClass import SagaClass


class RedisConnector(SagaClass):
    __redisConnection = None

    def __init__(self):
        SagaClass.__init__(self)

    def redis_setup(self):      # todo redis链接后续建立connector
        redis_host = self.get_param('redis_ip')
        redis_port = self.get_param('redis_port')
        redis_db = self.get_param('redis_db')
        redis_token = self.get_param('redis_token')
        self.__redisConnection = redis.Redis(host=redis_host,
                                             port=redis_port,
                                             db=redis_db,
                                             password=redis_token,
                                             decode_responses=True)

    def redis_set(self, key, value, ex=0):
        if self.__redisConnection is None:
            self.redis_setup()
        self.__redisConnection.set(key, value, ex)

    def redis_get(self, key):
        return self.__redisConnection.get(key)

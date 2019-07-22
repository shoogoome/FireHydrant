
from common.core.dao.redis import RedisClusterFactory

class RedisSessionFactory(RedisClusterFactory):

    def __init__(self):
        super(RedisSessionFactory, self).__init__("session", 7200)

from common.core.dao.redis import RedisClusterFactory


class TagRedisClusterFactory(RedisClusterFactory):

    def __init__(self, name="default", expire=86400):
        """
        redis集群缓存工厂
        :param name: 前缀名
        :param expire: 过期时间
        """
        super(TagRedisClusterFactory, self).__init__("practice:tag", expire)

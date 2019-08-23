from common.core.dao.redis import RedisClusterFactory



class RankingRedisClusterFactory(RedisClusterFactory):

    def __init__(self):
        """
        排行榜缓存 一个月时间
        """
        super(RankingRedisClusterFactory, self).__init__("ranking", 2592000)
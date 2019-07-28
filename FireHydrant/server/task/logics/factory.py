from common.core.dao.redis import RedisClusterFactory



class TaskRedisClusterFactory(RedisClusterFactory):

    def __init__(self):
        """
        任务缓存

        """
        super(TaskRedisClusterFactory, self).__init__("task", -1)


class ClassificationRedisClusterFactory(RedisClusterFactory):

    def __init__(self):
        """
        分类缓存
        缓存时间不限
        """
        super(ClassificationRedisClusterFactory, self).__init__("classification", -1)


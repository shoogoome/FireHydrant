# -*- coding: utf-8 -*-
# coding:utf-8
import redis
from django.conf import settings
from rediscluster import StrictRedisCluster
from LittlePigHoHo.settings import config_redis_cluster
import json
import threading

redis_pool = {}

redis_cluster_pool = []
# 获取redis集群配置
db_configs = [v for _, v in config_redis_cluster.items()]


class RedisClusterConnection(object):
    """redis集群连接单例模式"""

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return StrictRedisCluster(startup_nodes=db_configs, decode_responses=True, password=settings.REDIS_CONFIG_PASSWORD)
        # return StrictRedisCluster(startup_nodes=db_configs, decode_responses=True)
    def __new__(cls, *args, **kwargs):
        _instance_lock = threading.Lock()

        if not hasattr(RedisClusterConnection, '_instance'):
            with _instance_lock:
                if not hasattr(RedisClusterConnection, '_instance'):
                    RedisClusterConnection._instance = object.__new__(cls)

        return RedisClusterConnection._instance



def get_redis_conn(db=1):
    """
    建立Redis连接
    :param db: 0-session  1-考勤  2-数据库缓存  3-资源缓存  4-评优缓存
    :return:
    """
    if db not in redis_pool.keys():
        redis_pool[db] = redis.ConnectionPool(
            host=settings.REDIS_CONFIG_HOST,
            port=settings.REDIS_CONFIG_PORT,
            password=settings.REDIS_CONFIG_PASSWORD,
            db=db
        )

    return redis.StrictRedis(connection_pool=redis_pool[db])


class RedisClusterFactory(object):

    def __init__(self, name="default", expire=86400):
        """
        redis集群缓存工厂
        :param name: 前缀名
        :param expire: 过期时间
        """
        self.name = name
        self.redis_cluster = RedisClusterConnection()()
        self.expire = expire

    def set_json(self, name, value):
        """
        添加json缓存
        :param name:
        :param value:
        :return:
        """
        _name = self._build_name(name)
        _value = json.dumps(value)
        self.redis_cluster.set(_name, _value)
        self.redis_cluster.expire(_name, self.expire)

    def get_json(self, name):
        """
        获取json缓存
        :param name:
        :return:
        """
        value = self.redis_cluster.get(self._build_name(name))
        return json.loads(value)

    def get(self, name):
        """
        获取缓存
        :param name:
        :return:
        """
        return self.redis_cluster.get(self._build_name(name))

    def set(self, name, value, time=None):
        """
        添加缓存
        :param name:
        :param value:
        :param time:
        :return:
        """
        _name = self._build_name(name)
        self.redis_cluster.set(_name, value)
        self.redis_cluster.expire(_name, self.expire if not time else time)

    def hgetall(self, name):
        """
        获取全部name对应hash内容
        :param name:
        :return:
        """
        return self.redis_cluster.hgetall(self._build_name(name))

    def hget(self, name, key):
        """
        获取name对应key对应
        :param name:
        :param key:
        :return:
        """
        return self.redis_cluster.hget(self._build_name(name), key)

    def hmset(self, name, data):
        """
        添加hash入缓存 一天缓存时间
        :param name:
        :param data:
        :return:
        """
        self.redis_cluster.hmset(self._build_name(name), data)
        self.redis_cluster.expire(self._build_name(name), self.expire)

    def hset(self, name, key, value):
        """
        添加hash 一天缓存
        :param name:
        :param key:
        :param value:
        :return:
        """
        self.redis_cluster.hset(self._build_name(name), key, value)
        self.redis_cluster.expire(self._build_name(name), self.expire)

    def exists(self, name):
        """
        判断存在与否
        :param name:
        :return:
        """
        return self.redis_cluster.exists(self._build_name(name))

    def ttl(self, name):
        """
        返回过期时间
        :param name:
        :return:
        """
        return self.redis_cluster.ttl(self._build_name(name))

    def delete(self, name):
        """
        删除任意形式的键值
        :param name:
        :return:
        """
        self.redis_cluster.delete(self._build_name(name))

    def expired(self, name, time):
        """
        设置过期时间
        :param name:
        :param time:
        :return:
        """
        self.redis_cluster.expire(self._build_name(name), time)

    def keys(self, name: str):
        """
        匹配keys
        :param name:
        :return:
        """
        return self.redis_cluster.keys(name if name[-1] == "*" else name + "*")

    def _build_name(self, *name):
        """
        构建key
        :param name:
        :return:
        """
        return ":".join([self.name, *[str(i) for i in name]])

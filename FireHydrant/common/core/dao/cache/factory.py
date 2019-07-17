# -*- coding: utf-8 -*-
# coding:utf-8

from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


class FireHydrantCacheFactory(object):

    def __init__(self, key_list):
        """
        初始化
        :param key_list:
        设计上字段名会按照:
        类型: {model_cache, default_cache}
        数据表名: {model_table}
        数据集id: {object.id}
        """
        self.cache = cache
        if isinstance(key_list, list) or isinstance(key_list, tuple):
            self.key_list = ':'.join(key_list)
        elif key_list is not None:
            self.key_list = str(key_list)
        else:
            self.key_list = 'default_cache'

    def get_cache(self, key):
        """
        获取缓存信息
        :param key:
        :return:
        """
        l_key = self._build_key(key)
        return self.cache.get(l_key)

    def set_cache(self, key, value, expired=86400):
        """
        设置缓存（生命周期一天）
        :param key:
        :param value:
        :param expired:
        :return:
        """
        l_key = self._build_key(key)
        self.cache.set(l_key, value, expired)

    def get_many_cache(self, keys):
        """
        获取许多缓存数据
        :param keys:
        :return:
        """
        lkeys = [self._build_key(key) for key in keys]
        return self.cache.get_many(lkeys)

    def set_many_cache(self, data, expired=86400):
        """
        设置许多缓存数据
        :param data:
        :param expired:
        :return:
        """
        data = {self._build_key(key): value for key, value in data.item()}
        self.cache.set_many(data, expired)

    def delete_cache(self, key):
        """
        删除缓存信息
        :param key:
        :return:
        """
        l_key = self._build_key(key)
        self.cache.delete(l_key)

    def _build_key(self, key):
        """
        构建缓存字段名
        :return:
        """
        return "{}:{}".format(self.key_list, key)


def delete_model_single_object_cache(instance, **kwargs):
    try:
        table_name = instance._meta.db_table
        factory = FireHydrantCacheFactory(('model_cache', table_name))
        factory.delete_cache(instance.id)
    except:
        pass


def bind_model_cached_manager_signal(model_package):
    """
    自动为model注册缓存清除钩子
    :param model_package: model包
    :return:
    """
    for __model in model_package.__all__:
        m = getattr(model_package, __model)
        if isinstance(getattr(m, 'objects'), FireHydrantCacheFactory):
            receiver(post_save, sender=m)(delete_model_single_object_cache)
            receiver(post_delete, sender=m)(delete_model_single_object_cache)


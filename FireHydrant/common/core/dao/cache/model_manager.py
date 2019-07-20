from django.db.models import Manager
from .factory import FireHydrantCacheFactory


class FireHydrantModelManager(Manager):

    def get_once(self, pk):
        """
        缓存中获取一条记录
        若无则从数据库获取
        替代model中get方法
        :param pk:
        :return:
        """

        if pk is None or pk == "":
            return None
        # 获取数据表名
        table_name = self.model._meta.db_table
        # 初始化缓存
        cache = FireHydrantCacheFactory(('model_cache', table_name))
        # 尝试从缓存获取对象
        obj = cache.get_cache(pk)
        if obj is None:
            # 尝试从数据库中获取
            try:
                obj = super().get_queryset().get(pk=pk)
                cache.set_cache(pk, obj)
            except:
                return None

        return obj

    def all_cache(self):
        """
        全部缓存
        :return:
        """
        objs = super().get_queryset().values('id')
        data = [self.get_once(obj['id']) for obj in objs]
        return data

    def filter_cache(self, **kwargs):
        """
        过滤缓存
        :param kwargs:
        :return:
        """
        objs = super().get_queryset().values('id').filter(**kwargs)
        data = [self.get_once(obj['id']) for obj in objs]
        return data

    def get_many(self, pks):
        """
        get_once延伸
        :param pks:
        :return:
        """
        resule = []
        if isinstance(pks, list):
            for lid in pks:
                try:
                    info = self.get_once(lid)
                    if info is not None:
                        resule.append(info)
                except:
                    pass

        return resule


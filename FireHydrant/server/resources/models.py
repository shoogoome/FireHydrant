from django.db import models
from common.core.dao.time_stamp import TimeStampField
from common.core.dao.cache.factory import delete_model_single_object_cache
from common.core.dao.cache.model_manager import FireHydrantModelManager
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

# Create your models here.

class ResourcesMeta(models.Model):

    class Meta:
        verbose_name = "资源元数据记录"
        verbose_name_plural = "资源元数据记录表"
        app_label = 'resources'

    # 文件名称(禁止为空)
    name = models.CharField(max_length=255)

    # MIME类型
    mime = models.CharField(max_length=100)

    # 文件大小
    size = models.BigIntegerField(default=0)

    # 文件Hash
    hash = models.CharField(max_length=255, blank=True, null=True, default="")

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)

receiver(post_save, sender=ResourcesMeta)(delete_model_single_object_cache)
receiver(post_delete, sender=ResourcesMeta)(delete_model_single_object_cache)
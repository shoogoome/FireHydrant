from django.db import models
from common.core.dao.time_stamp import TimeStampField
from common.entity.task.config import TaskConfigEntity
from common.enum.task.stage import TaskStageEnum
from common.enum.task.type import TaskTypeEnum
from common.core.dao.cache.factory import delete_model_single_object_cache
from common.core.dao.cache.model_manager import FireHydrantModelManager
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from server.task.logics.factory import ClassificationRedisClusterFactory

class Task(models.Model):
    class Meta:
        verbose_name = "任务"
        verbose_name_plural = "任务表"
        app_label = 'task'

    # 发起人
    author = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    # 标题
    title = models.CharField(max_length=255)

    # 任务内容
    content = models.TextField(default="")

    # 附属资源链接
    resource_links = models.TextField(default='', null=True, blank=True)

    # 任务类型（默认个人任务）
    task_type = models.IntegerField(default=TaskTypeEnum.PERSONAL)

    # 当前处在任务阶段(默认发布期)
    stage = models.IntegerField(default=TaskStageEnum.RELEASE)

    # 任务分类
    classification = models.ForeignKey('task.TaskClassification', on_delete=models.SET_NULL, null=True)

    # 委托金
    commission = models.FloatField(default=0.0)

    # 配置
    config = models.TextField(default=TaskConfigEntity().dumps())

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return "[{}] 标题:{} 发起人:{}".format(self.id, self.title, self.author.nickname)


class TaskClassification(models.Model):

    class Meta:
        verbose_name = "任务分类"
        verbose_name_plural = "任务分类表"
        app_label = 'task'

    # 分类名称
    name = models.CharField(max_length=125)

    # 描述
    description = models.CharField(max_length=255, default='', blank=True)

    # 父节点
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return "[{}] 分类名称: {}".format(
            self.id, self.name
        )


class TaskReport(models.Model):

    class Meta:
        verbose_name = "任务进度汇报"
        verbose_name_plural = "任务进度汇报表"
        app_label = 'task'

    # 关联关联
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE)

    # 队长
    leader = models.ForeignKey('account.Account', blank=True, on_delete=models.SET_NULL, null=True)

    # 受托人
    workers = models.ManyToManyField('account.Account', blank=True, related_name='task_workers')

    # 总结
    summary = models.TextField(default="", blank=True)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return "[{}] {}".format(self.id, self.task.title)


def update_cache(instance, **kwargs):
    # 清除数据库缓存
    delete_model_single_object_cache(instance, **kwargs)
    # 分类变动则删除缓存
    redis = ClassificationRedisClusterFactory()
    if redis.exists(str(instance.id)):
        redis.delete(str(instance.id))
    if redis.exists('all'):
        redis.delete('all')

receiver(post_save, sender=Task)(delete_model_single_object_cache)
receiver(post_delete, sender=Task)(delete_model_single_object_cache)
receiver(post_save, sender=TaskClassification)(update_cache)
receiver(post_delete, sender=TaskClassification)(update_cache)
receiver(post_save, sender=TaskReport)(delete_model_single_object_cache)
receiver(post_delete, sender=TaskReport)(delete_model_single_object_cache)
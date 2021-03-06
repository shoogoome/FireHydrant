from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from common.core.dao.cache.factory import delete_model_single_object_cache
from common.core.dao.cache.model_manager import FireHydrantModelManager
from common.core.dao.time_stamp import TimeStampField
from common.enum.task.stage import TaskStageEnum
from common.enum.task.type import TaskTypeEnum
from .logics.signals import handle_classification_post_save_delete, handle_task_post_delete, handle_task_post_save


class Task(models.Model):
    class Meta:
        verbose_name = "任务"
        verbose_name_plural = "任务表"
        app_label = 'task'

    # 发起人
    author = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='task_author')

    # 标题
    title = models.CharField(max_length=255)

    # 任务内容
    content = models.TextField(default="")

    # 附属资源
    resource = models.ManyToManyField('resources.ResourcesMeta', null=True, blank=True, related_name='task_resources')

    # 任务类型（默认个人任务）
    task_type = models.IntegerField(default=TaskTypeEnum.PERSONAL)

    # 当前处在任务阶段(默认发布期)
    stage = models.IntegerField(default=TaskStageEnum.RELEASE)

    # 任务分类
    classification = models.ForeignKey('task.TaskClassification', on_delete=models.SET_NULL, null=True)

    # 配置
    config = models.TextField(default='{}')

    # 发布最终确认时间
    publish_end_time = models.FloatField(default=0.0)

    # 开发时长
    development_time = models.FloatField(default=0.0)

    # 委托金
    commission = models.FloatField(default=0.0)

    # ======== 委托信息 ========

    # 受托方队长
    leader = models.ForeignKey('account.Account', blank=True, on_delete=models.SET_NULL, null=True,
                               related_name='task_leader')

    # 受托人
    workers = models.ManyToManyField('account.Account', blank=True, null=True, related_name='task_workers')

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


class TaskApply(models.Model):
    class Meta:
        verbose_name = "任务申请"
        verbose_name_plural = "任务申请表"
        app_label = 'task'

    # 关联关联
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE)

    # 提交者
    author = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    # 正文
    content = models.TextField(default='')

    # 成就展示
    exhibition = models.ManyToManyField('account.AccountExhibition', null=True, blank=True,
                                        related_name='task_account_exhibition')

    # 重构管理器
    objects = FireHydrantModelManager()

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    def __str__(self):
        return "[{}] author: {}, task: {}".format(self.id, self.author.nickname, self.task.title)


class TaskReport(models.Model):
    class Meta:
        verbose_name = "任务进度汇报"
        verbose_name_plural = "任务进度汇报表"
        app_label = 'task'

    # 关联关联
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE)

    # 附属资源
    resource = models.ManyToManyField('resources.ResourcesMeta', null=True, blank=True,
                                      related_name='task_report_resources')

    # 总结
    summary = models.TextField(default="", blank=True)

    # 阶段
    index = models.IntegerField(default=0)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return "[{}] {}".format(self.id, self.task.title)


receiver(post_save, sender=Task)(handle_task_post_save)
receiver(post_delete, sender=Task)(handle_task_post_delete)
receiver(post_save, sender=TaskClassification)(handle_classification_post_save_delete)
receiver(post_delete, sender=TaskClassification)(handle_classification_post_save_delete)
receiver(post_save, sender=TaskReport)(delete_model_single_object_cache)
receiver(post_delete, sender=TaskReport)(delete_model_single_object_cache)
receiver(post_save, sender=TaskApply)(delete_model_single_object_cache)
receiver(post_delete, sender=TaskApply)(delete_model_single_object_cache)

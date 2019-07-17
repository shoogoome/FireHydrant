from django.db import models
from common.entity.pay.type import PayTypeEntity
from common.core.dao.time_stamp import TimeStampField
from common.enum.pay.type import PayTypeEnum
from common.core.dao.cache.factory import delete_model_single_object_cache
from common.core.dao.cache.model_manager import FireHydrantModelManager
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

# Create your models here.

class PayAccount(models.Model):

    class Meta:
        verbose_name = '支付虚拟账户'
        verbose_name_plural = '支付虚拟账户表'
        app_label = 'pay'

    # 绑定账号
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    # 支付账号
    payment = models.TextField(default=PayTypeEntity().dumps())

    # 当前总金额
    total_amount = models.FloatField(default=0.0)

    # 可用金额（不包括任务ing的冻结金额）
    available_amount = models.FloatField(default=0.0)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[{}] 昵称: {:20s} 邮箱: {:50d}'.format(
            self.id, self.account.nickname, self.account.username
        )

class PayRecord(models.Model):
    """
    交易记录表
    """
    class Meta:
        verbose_name = '交易记录'
        verbose_name_plural = '交易记录表'
        app_label = 'pay'

    # 关联账户
    account  = models.ForeignKey('account.Account', on_delete=models.CASCADE,
                                 related_name='pay_record_account')

    # 支付类型
    pay_type = models.PositiveSmallIntegerField(**PayTypeEnum.get_models_params())

    # 目标账户
    target = models.ForeignKey('account.Account', on_delete=models.SET_NULL,
                               blank=True, null=True, related_name='pay_record_target')

    # 支付金额
    amount = models.FloatField(default=0.0)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return "[{}] 发起账户: {} 创建时间: {}".format(
            self.id, self.account.nickname, self.create_time
        )

receiver(post_save, sender=PayAccount)(delete_model_single_object_cache)
receiver(post_delete, sender=PayAccount)(delete_model_single_object_cache)
receiver(post_save, sender=PayRecord)(delete_model_single_object_cache)
receiver(post_delete, sender=PayRecord)(delete_model_single_object_cache)
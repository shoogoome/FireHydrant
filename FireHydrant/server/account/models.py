# -*- coding: utf-8 -*-
# coding:utf-8

from django.db import models

from common.enum.account.role import AccountRoleEnum
from common.enum.account.sex import AccountSexEnum
from common.core.dao.time_stamp import TimeStampField
from common.core.dao.cache.factory import delete_model_single_object_cache
from common.core.dao.cache.model_manager import FireHydrantModelManager
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class Account(models.Model):
    """
    FireHydrant用户账户主类
    """

    class Meta:
        verbose_name = "FireHydrant主账户"
        verbose_name_plural = "FireHydrant主账户表"
        app_label = 'account'

    # Email用户名
    username = models.CharField(max_length=255)

    # === 基础信息  ===

    # 用户性别
    sex = models.PositiveSmallIntegerField(**AccountSexEnum.get_models_params())

    # 用户昵称
    nickname = models.CharField(max_length=50, default="")

    # 用户角色
    role = models.PositiveSmallIntegerField(**AccountRoleEnum.get_models_params())

    # 电话信息
    phone = models.CharField(max_length=20, default='', blank=True)

    # 电话已通过验证(留着吧，未来可能启用）
    phone_validated = models.BooleanField(default=False)

    # 用户头像
    avator = models.CharField(max_length=200, default='', blank=True)

    # 一句话签名
    motto = models.CharField(max_length=60, default='', blank=True)

    # ==== 扩展信息 ====

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 账户权限信息
    options = models.TextField(default='{}')

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[%d] 昵称：%s, 角色：%s' % (
            self.id, self.nickname, str(self.role)
        )

receiver(post_save, sender=Account)(delete_model_single_object_cache)
receiver(post_delete, sender=Account)(delete_model_single_object_cache)
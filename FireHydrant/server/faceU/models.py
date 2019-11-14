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


class FaceUAccount(models.Model):
    """
    FireHydrant用户账户主类
    """

    class Meta:
        verbose_name = "脸你主账户"
        verbose_name_plural = "脸你主账户表"
        app_label = 'faceU'

    # Email用户名
    username = models.CharField(max_length=255)

    # === 基础信息  ===

    # 用户性别
    sex = models.PositiveSmallIntegerField(**AccountSexEnum.get_models_params())

    # 密码
    password = models.CharField(max_length=255)

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

    # token
    temp_access_token = models.CharField(max_length=100)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[%d] 昵称：%s, 角色：%s' % (
            self.id, self.nickname, str(self.role)
        )

class FaceUFacialMakeup(models.Model):

    class Meta:
        verbose_name = "脸你脸谱"
        verbose_name_plural = "脸你脸谱表"
        app_label = 'faceU'

    # 脸谱uuid
    face_uuid = models.CharField(max_length=255)

    # 名称
    name = models.CharField(max_length=125)

    # 身份证
    id_code = models.CharField(max_length=30, null=True, blank=True)

    # 性别
    sex = models.PositiveSmallIntegerField(**AccountSexEnum.get_models_params(), null=True, blank=True)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[{}] uuid: {}, 姓名: {}, 身份证: {}'.format(
            self.id, self.face_uuid, self.name, self.id_code
        )

class FaceUGroups(models.Model):

    class Meta:
        verbose_name = "脸你分组"
        verbose_name_plural = "脸你分组表"
        app_label = 'faceU'

    # 归属用户
    author = models.ForeignKey('faceU.FaceUAccount', null=True, blank=True, on_delete=models.SET_NULL)

    # 标题
    title = models.CharField(max_length=255)

    # 描述
    description = models.CharField(max_length=255)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[{}] 归属人: {}, 标题: {}'.format(
            self.id, self.author.nickname, self.title
        )

class FaceUFacialMakeupMapping(models.Model):
    class Meta:
        verbose_name = "脸你脸谱分组映射"
        verbose_name_plural = "脸你脸谱分组映射表"
        app_label = 'faceU'

    # 脸谱uuid
    face = models.ForeignKey('faceU.FaceUFacialMakeup', null=True, blank=True, on_delete=models.SET_NULL)

    # 分组
    group = models.ForeignKey('faceU.FaceUGroups', null=True, blank=True, on_delete=models.SET_NULL)

    # 名称
    name = models.CharField(max_length=125)

    # 用户自定义标识
    code = models.CharField(max_length=125, null=True, blank=True)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[{}] 脸: [{}]{}, 分组: [{}]{}, 姓名: {}, 标识: {}'.format(
            self.id, self.face_id, self.face.name, self.group_id,
            self.group.title, self.name, self.code
        )

class FaceUDistinguishRecord(models.Model):

    class Meta:
        verbose_name = "脸你识别记录"
        verbose_name_plural = "脸你识别记录表"
        app_label = 'faceU'

    # 归属人
    author = models.ForeignKey('faceU.FaceUAccount', null=True, blank=True, on_delete=models.SET_NULL)

    # 分组
    group = models.ForeignKey('faceU.FaceUGroups', null=True, blank=True, on_delete=models.SET_NULL)

    # 结果
    result = models.TextField('')

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 最后更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[{}] 归属: [{}] {}, 分组: [{}]{}'.format(
            self.id, self.author_id, self.author.nickname,
            self.group_id, self.group.title if self.group_id else ''
        )

receiver(post_save, sender=FaceUAccount)(delete_model_single_object_cache)
receiver(post_delete, sender=FaceUAccount)(delete_model_single_object_cache)

receiver(post_save, sender=FaceUFacialMakeup)(delete_model_single_object_cache)
receiver(post_delete, sender=FaceUFacialMakeup)(delete_model_single_object_cache)

receiver(post_save, sender=FaceUGroups)(delete_model_single_object_cache)
receiver(post_delete, sender=FaceUGroups)(delete_model_single_object_cache)

receiver(post_save, sender=FaceUDistinguishRecord)(delete_model_single_object_cache)
receiver(post_delete, sender=FaceUDistinguishRecord)(delete_model_single_object_cache)

receiver(post_save, sender=FaceUFacialMakeupMapping)(delete_model_single_object_cache)
receiver(post_delete, sender=FaceUFacialMakeupMapping)(delete_model_single_object_cache)

# -*- coding: utf-8 -*-
# coding:utf-9

from django.db import models
from common.enum.team.maximum_number import TeamMaximumNumberEnum
from common.enum.team.role import TeamRoleEnum
from common.core.dao.time_stamp import TimeStampField
from common.core.dao.cache.factory import delete_model_single_object_cache
from common.core.dao.cache.model_manager import FireHydrantModelManager
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class Team(models.Model):

    class Meta:
        verbose_name = "队伍"
        verbose_name_plural = "队伍表"
        app_label = 'team'

    # 队伍名称
    nickname = models.CharField(default="", max_length=140)

    # 队长
    leader = models.ForeignKey('account.Account', null=True, on_delete=models.SET_NULL, related_name='team_leader')

    # 口号
    slogan = models.CharField(default="", max_length=255)

    # 最大成员数量
    maximum_number = models.PositiveSmallIntegerField(**TeamMaximumNumberEnum.get_models_params())

    # 是否满员
    full = models.BooleanField(default=False)

    # 入队密码
    password = models.CharField(max_length=140, blank=True, default='')

    # 是否为公开队伍
    public = models.BooleanField(default=False)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[{}] 队伍名称: {}, 公开与否: {}'.format(
            self.id, self.nickname, self.public
        )

class AccountTeam(models.Model):

    class Meta:
        verbose_name = "队伍成员"
        verbose_name_plural = "队伍成员表"
        app_label = 'team'

    # 队伍关联
    team = models.ForeignKey('team.Team', on_delete=models.CASCADE)

    # 账户关联
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    # 角色
    role = models.PositiveSmallIntegerField(**TeamRoleEnum.get_models_params())

    # 空闲与否
    free = models.BooleanField(default=True)

    # 创建时间（入队时间）
    create_time = TimeStampField(auto_now_add=True)

    # 更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[{}] 队伍名称: {}, 昵称: {}, 空闲与否: {}'.format(
            self.id, self.team.nickname, self.account.nickname, self.free
        )


receiver(post_save, sender=Team)(delete_model_single_object_cache)
receiver(post_delete, sender=Team)(delete_model_single_object_cache)
receiver(post_save, sender=AccountTeam)(delete_model_single_object_cache)
receiver(post_delete, sender=AccountTeam)(delete_model_single_object_cache)
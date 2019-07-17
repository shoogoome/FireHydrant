# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase

class TaskTypeEnum(EnumBase):

    PERSONAL = 0
    TEAM = 1

    __default__ = PERSONAL
    __desc__ = {
        'PERSONAL': '个人任务',
        'TEAM': '团队任务',
    }
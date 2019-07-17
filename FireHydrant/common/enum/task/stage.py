# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase

class TaskStageEnum(EnumBase):

    RELEASE = 0
    IMPLEMENT = 1
    SETTLEMENT = 2
    COMPLETE = 4

    __default__ = RELEASE
    __desc__ = {
        'RELEASE': '发布期',
        'IMPLEMENT': '执行期',
        'SETTLEMENT': '结算期',
        'COMPLETE': '完成'
    }
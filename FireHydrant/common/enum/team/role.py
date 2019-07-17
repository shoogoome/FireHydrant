# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase


class TeamRoleEnum(EnumBase):

    MEMBER = 0
    LEADER = 99

    __default__ = MEMBER
    __desc__ = {
        'MEMBER': '成员',
        'LEADER': '队长'
    }
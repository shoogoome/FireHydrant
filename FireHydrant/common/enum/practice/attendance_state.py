# -*- coding: utf-8 -*-
# coding:utf-8

from ...core.dao import EnumBase


class AttendanceStateEnum(EnumBase):

    SIGN_IN = 0
    LEAVE = 1
    ABSENT = 2

    __default__ = SIGN_IN
    __desc__ = {
        'SIGN_IN': '签到',
        'LEAVE': '请假',
        'ABSENT': '缺席',
    }

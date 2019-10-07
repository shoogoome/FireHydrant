# -*- coding: utf-8 -*-
# coding:utf-8

from common.core.dao.enumBase import EnumBase


class OddEvenEnum(EnumBase):

    NONE = 0
    ODD = 1
    EVEN = 2

    __default__ = NONE
    __desc__ = {
        'NONE': '单双周',
        'ODD': '单周',
        'EVEN': '双周',
    }

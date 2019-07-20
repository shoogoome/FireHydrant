# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase


class TeamMaximumNumberEnum(EnumBase):

    ONE = 10
    TWO = 30

    __default__ = ONE
    __desc__ = {
        'ONE': '一级 10人',
        'TWO': '二级 30人'
    }
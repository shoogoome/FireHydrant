# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase

class RankingTypeEnum(EnumBase):

    ALL = 0
    MONTH = 1
    QUARTER = 2
    YEAR = 4

    __default__ = ALL
    __desc__ = {
        'ALL': '总榜',
        'MONTH': '月榜',
        'QUARTER': '季榜',
        'YEAR': '年榜',
    }
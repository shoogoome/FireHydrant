# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase

class PayTypeEnum(EnumBase):

    IN = 0
    OUT = 1
    TRANSFER = 2

    __default__ = IN
    __desc__ = {
        'IN': '转入',
        'OUT': '转出',
        'TRANSFER': '转账'
    }
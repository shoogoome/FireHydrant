# -*- coding: utf-8 -*-
# coding:utf-8
from common.core.dao.enumBase import EnumBase


class AccountRoleEnum(EnumBase):

    USER = 0
    ADMIN = 99

    __default__ = USER
    __desc__ = {
        'USER': '用户',
        'ADMIN': '系统管理员'
    }
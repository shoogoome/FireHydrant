# -*- coding: utf-8 -*-
# coding: utf-8


from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.faceU.models import FaceUAccount
from common.enum.account.role import AccountRoleEnum
import json
from common.exceptions.account.info import AccountInfoExcept
from ...logic.account import FaceUAccountLogic
from server.account.logics.info import AccountLogic


class FaceUAccountInfoView(FireHydrantView):

    @check_login
    def get(self, request, aid):
        """
        获取用户信息 or 自己信息
        :param request:
        :param aid:
        :return:
        """
        logic = FaceUAccountLogic(self.auth, aid)
        return SuccessResult(logic.get_account_info())

    @check_login
    def delete(self, request, aid):
        """
        删除用户
        :param request:
        :param aid:
        :return:
        """
        ...

    @check_login
    def put(self, request, aid):
        """
        修改用户信息
        :param request:
        :param aid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = FaceUAccountLogic(self.auth, aid)

        account = logic.account
        with params.diff(account):
            account.nickname = params.str('nickname', desc='昵称')
            account.phone = params.str('phone', desc='电话')
            account.sex = params.int('sex', desc='性别')
        # 头像保存
        if params.has('avator'):
            avator = params.str('avator', desc='头像数据')
            account.avator = AccountLogic.save_account_avator("facec:{}".format(account.id), avator)

        account.save()
        return SuccessResult(id=aid)


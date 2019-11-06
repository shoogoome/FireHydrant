# -*- coding: utf-8 -*-
# coding: utf-8


from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.faceU.models import FaceUAccount
from common.enum.account.role import AccountRoleEnum
import requests
import json
from common.exceptions.account.info import AccountInfoExcept
from ...logic.account import FaceUAccountLogic


class FaceUAccountInfoView(FireHydrantView):

    @check_login
    def get(self, request, aid=''):
        """
        获取用户信息 or 自己信息
        :param request:
        :param aid:
        :return:
        """
        logic = FaceUAccountLogic(self.auth, self.auth.get_account() if not aid else aid)
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
        ...

class FaceUAccountListMget(FireHydrantView):

    @check_login
    def get(self, request):
        """
        获取用户列表
        :param request:
        :return:
        """
        ...

    @check_login
    def post(self, request):
        """
        批量获取用户信息
        :param request:
        :return:
        """
        ...
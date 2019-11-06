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


class FaceUGroupInfo(FireHydrantView):

    @check_login
    def get(self, request, aid, gid):
        """
        获取分组信息
        :param request:
        :param aid:
        :param gid:
        :return:
        """
        ...

    @check_login
    def post(self, request, aid):
        """
        创建分组
        :param request:
        :param aid:
        :return:
        """
        ...

    @check_login
    def put(self, request, aid, gid):
        """
        修改分组信息
        :param request:
        :param aid:
        :param gid:
        :return:
        """
        ...

    @check_login
    def delete(self, request, aid, gis):
        """
        删除分组
        :param request:
        :param aid:
        :param gis:
        :return:
        """
        ...

class FaceUGroupListMget(FireHydrantView):

    @check_login
    def get(self, request, aid):
        """
        获取分组列表
        :param request:
        :param aid:
        :return:
        """
        ...

    @check_login
    def post(self, request, aid):
        """
        批量获取分组信息
        :param request:
        :param aid:
        :return:
        """
        ...
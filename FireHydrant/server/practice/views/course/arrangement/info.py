# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult


class PracticeArrangementInfoView(FireHydrantView):

    def post(self, request, sid, cid):
        """
        创建排课
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        ...


    def get(self, request, sid, cid, aid):
        """
        获取排课信息
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :return:
        """
        ...


    def put(self, request, sid, cid, aid):
        """
        修改排课信息
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :return:
        """
        ...

    def delete(self, request, sid, cid, aid):
        """
        删除排课
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :return:
        """
        ...
# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult


class PracticeArrangementListMgetView(FireHydrantView):


    def post(self, request, sid, cid):
        """
        批量获取排课信息
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        ...

    def get(self, request, sid, cid):
        """
        获取排课列表
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        ...
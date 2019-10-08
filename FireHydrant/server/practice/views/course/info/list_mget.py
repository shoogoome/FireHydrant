# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult

class PracticeCourseListMgetView(FireHydrantView):


    def get(self, request, sid):
        """
        获取课程列表
        :param request:
        :param sid:
        :return:
        """
        ...

    def post(self, request, sid):
        """
        批量获取课程信息
        :param request:
        :param sid:
        :return:
        """
        ...
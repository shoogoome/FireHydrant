# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult


class PracticeStudentInfoView(FireHydrantView):


    def get(self, request, sid, stid):
        """
        获取学生信息
        :param request:
        :param sid:
        :param stid:
        :return:
        """
        ...


    def post(self, request, sid):
        """
        创建学生
        :param request:
        :param sid:
        :return:
        """
        ...


    def put(self, request, sid, stid):
        """
        修改学生信息
        :param request:
        :param sid:
        :param stid:
        :return:
        """
        ...

    def delete(self, request, sid, stid):
        """
        删除学生
        :param request:
        :param sid:
        :param stid:
        :return:
        """
        ...
# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.practice.logics.school import SchoolLogic
from server.practice.models import PracticeSchool

class PracticeCourseInfoView(FireHydrantView):

    def post(self, request, sid):
        """
        创建课程
        :param request:
        :param sid:
        :return:
        """
        ...

    def get(self, request, sid, cid):
        """
        获取课程信息
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        ...

    def put(self, request, sid, cid):
        """
        修改课程信息
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        ...

    def delete(self, request, sid, cid):
        """
        删除课程
        :param request:
        :param sid:
        :param cid:
        :return:
        """
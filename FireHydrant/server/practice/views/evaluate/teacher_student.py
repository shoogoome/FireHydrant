# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...logics.school import SchoolLogic
from ...models import PracticeSchool
from ...logics.classroom import ClassroomLogic
from ...logics.school import SchoolLogic
from ...models import PracticeClassroom


class PracticeTeacherToStudentInfoView(FireHydrantView):

    def get(self, request, sid, cid, eid):
        """
        获取老师对学生评价信息
        :param request:
        :param sid:
        :param cid:
        :param eid:
        :return:
        """
        ...

    def post(self, request, sid, cid):
        """
        批量导入老师对学生评价
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        ...

    def delete(self, request, sid, cid, eid):
        """
        删除老师对学生的评价
        :param request:
        :param sid:
        :param cid:
        :param eid:
        :return:
        """
        ...


class PracticeTeacherToStudentListMgetView(FireHydrantView):

    def get(self, request, sid, cid):
        """
        获取老师对学生评价列表
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        ...

    def post(self, request, sid, cid):
        """
        批量获取老师对学生评价
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        ...

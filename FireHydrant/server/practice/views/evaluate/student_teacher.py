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
from ...logics.evaluate import EvaluateStudentToTeacherLogic
from ...models import PracticeEvaluateStudentToTeacher
from ...logics.course import CourseLogic


class PracticeStudentToTeacherInfoView(FireHydrantView):

    @check_login
    def get(self, request, sid, cid, eid):
        """
        获取学生对老师评价信息
        :param request:
        :param sid:
        :param cid:
        :param eid:
        :return:
        """
        logic = EvaluateStudentToTeacherLogic(self.auth, sid, cid, eid)
        return SuccessResult(logic.get_evaluate_info())

    def post(self, request, sid, cid):
        """
        批量导入学生对老师评价
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        ...

    def delete(self, request, sid, cid, eid):
        """
        删除学生对老师对评价
        :param request: 
        :param sid: 
        :param cid: 
        :param eid: 
        :return: 
        """
        ...


class PracticeStudentToTeacherListMget(FireHydrantView):

    def get(self, request, sid, cid):
        """
        获取学生对老师评价列表
        :param request: 
        :param sid: 
        :param cid: 
        :return: 
        """
        ...

    def post(self, request, sid, cid):
        """
        批量获取学生对老师评价
        :param request: 
        :param sid: 
        :param cid: 
        :return: 
        """
        ...

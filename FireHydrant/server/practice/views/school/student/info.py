# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ....models import PracticeStudentUser
from ....logics.student import StudentUserLogic
from ....logics.school import SchoolLogic
from common.exceptions.practice.school.studentuser import PracticeStudentUserInfoExcept
from django.db.models import Q
from server.account.models import Account
from common.utils.helper.pagination import slicer

class PracticeStudentInfoView(FireHydrantView):

    @check_login
    def get(self, request, sid, stid):
        """
        获取学生信息
        :param request:
        :param sid:
        :param stid:
        :return:
        """
        logic = StudentUserLogic(self.auth, sid, stid)
        return SuccessResult(logic.get_school_info())

    @check_login
    def post(self, request, sid):
        """
        创建学生
        :param request:
        :param sid:
        :return:
        """
        logic = StudentUserLogic(self.auth, sid)
        params = ParamsParser(request.JSON)

        studentuser = logic.create_studentuser(params)
        return SuccessResult(id=studentuser.id)

    @check_login
    def put(self, request, sid, stid):
        """
        修改学生信息
        :param request:
        :param sid:
        :param stid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = StudentUserLogic(self.auth, sid, stid)

        studentuser = logic.studentuser
        with params.diff(studentuser):
            studentuser.realname = params.str('realname', desc='真实名称')

        studentuser.save()
        return SuccessResult(id=stid)

    @check_login
    def delete(self, request, sid, stid):
        """
        删除学生
        :param request:
        :param sid:
        :param stid:
        :return:
        """
        logic = StudentUserLogic(self.auth, sid, stid)

        logic.studentuser.delete()
        return SuccessResult(id=stid)
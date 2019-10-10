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
from django.db.models import Q

class PracticeStudentListMgetView(FireHydrantView):

    @check_login
    def get(self, request, sid):
        """
        获取学生列表
        :param request:
        :param sid:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        studentuser = PracticeStudentUser.objects.filter(school_id=sid).values('id', 'update_time')
        if params.has('key'):
            studentuser = studentuser.filter(
                Q(realname__contains=params.str('key')) |
                Q(code__contains=params.str('key'))
            )

        studentuser_list, pagination = slicer(studentuser, limit=limit, page=page)()()
        return SuccessResult(studentusers=studentuser_list, pagination=pagination)

    @check_login
    def post(self, request, sid):
        """
        批量获取学生信息
        :param request:
        :param sid:
        :return:
        """
        logic = StudentUserLogic(self.auth, sid)
        params = ParamsParser(request.JSON)
        ids = params.list('ids', desc='学生id列表')

        data = []
        studentsusers = PracticeStudentUser.objects.get_many(ids)
        for studentsuser in studentsusers:
            try:
                logic.studentuser = studentsuser
                data.append(logic.get_studentuser_info())
            except:
                pass
        return SuccessResult(data)
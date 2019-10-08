# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.practice.logics.school import SchoolLogic
from server.practice.models import PracticeSchool


class PracticeSchoolInfoView(FireHydrantView):

    @check_login
    def get(self, request, sid):
        """
        获取学校信息
        :param request:
        :param sid:
        :return:
        """
        logic = SchoolLogic(self.auth, sid)
        return SuccessResult(logic.get_school_info())

    @check_login
    def post(self, request):
        """
        创建学校
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        with transaction.atomic():
            school = PracticeSchool.objects.create(
                name=params.str('name', desc="学校名称"),
                description=params.str('description', desc='学校简介'),
            )
        return SuccessResult(id=school.id)

    @check_login
    def delete(self, request, sid):
        """
        删除学校
        :param request:
        :param sid:
        :return:
        """
        logic = SchoolLogic(self.auth, sid)
        logic.school.delete()
        return SuccessResult(sid)

    @check_login
    def put(self, request, sid):
        """
        修改学校信息
        :param request:
        :param sid:
        :return:
        """
        logic = SchoolLogic(self.auth, sid)
        params = ParamsParser(request.JSON)

        school = logic.school
        with params.diff(school):
            school.name = params.str('name', desc="学校名称")
            school.description = params.str('description', desc='学校简介')

        school.save()
        return SuccessResult(id=sid)

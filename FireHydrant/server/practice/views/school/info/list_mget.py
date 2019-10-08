# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.practice.logics.school import SchoolLogic
from server.practice.models import PracticeSchool


class PracticeSchoolListMgetView(FireHydrantView):

    def get(self, request):
        """
        获取学校列表
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)

        schools = PracticeSchool.objects.values('id', 'update_time')
        if params.has('name'):
            schools = schools.filter(name__contains=params.str('name', desc='学校名称'))

        return SuccessResult([{
            'id': school.get('id', ""),
            'update_time': schools.get('update_time', 0.0)
        } for school in schools])


    @check_login
    def post(self, request):
        """
        批量获取学校信息
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        ids = params.list('ids', desc="学校id列表")
        schools = PracticeSchool.objects.get_many(pks=ids)

        data = []
        for school in schools:
            try:
                logic = SchoolLogic(self.auth, school)
                data.append(logic.get_school_info())
            except:
                pass

        return SuccessResult(data)

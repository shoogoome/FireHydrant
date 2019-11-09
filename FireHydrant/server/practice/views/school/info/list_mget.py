# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.firehydrant import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.practice.logics.school import SchoolLogic
from server.practice.models import PracticeSchool
from common.utils.helper.pagination import slicer


class PracticeSchoolListMgetView(FireHydrantView):

    def get(self, request):
        """
        获取学校列表
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        schools = PracticeSchool.objects.values('id', 'update_time')
        if params.has('name'):
            schools = schools.filter(name__contains=params.str('name', desc='学校名称'))

        schools_list, pagination = slicer(schools, limit=limit, page=page)()()
        return SuccessResult(schools=schools_list, pagination=pagination)


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

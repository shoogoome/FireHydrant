# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.firehydrant import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...logics.school import SchoolLogic
from ...models import PracticeSchool
from ...models import PracticeClassroom
from ...logics.classroom import ClassroomLogic
from common.utils.helper.pagination import slicer


class PracticeClassroomListMgetView(FireHydrantView):

    @check_login
    def get(self, request, sid):
        """
        获取学校教室列表
        :param request:
        :param sid:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)


        classrooms = PracticeClassroom.objects.filter(school_id=sid).values('id', 'update_time')
        if params.has('name'):
            classrooms = classrooms.filter(name__contails=params.str('name', desc='教室名称'))
        if params.has('size'):
            classrooms = classrooms.filter(size__gte=params.int('size', desc='教室大小'))

        classrooms_list, pagination = slicer(classrooms, limit=limit, page=page)()()
        return SuccessResult(classrooms=classrooms_list, pagination=pagination)


    @check_login
    def post(self, request, sid):
        """
        批量获取教室信息
        :param request:
        :param sid:
        :return:
        """
        logic = ClassroomLogic(self.auth, sid)
        params = ParamsParser(request.JSON)
        ids = params.list('ids', desc="教室id列表")

        data = []
        classrooms = PracticeClassroom.objects.get_many(ids)
        for classroom in classrooms:
            try:
                if classroom.school != logic.school:
                    continue
                logic.classroom = classroom
                data.append(logic.get_classroom_info())
            except:
                pass
        return SuccessResult(data)


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

class PracticeClassroomInfoView(FireHydrantView):

    @check_login
    def get(self, request, sid, cid):
        """
        获取教室信息
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        logic = ClassroomLogic(self.auth, sid, cid)
        return SuccessResult(logic.get_classroom_info())

    @check_login
    def post(self, request, sid):
        """
        批量导入教室信息
        :param request:
        :param sid:
        :return:
        """
        logic = SchoolLogic(self.auth, sid)
        params = ParamsParser(request.JSON)
        classrooms = params.list('data', desc='教室信息')

        state = {}
        for classroom in classrooms:

            params_classroom = ParamsParser(classroom)
            name = params_classroom.str('name', desc='教室名称')
            try:
                with transaction.atomic():
                    PracticeClassroom.objects.create(
                        school=logic.school,
                        name=name,
                        size=params_classroom.int('size', desc='教室大小'),
                    )
                    state[name] = 1
            except:
                state[name] = 0
        return SuccessResult(state)

    @check_login
    def put(self, request, sid, cid):
        """
        修改教室信息
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        logic = ClassroomLogic(self.auth, sid, cid)
        params = ParamsParser(request.JSON)

        classroom = logic.classroom
        with params.diff(classroom):
            classroom.size = params.int('size', desc='教室大小')
            classroom.name = params.str('name', desc='教室名称')
        classroom.save()

        return SuccessResult(id=cid)

    @check_login
    def delete(self, request, sid, cid):
        """
        删除教室
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        logic = ClassroomLogic(self.auth, sid, cid)
        logic.classroom.delete()

        return SuccessResult(id=cid)

# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from common.enum.practice.oddeven import OddEvenEnum
from common.exceptions.practice.course.arrangement import PracticeArrangementInfoExcept
from ....logics.arrangement import ArrangementLogic
from ....logics.course import CourseLogic
from ....models import PracticeArrangement

class PracticeArrangementInfoView(FireHydrantView):

    @check_login
    def post(self, request, sid, cid):
        """
        创建排课
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        logic = CourseLogic(self.auth, sid, cid)
        params = ParamsParser(request.JSON)

        arrangement = PracticeArrangement.objects.create(
            course=logic.course,
            name=params.str('name', desc='名称'),
            day_of_week=params.int('day_of_week', desc='周几', require=False, default=0, max_value=7, min_value=0),
            start_week=params.int('start_week', desc='开始周', require=False, default=0, min_value=0),
            end_week=params.int('end_week', desc='结束周', require=False, default=0, min_value=0),
            odd_even=params.int('odd_even', desc='单双周', require=False, default=int(OddEvenEnum.NONE)),
            start_section=params.int('start_section', desc='开始节', require=False, default=0, min_value=0),
            end_section=params.int('end_section', desc='结束节', require=False, default=0, min_value=0),
            start_time=params.float('start_time', desc='开始时间'),
            end_tim=params.float('end_time', desc='结束时间')
        )
        return SuccessResult(id=arrangement.id)

    @check_login
    def get(self, request, sid, cid, aid):
        """
        获取排课信息
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :return:
        """
        logic = ArrangementLogic(self.auth, sid, cid, aid)

        return SuccessResult(logic.get_arrangement_info())

    @check_login
    def put(self, request, sid, cid, aid):
        """
        修改排课信息
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :return:
        """
        logic = ArrangementLogic(self.auth, sid, cid, aid)
        params = ParamsParser(request.JSON)

        arrangement = logic.arrangement
        with params.diff(arrangement):
            arrangement.name = params.str('name', desc='名称'),
            arrangement.day_of_week = params.int('day_of_week', desc='周几', max_value=7, min_value=0),
            arrangement.start_week = params.int('start_week', desc='开始周', min_value=0),
            arrangement.end_week = params.int('end_week', desc='结束周', min_value=0),
            arrangement.odd_even = params.int('odd_even', desc='单双周'),
            arrangement.start_section = params.int('start_section', min_value=0),
            arrangement.end_section = params.int('end_section', desc='结束节', min_value=0),
            arrangement.start_time = params.float('start_time', desc='开始时间'),
            arrangement.end_tim = params.float('end_time', desc='结束时间')
        arrangement.save()
        return SuccessResult(id=aid)

    @check_login
    def delete(self, request, sid, cid, aid):
        """
        删除排课
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :return:
        """
        logic = ArrangementLogic(self.auth, sid, cid, aid)
        logic.arrangement.delete()

        return SuccessResult(id=aid)
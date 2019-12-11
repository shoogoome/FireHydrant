# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.firehydrant import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.firehydrant import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from common.enum.practice.oddeven import OddEvenEnum
from common.exceptions.practice.course.arrangement import PracticeArrangementInfoExcept
from ....logics.arrangement import ArrangementLogic
from ....logics.course import CourseLogic
from ....models import PracticeArrangement
from common.utils.helper.pagination import slicer

class PracticeArrangementListMgetView(FireHydrantView):

    @check_login
    def post(self, request, sid, cid):
        """
        批量获取排课信息
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        logic = ArrangementLogic(self.auth, sid, cid)
        params = ParamsParser(request.JSON)
        ids = params.list('ids', desc='排课id列表')

        data = []
        arrangements = PracticeArrangement.objects.get_many(ids)
        for arrangement in arrangements:
            try:
                logic.arrangement = arrangement
                data.append(logic.get_arrangement_info())
            except:
                pass

        return SuccessResult(data)

    @check_login
    def get(self, request, sid, cid):
        """
        获取排课列表
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        arrangements = PracticeArrangement.objects.filter(course_id=cid).values('id', 'update_time')
        if params.has('name'):
            arrangements = arrangements.filter(name__contains=params.str('name', desc='名称'))

        arrangements_list, pagination = slicer(arrangements, limit=limit, page=page)()()
        return SuccessResult(arrangements=arrangements_list, pagination=pagination)

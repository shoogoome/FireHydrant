# -*- coding: utf-8 -*-
# coding: utf-8

from common.core.auth.check_login import check_login
from common.core.http.firehydrant import FireHydrantView
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...logics.attendance import AttendanceLogic
from ...models import PracticeAttendance


class PracticeAttendanceListMgetView(FireHydrantView):

    @check_login
    def get(self, request, sid, cid, aid):
        """
        获取排课考勤
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        attendances = PracticeAttendance.objects.filter(arrangement_id=aid).values('id', 'update_time')

        if params.has('leaver'):
            attendances = attendances.filter(leaver__gte=params.int('leaver', desc='请假次数'))
        if params.has('absent'):
            attendances = attendances.filter(absent__gte=params.int('absent', desc='缺勤'))
        if params.has('late'):
            attendances = attendances.filter(late__gte=params.int('late', desc='迟到'))
        if params.has('key'):
            attendances = attendances.filter(student__realname__contains=params.str('key', desc='关键字（学生姓名）'))

        attendance_list, pagination = slicer(attendances, limit=limit, page=page)()()
        return SuccessResult(attendances=attendance_list, pagination=pagination)

    @check_login
    def post(self, request, sid, cid, aid):
        """
        批量获取考勤信息
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :return:
        """
        logic = AttendanceLogic(self.auth, sid, cid, aid)
        params = ParamsParser(request.JSON)
        ids = params.list('ids', desc='考勤id列表')

        data = []
        attendances = PracticeAttendance.objects.get_many(ids)
        for attendance in attendances:
            try:
                logic.attendance = attendance
                data.append(logic.get_attendance_info())
            except:
                pass

        return SuccessResult(data)

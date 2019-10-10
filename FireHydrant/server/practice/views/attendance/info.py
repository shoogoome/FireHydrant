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
from ...models import PracticeClassroomUser
from common.exceptions.practice.classroom.user import PracticeClassroomUserExcept
from ...logics.arrangement import ArrangementLogic
from ...models import PracticeAttendance
from ...logics.attendance import AttendanceLogic

class PracticeAttendanceInfoView(FireHydrantView):

    @check_login
    def post(self, request, sid, cid, aid):
        """
        导入考勤情况
        主要是因为该系统只是一个附属管理系统
        原本应该直接从主系统数据库获取信息
        现在只能做导入操作
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :return:
        """
        params = ParamsParser(request.JSON)
        data = params.list('data', default='考勤信息')
        logic = ArrangementLogic(self.auth, sid, cid, aid)
        students = logic.arrangement.student.value('code', 'id')

        status = {}
        students_info = {student.get('code', ''): student.get('id', '') for student in students}
        for info in data:
            with transaction.atomic():
                try:
                    PracticeAttendance.objects.create(
                        school_id=sid,
                        course_id=cid,
                        arrangement_id=aid,
                        student_id=students_info.get(info.get('code', ''), -1),
                        leaver=info.get('leaver', 0),
                        absent=info.get('absent', 0),
                        late=info.get('late', 0)
                    )
                    status[info.get('code', '')] = True
                except Exception as ex:
                    transaction.rollback()
                    status[info.get('code', '')] = False
        return SuccessResult(status)

    @check_login
    def get(self, request, sid, cid, aid, atid):
        """
        查看排课考勤情况
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :param atid:
        :return:
        """
        logic = AttendanceLogic(self.auth, sid, cid, aid, atid)
        return SuccessResult(logic.get_attendance_info())

    @check_login
    def put(self, request, sid, cid, aid, atid):
        """
        修改考勤情况
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :param atid:
        :return:
        """
        logic = AttendanceLogic(self.auth, sid, cid, aid, atid)
        params = ParamsParser(request.JSON)

        attendance = logic.attendance
        with params.diff(attendance):
            attendance.leaver = params.int('leaver', desc='请假次数')
            attendance.absent = params.int('absent', desc='缺勤')
            attendance.late = params.int('late', desc='late')
        attendance.save()
        return SuccessResult(id=atid)

    @check_login
    def delete(self, request, sid, cid, aid, atid):
        """
        删除考勤
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :param atid:
        :return:
        """
        logic = AttendanceLogic(self.auth, sid, cid, aid, atid)
        logic.attendance.delete()

        return SuccessResult(id=atid)


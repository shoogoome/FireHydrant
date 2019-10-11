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
from ...logics.evaluate import EvaluateStudentToTeacherLogic
from ...models import PracticeEvaluateStudentToTeacher
from ...logics.course import CourseLogic
from django.db.models import Q
from common.utils.helper.pagination import slicer


class PracticeStudentToTeacherInfoView(FireHydrantView):

    @check_login
    def get(self, request, sid, cid, eid):
        """
        获取学生对老师评价信息
        :param request:
        :param sid:
        :param cid:
        :param eid:
        :return:
        """
        logic = EvaluateStudentToTeacherLogic(self.auth, sid, cid, eid)
        return SuccessResult(logic.get_evaluate_info())

    @check_login
    def post(self, request, sid, cid):
        """
        批量导入学生对老师评价
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        logic = EvaluateStudentToTeacherLogic(self.auth, sid, cid)
        params = ParamsParser(request.JSON)
        data = params.list('data', desc='评价信息')

        # 格式化评价数据（构建key和拿取code）
        codes = []
        params_data = {}
        for da in data:
            try:
                code = da.get('code', '')
                params_data[code] = da
                codes.append(code)
            except:
                pass

        status = {}
        # 获取课程内且code存在的学生账户
        students = logic.get_course_all_students(codes)
        for student in students:
            s_params = ParamsParser(params_data[student.code])
            try:
                with transaction.atomic():
                    PracticeEvaluateStudentToTeacher.objects.create(
                        author=student,
                        star=s_params.int('star', desc='星级', require=False, default=5, min_value=0, max_value=5),
                        message=s_params.str('message', desc='评语', require=False, default=""),
                        teacher=logic.course.author
                    )
                status[student.code] = 1
            except:
                status[student.code] = 0
                pass

        return SuccessResult(status=status)

    @check_login
    def delete(self, request, sid, cid, eid):
        """
        删除学生对老师对评价
        :param request: 
        :param sid: 
        :param cid: 
        :param eid: 
        :return: 
        """
        logic = EvaluateStudentToTeacherLogic(self.auth, sid, cid, eid)

        logic.evaluate.delete()
        return SuccessResult(id=eid)


class PracticeStudentToTeacherListMgetView(FireHydrantView):

    @check_login
    def get(self, request, sid, cid):
        """
        获取学生对老师评价列表
        :param request: 
        :param sid: 
        :param cid: 
        :return: 
        """
        logic = CourseLogic(self.auth, sid, cid)
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        evaluates = PracticeEvaluateStudentToTeacher.objects.filter(teacher=logic.course.author).values('id', 'update_time')
        if params.has('star'):
            evaluates = evaluates.filter(star=params.int('star', desc='星级'))
        if params.has('key'):
            key = params.str('key', desc='关键字（学生真实名称、学号）弱匹配')
            evaluates = evaluates.filter(
                Q(author__realname__contains=key) |
                Q(author__code__contains=key)
            )

        evaluates_list, pagination = slicer(evaluates, limit=limit, page=page)()()
        return SuccessResult(evaluates=evaluates_list, pagination=pagination)

    @check_login
    def post(self, request, sid, cid):
        """
        批量获取学生对老师评价
        :param request: 
        :param sid: 
        :param cid: 
        :return: 
        """
        logic = EvaluateStudentToTeacherLogic(self.auth, sid, cid)
        params = ParamsParser(request.JSON)
        ids = params.list('ids', desc='评价列表')

        data = []
        evaluates = PracticeEvaluateStudentToTeacher.objects.get_many(ids)
        for evaluate in evaluates:
            try:
                logic.evaluate = evaluate
                data.append(logic.get_evaluate_info())
            except:
                pass

        return SuccessResult(data)


# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.exceptions.practice.course.info import PracticeCourseInfoExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ....logics.course import CourseLogic
from ....logics.school import SchoolLogic
from ....models import PracticeCourse
from ....models import PracticeTag


class PracticeCourseInfoView(FireHydrantView):

    @check_login
    def post(self, request, sid):
        """
        创建课程
        :param request:
        :param sid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = SchoolLogic(self.auth, sid)

        try:
            with transaction.atomic():
                course = PracticeCourse.objects.create(
                    school=logic.school,
                    author=self.auth.get_account(),
                    tag_id=params.int('tag', desc='tagid') if params.has('tag') else None,
                    name=params.str('name', desc='课程名称'),
                    description=params.str('description', desc='描述', default='', require=False),
                    start_time=params.float('start_time', desc='开始时间', default=0.0, require=False),
                    end_time=params.float('end_time', desc='结束时间', default=0.0, require=False)
                )
        except Exception as ex:
            raise PracticeCourseInfoExcept.course_create_fail()
        return SuccessResult(id=course.id)

    @check_login
    def get(self, request, sid, cid):
        """
        获取课程信息
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        logic = CourseLogic(self.auth, sid, cid)

        return SuccessResult(logic.get_course_info())

    @check_login
    def put(self, request, sid, cid):
        """
        修改课程信息
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = CourseLogic(self.auth, sid, cid)
        course = logic.course

        if params.has('tag'):
            tag = PracticeTag.objects.get_once(params.int('tag', desc='tagid'))
            if tag:
                course.tag = tag
        with params.diff(course):
            course.name = params.str('name', desc='名称')
            course.description = params.str('description', desc='简介')
            course.start_time = params.float('start_time', desc='开始时间')
            course.end_time = params.float('end_time', desc='结束时间')
        course.save()
        return SuccessResult(id=cid)

    @check_login
    def delete(self, request, sid, cid):
        """
        删除课程
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        logic = CourseLogic(self.auth, sid, cid)
        logic.course.delete()
        return SuccessResult(id=cid)

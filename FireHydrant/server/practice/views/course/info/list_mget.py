# -*- coding: utf-8 -*-
# coding: utf-8

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ....logics.course import CourseLogic
from ....models import PracticeCourse
from common.utils.helper.pagination import slicer


class PracticeCourseListMgetView(FireHydrantView):

    @check_login
    def get(self, request, sid):
        """
        获取课程列表
        :param request:
        :param sid:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)


        courses = PracticeCourse.objects.filter(school_id=sid).values('id', 'update_time')
        if params.has('name'):
            courses = courses.filter(name__contains=params.str('name', desc='名称'))
        if params.has('tag'):
            courses = courses.filter(tag_id=params.int('tag', desc='tagid'))
        if params.has('start_time'):
            courses = courses.filter(start_time__gte=params.float('start_time', desc='开始时间'))
        if params.has('end_time'):
            courses = courses.filter(end_time__lte=params.float('end_time', desc='结束时间'))

        courses_list, pagination = slicer(courses, limit=limit, page=page)()()
        return SuccessResult(courses=courses_list, pagination=pagination)

    @check_login
    def post(self, request, sid):
        """
        批量获取课程信息
        :param request:
        :param sid:
        :return:
        """
        params = ParamsParser(request.JSON)
        ids = params.list('ids', desc='课程id列表')
        logic = CourseLogic(self.auth, sid)

        data = []
        courses = PracticeCourse.objects.get_many(ids)
        for course in courses:
            try:
                logic.course = course
                data.append(logic.get_course_info())
            except:
                pass

        return SuccessResult(data)

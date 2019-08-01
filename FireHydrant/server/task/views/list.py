# -*- coding: utf-8 -*-
# coding: utf-8

import time

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.enum.task.stage import TaskStageEnum
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ..models import Task


class TaskListView(FireHydrantView):

    @check_login
    def get(self, request):
        """
        获取任务列表
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        tasks = Task.objects.values('id', 'title', 'task_type', 'stage', 'classification', 'update_time')
        if params.has('task_type'):
            tasks = tasks.filter(task_type=params.int('task_type', desc='任务类型'))
        if params.has('stage'):
            stage = params.int('stage', desc='任务阶段')
            if stage == int(TaskStageEnum.RELEASE):
                tasks.exclude(publish_end_time__lte=time.time())
            tasks = tasks.filter(stage=stage)
        if params.has('classification'):
            tasks = tasks.filter(classification_id=params.int('classification', desc='分类id'))
        if params.has('title'):
            tasks = tasks.filter(title__contains=params.str('title', desc='标题'))

        tasks, pagination = slicer(tasks, limit=limit, page=page)()()

        return SuccessResult(tasks=tasks, pagination=pagination)

    def post(self, request):
        """
        批量获取任务信息
        :param request:
        :return:
        """
        ...

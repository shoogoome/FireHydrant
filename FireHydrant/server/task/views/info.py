# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.constants.length_limitation import *
from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.exceptions.task.task import TaskInfoExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ..logics.task import TaskLogic
from ..models import Task, TaskClassification
from common.enum.task.type import TaskTypeEnum
from common.exceptions.task.classification import TaskClassificationExcept
from common.enum.task.stage import TaskStageEnum

class TaskInfoView(FireHydrantView):

    @check_login
    def post(self, request):
        """
        创建任务
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        task_type = params.int('task_type', desc='任务分类')
        if not TaskTypeEnum.has_value(task_type):
            raise TaskInfoExcept.task_type_is_not_exists()

        if params.has('classification'):
            classification = TaskClassification.objects.get_once(pk=params.int('classification', desc='任务类型id'))
            if classification is None:
                raise TaskClassificationExcept.classification_is_not_exists()

        with transaction.atomic():
            task = Task.objects.create(
                author=self.auth.get_account(),
                title=params.str('title', desc='标题'),
                content=params.str('content', desc='正文'),
                commission=params.float('commission', desc='委托金'),
                task_type=task_type,
            )
        if params.has('classification'):
            task.classification = classification
        task.save()
        return SuccessResult(id=task.id)

    @check_login
    def get(self, request, tid):
        """
        查询任务信息
        :param request:
        :param tid:
        :return:
        """
        logic = TaskLogic(self.auth, tid)

        return SuccessResult(logic.get_task_info())


    def put(self, request, tid):
        """
        修改任务信息
        :param request:
        :param tid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = TaskLogic(self.auth, tid)

        task = logic.task
        # TODO 有人申请接任务则不允许在修改信息
        # if task.stage != int(TaskStageEnum.RELEASE):
        #     raise TaskInfoExcept.is_not_in_release()

        if params.has('task_type'):
            task_type = params.int('task_type', desc='任务分类')
            if not TaskTypeEnum.has_value(task_type):
                raise TaskInfoExcept.task_type_is_not_exists()
            task.task_type = task_type
        if params.has('classification'):
            classification = TaskClassification.objects.get_once(pk=params.int('classification', desc='任务类型id'))
            if classification is not None:
                task.classification = classification
                task.save()

        with params.diff(task):
            task.title = params.str('title', desc='标题')
            task.content = params.str('content',desc='正文')







    def delete(self, request, tid):
        """
        删除任务
        :param request:
        :param tid:
        :return:
        """
        ...









# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.constants.params import TASK_PUBLIC_WAIT_TIME
from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.enum.task.type import TaskTypeEnum
from common.exceptions.task.classification import TaskClassificationExcept
from common.exceptions.task.task import TaskInfoExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ..logics.task import TaskLogic
from ..models import Task, TaskClassification, TaskApply


class TaskInfoView(FireHydrantView):

    @check_login
    def post(self, request):
        """
        创建任务
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        publish_end_time = params.float('publish_end_time', desc='任务配置')
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
                task_type=task_type,
                commission=params.float('commission', desc='委托金'),
                development_time=params.float('development_time', desc='开发时长'),
            )
        if params.has('classification'):
            task.classification = classification
        # 设定的过期时间超过30天 或者不规范 则强制30天
        if publish_end_time > (TASK_PUBLIC_WAIT_TIME + task.create_time) or publish_end_time < task.create_time:
            task.publish_end_time = TASK_PUBLIC_WAIT_TIME + task.create_time
        else:
            task.publish_end_time = publish_end_time

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

    @check_login
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
        # 有人申请接任务则不允许再修改信息
        if TaskApply.objects.filter(task=task).exists():
            raise TaskInfoExcept.task_conduct()

        if params.has('task_type'):
            task_type = params.int('task_type', desc='任务分类')
            if not TaskTypeEnum.has_value(task_type):
                raise TaskInfoExcept.task_type_is_not_exists()
            task.task_type = task_type
        if params.has('classification'):
            classification = TaskClassification.objects.get_once(pk=params.int('classification', desc='任务类型id'))
            if classification is None:
                raise TaskClassificationExcept.classification_is_not_exists()
            task.classification = classification
            task.save()

        with params.diff(task):
            task.title = params.str('title', desc='标题')
            task.content = params.str('content', desc='正文')
            task.commission = params.float('commission', desc='委托金')
            task.development_time = params.float('development_time', desc='开发时长')

        if params.has('publish_end_time'):
            publish_end_time = params.float('publish_end_time', desc='发布最终确认时间')
            # 设定的过期时间超过30天则强制30天
            if publish_end_time > (TASK_PUBLIC_WAIT_TIME + task.create_time):
                task.publish_end_time = TASK_PUBLIC_WAIT_TIME + task.create_time
            else:
                task.publish_end_time = publish_end_time
        task.save()

        return SuccessResult(id=tid)

    @check_login
    def delete(self, request, tid):
        """
        删除任务
        :param request:
        :param tid:
        :return:
        """
        logic = TaskLogic(self.auth, tid)

        logic.task.delete()
        return SuccessResult(id=tid)

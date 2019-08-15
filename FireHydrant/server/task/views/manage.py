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


class TaskManageView(FireHydrantView):

    @check_login
    def get(self, request, tid):
        """
        获取任务申请列表
        :param request:
        :param tid:
        :return:
        """
        ...

    @check_login
    def post(self, request, tid):
        """
        提交任务申请
        :param request:
        :param tid:
        :return:
        """
        ...

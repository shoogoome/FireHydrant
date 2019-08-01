# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.constants.length_limitation import *
from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.exceptions.task.classification import TaskClassificationExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...logics.classification import TaskClassificationLogic
from ...models import TaskClassification


class TaskListView(FireHydrantView):

    def get(self, request):
        """
        获取任务列表
        :param request:
        :return:
        """
        ...

    def post(self, request):
        """
        批量获取任务信息
        :param request:
        :return:
        """
        ...


    




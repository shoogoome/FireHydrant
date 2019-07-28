# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.constants.length_limitation import *
from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.enum.team.role import TeamRoleEnum
from common.exceptions.team.info import TeamInfoExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...models import TaskClassification
from common.exceptions.task.classification import TaskClassificationExcept


class TaskClassificationInfoView(FireHydrantView):

    @check_login
    def post(self, request):
        """
        创建任务分类
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        if params.int('parent'):
            parent = TaskClassification.objects.get_once(pk=params.int('parent', desc='父节点id'))
            if parent is None:
                raise TaskClassificationExcept.classification_is_not_exists()

        with transaction.atomic():
            classification = TaskClassification.objects.create(
                name=params.str('name', desc='分类名称'),
                description=params.str('description', desc='简介', default='', require=False),
            )

        if params.int('parent'):
            classification.parent = parent
            classification.save()

        return SuccessResult(id=classification.id)

    def get(self, request):
        """
        获取任务分类信息
        :param request:
        :return:
        """
        ...

    def put(self, request):
        """
        修改分类信息
        :param request:
        :return:
        """
        ...

    def delete(self, request):
        """
        删除分类信息
        :param request:
        :return:
        """
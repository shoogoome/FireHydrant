# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.constants.length_limitation import *
from common.core.auth.check_login import check_login
from common.core.http.firehydrant import FireHydrantView
from common.exceptions.task.classification import TaskClassificationExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...logics.classification import TaskClassificationLogic
from ...models import TaskClassification


class TaskClassificationInfoView(FireHydrantView):

    @check_login
    def post(self, request):
        """
        创建任务分类
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        if params.has('parent'):
            parent = TaskClassification.objects.get_once(pk=params.int('parent', desc='父节点id'))
            if parent is None:
                raise TaskClassificationExcept.classification_is_not_exists()

        with transaction.atomic():
            classification = TaskClassification.objects.create(
                name=params.str('name', desc='分类名称', max_length=MAX_CLASSIFICATION_LENGTH),
                description=params.str('description', desc='简介', default='', require=False,
                                       max_length=MAX_DESCRIPETION_LENGTH),
            )

        if params.has('parent'):
            classification.parent = parent
            classification.save()

        return SuccessResult(id=classification.id)

    def get(self, request, cid):
        """
        获取任务分类信息
        :param request:
        :param cid:
        :return:
        """
        logic = TaskClassificationLogic(self.auth, cid)
        return SuccessResult(logic.get_classification_info())

    @check_login
    def put(self, request, cid):
        """
        修改分类信息
        :param request:
        :param cid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = TaskClassificationLogic(self.auth, cid)

        # 环状警告
        # if params.has('parent'):
        #     parent = TaskClassification.objects.get_once(pk=params.int('parent', desc='父节点id'))
        #     if parent is None:
        #         raise TaskClassificationExcept.parent_is_not_exists()

        classification = logic.classification
        with params.diff(classification):
            classification.name = params.str('name', desc='名称', max_length=MAX_CLASSIFICATION_LENGTH)
            classification.description = params.str('description', desc='简介', max_length=MAX_DESCRIPETION_LENGTH)

        # if params.has('parent'):
        #     classification.parent = parent
        classification.save()

        return SuccessResult(id=cid)

    @check_login
    def delete(self, request, cid):
        """
        删除分类信息
        :param request:
        :param cid:
        :return:
        """
        logic = TaskClassificationLogic(self.auth, cid)
        logic.classification.delete()

        return SuccessResult(id=cid)

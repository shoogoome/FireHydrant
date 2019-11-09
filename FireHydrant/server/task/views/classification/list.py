# -*- coding: utf-8 -*-
# coding: utf-8

from common.core.http.firehydrant import FireHydrantView
from common.utils.helper.result import SuccessResult
from ...logics.classification import TaskClassificationLogic


class TaskClassificationListView(FireHydrantView):

    def get(self, request):
        """
        获取全部任务分类列表
        :param request:
        :return:
        """
        return SuccessResult(TaskClassificationLogic.get_all_classification_info())
